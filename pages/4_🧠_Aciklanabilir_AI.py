import streamlit as st
import sys, os
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.data_processor import load_data
from utils.ml_engine import DataPreprocessor, AttritionPredictor, ExplainableAI

st.set_page_config(page_title='Açıklanabilir AI - NexHR', page_icon='🧠', layout='wide')

if not st.session_state.get('authenticated', False):
    st.warning("🔒 Lütfen ana sayfadan giriş yapın.")
    st.stop()

st.markdown("""
<style>
    .info-box {
        background-color: rgba(59, 130, 246, 0.1);
        border-left: 4px solid #3B82F6;
        padding: 15px;
        border-radius: 5px;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

st.title("🧠 Açıklanabilir AI (Explainable AI)")
st.markdown('<div class="info-box"><strong>Açıklanabilir Yapay Zeka (XAI)</strong>, makine öğrenimi modelinin aldığı kararların arkasındaki nedenleri şeffaf bir şekilde gösterir. SHAP (SHapley Additive exPlanations) yöntemi kullanılarak, her bir özelliğin modelin tahmini üzerindeki etkisi matematiksel olarak hesaplanır.</div>', unsafe_allow_html=True)

@st.cache_data
def get_data():
    return load_data()

@st.cache_resource
def compute_shap(df):
    preprocessor = DataPreprocessor()
    X, y = preprocessor.fit_transform(df)
    predictor = AttritionPredictor()
    predictor.train(X, y)
    
    explainer = ExplainableAI(predictor.model, preprocessor.get_feature_names())
    shap_values = explainer.get_shap_values(X)
    return preprocessor, predictor, explainer, shap_values, X

try:
    df = get_data()
    
    if st.button("SHAP Analizini Başlat (Yoğun İşlem)"):
        with st.spinner("SHAP değerleri hesaplanıyor..."):
            preprocessor, predictor, explainer, shap_values, X = compute_shap(df)
            st.session_state['shap_ready'] = True
            st.success("SHAP analizi tamamlandı!")
            
    if st.session_state.get('shap_ready', False):
        preprocessor, predictor, explainer, shap_values, X = compute_shap(df)
        
        st.subheader("Küresel Özellik Etkisi (Global Feature Importance)")
        summary_df = explainer.get_summary_data(shap_values, X)
        
        if not summary_df.empty:
            fig_global = px.bar(summary_df.head(15).sort_values('importance', ascending=True), 
                                x='importance', y='feature', orientation='h',
                                color='importance', color_continuous_scale="Mint",
                                labels={'importance': 'Ortalama SHAP Değeri (Mutlak Etki)', 'feature': 'Özellik'})
            fig_global.update_layout(template="plotly_dark")
            st.plotly_chart(fig_global, use_container_width=True)
            
            st.subheader("SHAP Özeti (Beeswarm Dağılımı)")
            # Simulating beeswarm plot with scatter
            top_features = summary_df['feature'].head(10).tolist()
            
            plot_data = []
            for i, feat in enumerate(top_features):
                feat_idx = list(preprocessor.get_feature_names()).index(feat)
                feat_shap = shap_values[:, feat_idx]
                feat_vals = X[:, feat_idx]
                
                for s, v in zip(feat_shap, feat_vals):
                    plot_data.append({'Feature': feat, 'SHAP Value': s, 'Feature Value': v})
                    
            plot_df = pd.DataFrame(plot_data)
            fig_bee = px.strip(plot_df, x='SHAP Value', y='Feature', color='Feature Value',
                               orientation='h', stripmode='overlay')
            fig_bee.update_layout(template="plotly_dark")
            st.plotly_chart(fig_bee, use_container_width=True)
        else:
            st.info("SHAP özeti verisi bulunamadı.")
            
        st.subheader("Bireysel Açıklama (Şelale Grafiği)")
        
        emp_indices = list(range(len(df)))
        emp_names = df['FirstName'] + ' ' + df['LastName'] + ' (ID: ' + df['EmployeeID'].astype(str) + ')'
        selected_idx = st.selectbox("Analiz edilecek çalışanı seçin:", emp_indices, format_func=lambda x: emp_names.iloc[x])
        
        ind_exp = explainer.get_individual_explanation(shap_values, X, selected_idx)
        if not ind_exp.empty:
            ind_exp['Color'] = np.where(ind_exp['shap_value'] > 0, '#EF4444', '#10B981')
            ind_exp['FormattedFeature'] = ind_exp['feature'] + " = " + ind_exp['feature_value'].astype(str)
            
            fig_waterfall = go.Figure(go.Waterfall(
                name="SHAP",
                orientation="h",
                measure=["relative"] * len(ind_exp),
                y=ind_exp['FormattedFeature'],
                x=ind_exp['shap_value'],
                connector={"line": {"color": "rgb(63, 63, 63)"}},
                decreasing={"marker": {"color": "#10B981"}},
                increasing={"marker": {"color": "#EF4444"}},
                totals={"marker": {"color": "#3B82F6"}}
            ))
            fig_waterfall.update_layout(title=f"{emp_names.iloc[selected_idx]} için Model Tahmin Gerekçeleri", template="plotly_dark")
            st.plotly_chart(fig_waterfall, use_container_width=True)
            
            st.markdown("**(Kırmızı)** değerler ayrılma ihtimalini *artıran*, **(Yeşil)** değerler ise ayrılma ihtimalini *azaltan* faktörleri göstermektedir.")

except Exception as e:
    st.error(f"SHAP analizi sırasında hata: {str(e)}")
