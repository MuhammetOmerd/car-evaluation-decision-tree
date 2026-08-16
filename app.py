import streamlit as st
import sys, os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from utils.data_processor import load_data, get_kpi_metrics, get_department_stats

st.set_page_config(page_title='NexHR - AI Performans Analitiği', page_icon='🧠', layout='wide')

COLORS = ['#6366F1', '#EC4899', '#10B981', '#F59E0B', '#3B82F6', '#8B5CF6', '#14B8A6', '#F97316']

st.markdown("""
<style>
    .metric-card {
        background: linear-gradient(135deg, #1e1e2d 0%, #2d2d44 100%);
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border-left: 5px solid #6366F1;
        margin-bottom: 20px;
    }
    .metric-title {
        color: #a0a0b2;
        font-size: 14px;
        font-weight: 600;
        text-transform: uppercase;
    }
    .metric-value {
        color: #ffffff;
        font-size: 28px;
        font-weight: 700;
    }
</style>
""", unsafe_allow_html=True)

st.title("🧠 NexHR - AI Performans Analitiği")
st.markdown("İnsan kaynakları verilerini yapay zeka ile analiz ederek çalışan performansı ve işten ayrılma risklerini tahmin eden akıllı analitik platformu.")

@st.cache_data
def get_data():
    return load_data()

try:
    df = get_data()
    
    kpi = get_kpi_metrics(df)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f'<div class="metric-card"><div class="metric-title">Toplam Çalışan</div><div class="metric-value">{kpi["total_employees"]}</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-card"><div class="metric-title">İşten Ayrılma Oranı</div><div class="metric-value">%{kpi["attrition_rate"]:.1f}</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="metric-card" style="border-left-color: #10B981;"><div class="metric-title">Ort. Performans</div><div class="metric-value">{kpi["avg_performance"]:.2f}</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-card" style="border-left-color: #10B981;"><div class="metric-title">Ort. Maaş</div><div class="metric-value">₺{kpi["avg_income"]:,.0f}</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="metric-card" style="border-left-color: #EC4899;"><div class="metric-title">Ort. Memnuniyet</div><div class="metric-value">{kpi["avg_satisfaction"]:.2f}</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-card" style="border-left-color: #EC4899;"><div class="metric-title">Fazla Mesai Oranı</div><div class="metric-value">%{kpi["overtime_rate"]:.1f}</div></div>', unsafe_allow_html=True)

    dept_stats = get_department_stats(df)
    
    st.subheader("Departman Performans Karşılaştırması")
    fig_dept = px.bar(dept_stats.sort_values('avg_performance', ascending=True).reset_index(), 
                      x='avg_performance', y='Department', orientation='h',
                      color='avg_performance', color_continuous_scale=['#EC4899', '#6366F1'],
                      labels={'avg_performance': 'Ortalama Performans', 'Department': 'Departman'})
    fig_dept.update_layout(height=400, template="plotly_dark", margin=dict(l=0, r=0, t=30, b=0))
    st.plotly_chart(fig_dept, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("İşten Ayrılma Dağılımı")
        attrition_counts = df['Attrition'].value_counts().reset_index()
        attrition_counts.columns = ['Durum', 'Kişi']
        fig_attr = px.pie(attrition_counts, values='Kişi', names='Durum', color='Durum', 
                          color_discrete_map={'Evet': '#EF4444', 'Hayır': '#10B981'}, hole=0)
        fig_attr.update_layout(template="plotly_dark")
        st.plotly_chart(fig_attr, use_container_width=True)
        
    with col2:
        st.subheader("Eğitim Seviyesi Dağılımı")
        edu_counts = df['EducationLevel'].value_counts().reset_index()
        edu_counts.columns = ['Eğitim', 'Kişi']
        fig_edu = px.pie(edu_counts, values='Kişi', names='Eğitim', hole=0.5, color_discrete_sequence=COLORS)
        fig_edu.update_layout(template="plotly_dark")
        st.plotly_chart(fig_edu, use_container_width=True)

    st.subheader("Cinsiyet Dağılımı")
    gender_counts = df['Gender'].value_counts().reset_index()
    gender_counts.columns = ['Cinsiyet', 'Kişi']
    fig_gender = px.bar(gender_counts, x='Cinsiyet', y='Kişi', color='Cinsiyet', 
                        color_discrete_map={'Erkek': '#3B82F6', 'Kadın': '#EC4899'})
    fig_gender.update_layout(template="plotly_dark")
    st.plotly_chart(fig_gender, use_container_width=True)

except Exception as e:
    st.error(f"Veri yüklenirken bir hata oluştu: {str(e)}")

st.markdown("---")
st.markdown("<div style='text-align: center; color: #666;'>© 2026 NexHR Analytics</div>", unsafe_allow_html=True)
