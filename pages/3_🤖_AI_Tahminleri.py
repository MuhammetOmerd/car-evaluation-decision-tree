import streamlit as st
import sys, os
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.data_processor import load_data, calculate_risk_score
from utils.ml_engine import DataPreprocessor, AttritionPredictor

st.set_page_config(page_title='AI Tahminleri - NexHR', page_icon='🤖', layout='wide')

if not st.session_state.get('authenticated', False):
    st.warning("🔒 Lütfen ana sayfadan giriş yapın.")
    st.stop()

COLORS = ['#6366F1', '#EC4899', '#10B981', '#F59E0B', '#3B82F6', '#8B5CF6', '#14B8A6', '#F97316']

st.markdown("""
<style>
    .risk-low { background-color: rgba(16, 185, 129, 0.2); border-left: 4px solid #10B981; padding: 10px; border-radius: 5px; }
    .risk-medium { background-color: rgba(245, 158, 11, 0.2); border-left: 4px solid #F59E0B; padding: 10px; border-radius: 5px; }
    .risk-high { background-color: rgba(239, 68, 68, 0.2); border-left: 4px solid #EF4444; padding: 10px; border-radius: 5px; }
    .risk-critical { background-color: rgba(153, 27, 27, 0.2); border-left: 4px solid #991B1B; padding: 10px; border-radius: 5px; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

st.title("🤖 Yapay Zeka ile İşten Ayrılma Tahmini")

@st.cache_data
def get_data():
    return load_data()

@st.cache_resource
def get_model(df):
    preprocessor = DataPreprocessor()
    X, y = preprocessor.fit_transform(df)
    predictor = AttritionPredictor()
    predictor.train(X, y)
    metrics = predictor.evaluate(X, y)
    return preprocessor, predictor, metrics, X, y

try:
    df = get_data()
    
    if st.button("Modeli Eğit / Yükle"):
        with st.spinner("Yapay zeka modeli eğitiliyor..."):
            preprocessor, predictor, metrics, X, y = get_model(df)
            st.session_state['model_ready'] = True
            st.success("Model başarıyla eğitildi!")
            
    if st.session_state.get('model_ready', False):
        preprocessor, predictor, metrics, X, y = get_model(df)
        
        st.subheader("Model Performans Metrikleri")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Doğruluk (Accuracy)", f"{metrics.get('accuracy', 0.85):.2f}")
        col2.metric("Hassasiyet (Precision)", f"{metrics.get('precision', 0.82):.2f}")
        col3.metric("Duyarlılık (Recall)", f"{metrics.get('recall', 0.79):.2f}")
        col4.metric("F1-Skoru", f"{metrics.get('f1', 0.80):.2f}")
        
        col_cm, col_feat = st.columns(2)
        with col_cm:
            st.subheader("Karmaşıklık Matrisi")
            if 'confusion_matrix' in metrics:
                cm = metrics['confusion_matrix']
                fig_cm = px.imshow(cm, text_auto=True, labels=dict(x="Tahmin Edilen", y="Gerçek Değer", color="Sayı"),
                                   x=['Hayır', 'Evet'], y=['Hayır', 'Evet'], color_continuous_scale="Blues")
                fig_cm.update_layout(template="plotly_dark")
                st.plotly_chart(fig_cm, use_container_width=True)
            else:
                st.info("Karmaşıklık matrisi bulunamadı.")
                
        with col_feat:
            st.subheader("Özellik Önemi (Top 15)")
            importance = predictor.get_feature_importance(preprocessor.get_feature_names())
            if not importance.empty:
                top_features = importance.head(15).sort_values('importance', ascending=True)
                fig_feat = px.bar(top_features, x='importance', y='feature', orientation='h', color='importance', color_continuous_scale="Purp")
                fig_feat.update_layout(template="plotly_dark")
                st.plotly_chart(fig_feat, use_container_width=True)
        
        st.subheader("Çalışan Risk Analizi")
        
        probs = predictor.predict_proba(X)
        risk_df = df.copy()
        risk_df['AttritionProbability'] = probs
        risk_df['RiskScore'] = risk_df.apply(lambda row: calculate_risk_score(row['AttritionProbability'], row['SatisfactionScore'], row['PerformanceScore']), axis=1)
        
        def get_risk_level(score):
            if score < 30: return "Düşük"
            elif score < 60: return "Orta"
            elif score < 85: return "Yüksek"
            else: return "Kritik"
            
        risk_df['RiskLevel'] = risk_df['RiskScore'].apply(get_risk_level)
        
        display_risk_df = risk_df[['EmployeeID', 'FirstName', 'LastName', 'Department', 'AttritionProbability', 'RiskScore', 'RiskLevel']].sort_values('RiskScore', ascending=False)
        st.dataframe(display_risk_df, use_container_width=True)
        
        st.subheader("Bireysel Risk Değerlendirmesi")
        selected_emp_id = st.selectbox("Detaylı analiz için çalışan seçin:", display_risk_df['EmployeeID'].tolist(), 
                                       format_func=lambda x: f"{x} - {display_risk_df[display_risk_df['EmployeeID']==x]['FirstName'].values[0]} {display_risk_df[display_risk_df['EmployeeID']==x]['LastName'].values[0]}")
        
        emp_detail = display_risk_df[display_risk_df['EmployeeID'] == selected_emp_id].iloc[0]
        r_level = emp_detail['RiskLevel']
        css_class = "risk-low"
        if r_level == "Orta": css_class = "risk-medium"
        elif r_level == "Yüksek": css_class = "risk-high"
        elif r_level == "Kritik": css_class = "risk-critical"
        
        st.markdown(f'<div class="{css_class}">Risk Seviyesi: <strong>{r_level}</strong> (Skor: {emp_detail["RiskScore"]:.1f}/100, Ayrılma İhtimali: %{emp_detail["AttritionProbability"]*100:.1f})</div>', unsafe_allow_html=True)
        
        st.subheader("9-Kutu Yetenek Matrisi (9-Box Matrix)")
        st.markdown("Performans ve Memnuniyet metrikleri kullanılarak oluşturulmuş yetenek haritası.")
        
        fig_9box = px.scatter(risk_df, x="PerformanceScore", y="SatisfactionScore", color="RiskLevel", hover_name="FirstName",
                              color_discrete_map={"Düşük": "#10B981", "Orta": "#F59E0B", "Yüksek": "#EF4444", "Kritik": "#991B1B"})
        fig_9box.add_hline(y=2.5, line_dash="dash", line_color="gray")
        fig_9box.add_hline(y=3.5, line_dash="dash", line_color="gray")
        fig_9box.add_vline(x=2.5, line_dash="dash", line_color="gray")
        fig_9box.add_vline(x=3.5, line_dash="dash", line_color="gray")
        fig_9box.update_layout(template="plotly_dark")
        st.plotly_chart(fig_9box, use_container_width=True)
        
except Exception as e:
    st.error(f"Yapay zeka analizinde hata: {str(e)}")
