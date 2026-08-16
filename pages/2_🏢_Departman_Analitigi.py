import streamlit as st
import sys, os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.data_processor import load_data, get_department_stats

st.set_page_config(page_title='Departman Analitiği - NexHR', page_icon='🏢', layout='wide')

COLORS = ['#6366F1', '#EC4899', '#10B981', '#F59E0B', '#3B82F6', '#8B5CF6', '#14B8A6', '#F97316']

st.markdown("""
<style>
    .dept-card {
        background: linear-gradient(135deg, #1e1e2d 0%, #2d2d44 100%);
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        border-top: 4px solid #3B82F6;
    }
    .dept-value {
        font-size: 24px;
        font-weight: bold;
        color: #fff;
    }
    .dept-label {
        font-size: 14px;
        color: #a0a0b2;
    }
</style>
""", unsafe_allow_html=True)

st.title("🏢 Departman Analitiği")

@st.cache_data
def get_data():
    return load_data()

try:
    df = get_data()
    dept_stats = get_department_stats(df).reset_index()
    
    st.sidebar.header("Departman Seçimi")
    selected_dept = st.sidebar.selectbox("Detaylı analiz için seçin", df['Department'].unique())
    
    dept_df = df[df['Department'] == selected_dept]
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f'<div class="dept-card"><div class="dept-value">{len(dept_df)}</div><div class="dept-label">Çalışan Sayısı</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="dept-card"><div class="dept-value">{dept_df["PerformanceScore"].mean():.2f}</div><div class="dept-label">Ortalama Performans</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="dept-card"><div class="dept-value">{dept_df["SatisfactionScore"].mean():.2f}</div><div class="dept-label">Ortalama Memnuniyet</div></div>', unsafe_allow_html=True)
    with col4:
        attrition_rate = (dept_df['Attrition'] == 'Evet').mean() * 100
        st.markdown(f'<div class="dept-card"><div class="dept-value">%{attrition_rate:.1f}</div><div class="dept-label">İşten Ayrılma Oranı</div></div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_radar, col_heat = st.columns(2)
    with col_radar:
        st.subheader("Departmanlar Arası Karşılaştırma (Radar)")
        
        normalized_stats = dept_stats.copy()
        for col in ['avg_performance', 'avg_satisfaction', 'avg_income', 'avg_work_life_balance']:
            if col in normalized_stats.columns:
                normalized_stats[col] = normalized_stats[col] / normalized_stats[col].max()
            
        fig_radar = go.Figure()
        for i, row in normalized_stats.iterrows():
            if 'avg_work_life_balance' in row:
                values = [row['avg_performance'], row['avg_satisfaction'], row['avg_work_life_balance'], row['avg_income']]
                categories = ['Performans', 'Memnuniyet', 'İş-Yaşam Dengesi', 'Maaş Endeksi']
            else:
                values = [row.get('avg_performance', 0), row.get('avg_satisfaction', 0), 0.5, row.get('avg_income', 0)]
                categories = ['Performans', 'Memnuniyet', 'İş-Yaşam Dengesi', 'Maaş Endeksi']
            
            fig_radar.add_trace(go.Scatterpolar(
                r=values + [values[0]],
                theta=categories + [categories[0]],
                fill='toself',
                name=row['Department']
            ))
        fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 1])), template="plotly_dark", showlegend=True)
        st.plotly_chart(fig_radar, use_container_width=True)
        
    with col_heat:
        st.subheader("Departman ve Performans Dağılımı")
        heat_data = pd.crosstab(df['Department'], df['PerformanceScore'])
        fig_heat = px.imshow(heat_data, labels=dict(x="Performans Puanı", y="Departman", color="Kişi Sayısı"), color_continuous_scale="Viridis")
        fig_heat.update_layout(template="plotly_dark")
        st.plotly_chart(fig_heat, use_container_width=True)
        
    st.subheader("Seçili Departman: En İyi 10 Performans")
    top_performers = dept_df.sort_values(by=['PerformanceScore', 'SatisfactionScore'], ascending=[False, False]).head(10)
    st.dataframe(top_performers[['EmployeeID', 'FirstName', 'LastName', 'JobRole', 'PerformanceScore', 'SatisfactionScore', 'MonthlyIncome']], use_container_width=True)
    
    st.subheader("Departman ve Fazla Mesai Dağılımı")
    overtime_dist = df.groupby(['Department', 'OverTime']).size().reset_index(name='Count')
    fig_bar = px.bar(overtime_dist, x='Department', y='Count', color='OverTime', barmode='stack', color_discrete_map={'Evet': '#F59E0B', 'Hayır': '#6366F1'})
    fig_bar.update_layout(template="plotly_dark")
    st.plotly_chart(fig_bar, use_container_width=True)

except Exception as e:
    st.error(f"Bir hata oluştu: {str(e)}")
