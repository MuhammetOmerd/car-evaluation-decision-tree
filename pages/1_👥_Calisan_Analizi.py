import streamlit as st
import sys, os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.data_processor import load_data, filter_employees

st.set_page_config(page_title='Çalışan Analizi - NexHR', page_icon='👥', layout='wide')

if not st.session_state.get('authenticated', False):
    st.warning("🔒 Lütfen ana sayfadan giriş yapın.")
    st.stop()

COLORS = ['#6366F1', '#EC4899', '#10B981', '#F59E0B', '#3B82F6', '#8B5CF6', '#14B8A6', '#F97316']

st.markdown("""
<style>
    .emp-card {
        background: linear-gradient(135deg, #2d2d44 0%, #1e1e2d 100%);
        border-radius: 8px;
        padding: 15px;
        border-left: 4px solid #F59E0B;
        margin-top: 10px;
    }
</style>
""", unsafe_allow_html=True)

st.title("👥 Çalışan Analizi")

@st.cache_data
def get_data():
    return load_data()

try:
    df = get_data()
    
    st.sidebar.header("Filtreler")
    dept_options = ['Tümü'] + list(df['Department'].unique())
    selected_dept = st.sidebar.selectbox("Departman", dept_options)
    
    gender_options = ['Tümü'] + list(df['Gender'].unique())
    selected_gender = st.sidebar.selectbox("Cinsiyet", gender_options)
    
    edu_options = ['Tümü'] + list(df['EducationLevel'].unique())
    selected_edu = st.sidebar.selectbox("Eğitim Seviyesi", edu_options)
    
    dept_filter = None if selected_dept == 'Tümü' else selected_dept
    gender_filter = None if selected_gender == 'Tümü' else selected_gender
    edu_filter = None if selected_edu == 'Tümü' else selected_edu
    
    filtered_df = filter_employees(df, dept_filter, gender_filter, edu_filter)
    
    st.subheader(f"Çalışan Listesi ({len(filtered_df)} kişi)")
    search_query = st.text_input("Çalışan Ara (İsim veya Soyisim):")
    
    if search_query:
        display_df = filtered_df[filtered_df['FirstName'].str.contains(search_query, case=False, na=False) | 
                                 filtered_df['LastName'].str.contains(search_query, case=False, na=False)]
    else:
        display_df = filtered_df
        
    st.dataframe(display_df[['EmployeeID', 'FirstName', 'LastName', 'Department', 'JobRole', 'PerformanceScore', 'SatisfactionScore', 'MonthlyIncome']], use_container_width=True)
    
    if not display_df.empty:
        with st.expander("Seçili Çalışan Detayları"):
            selected_emp = st.selectbox("Çalışan Seçin", display_df['EmployeeID'].tolist(), format_func=lambda x: f"{x} - {display_df[display_df['EmployeeID']==x]['FirstName'].values[0]} {display_df[display_df['EmployeeID']==x]['LastName'].values[0]}")
            emp_data = display_df[display_df['EmployeeID'] == selected_emp].iloc[0]
            
            st.markdown(f"""
            <div class="emp-card">
                <h3>{emp_data['FirstName']} {emp_data['LastName']}</h3>
                <p><strong>Rol:</strong> {emp_data['JobRole']} | <strong>Departman:</strong> {emp_data['Department']}</p>
                <p><strong>Maaş:</strong> ₺{emp_data['MonthlyIncome']:,} | <strong>Şirketteki Yılı:</strong> {emp_data['YearsAtCompany']}</p>
                <p><strong>Performans Puanı:</strong> {emp_data['PerformanceScore']} | <strong>Memnuniyet Puanı:</strong> {emp_data['SatisfactionScore']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Departmana Göre Yaş Dağılımı")
        fig_age = px.histogram(filtered_df, x="Age", color="Department", marginal="box", color_discrete_sequence=COLORS)
        fig_age.update_layout(template="plotly_dark")
        st.plotly_chart(fig_age, use_container_width=True)
        
    with col2:
        st.subheader("Performans ve Maaş İlişkisi")
        fig_inc = px.scatter(filtered_df, x="PerformanceScore", y="MonthlyIncome", color="Department", size="YearsAtCompany", hover_name="FirstName", color_discrete_sequence=COLORS)
        fig_inc.update_layout(template="plotly_dark")
        st.plotly_chart(fig_inc, use_container_width=True)
        
    col3, col4 = st.columns(2)
    with col3:
        st.subheader("Şirketteki Yıl ve Memnuniyet")
        fig_bubble = px.scatter(filtered_df, x="YearsAtCompany", y="SatisfactionScore", color="Attrition", size="MonthlyIncome", hover_name="FirstName", color_discrete_map={'Evet': '#EF4444', 'Hayır': '#10B981'})
        fig_bubble.update_layout(template="plotly_dark")
        st.plotly_chart(fig_bubble, use_container_width=True)
        
    with col4:
        st.subheader("Performans Puanı Dağılımı")
        fig_violin = px.violin(filtered_df, y="PerformanceScore", x="Department", color="Department", box=True, color_discrete_sequence=COLORS)
        fig_violin.update_layout(template="plotly_dark")
        st.plotly_chart(fig_violin, use_container_width=True)

except Exception as e:
    st.error(f"Bir hata oluştu: {str(e)}")
