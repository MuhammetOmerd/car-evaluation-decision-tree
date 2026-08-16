"""
Veri işleme yardımcı fonksiyonları.
"""
import os
import pandas as pd
import numpy as np

import streamlit as st

def load_data():
    """Verisetini yükler. Özel veri varsa onu, yoksa varsayılanı döner."""
    if 'custom_df' in st.session_state and st.session_state['custom_df'] is not None:
        return st.session_state['custom_df']
        
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(project_root, 'data', 'hr_employee_data.csv')
    return pd.read_csv(file_path)

def get_department_stats(df):
    """Departman bazlı istatistikleri döner."""
    stats = df.groupby('Department').agg(
        total_employees=('EmployeeID', 'count'),
        avg_performance=('PerformanceScore', 'mean'),
        avg_satisfaction=('SatisfactionScore', 'mean'),
        avg_income=('MonthlyIncome', 'mean'),
        attrition_count=('Attrition', lambda x: (x == 'Evet').sum())
    ).reset_index()
    stats['attrition_rate'] = stats['attrition_count'] / stats['total_employees']
    return stats.to_dict('records')

def get_employee_profile(df, employee_id):
    """Belirli bir çalışanın profil verisini sözlük olarak döner."""
    emp_df = df[df['EmployeeID'] == employee_id]
    if emp_df.empty:
        return None
    return emp_df.iloc[0].to_dict()

def calculate_risk_score(attrition_prob, satisfaction, performance):
    """İşten ayrılma riski skoru (0-100) hesaplar."""
    sat_factor = (5.0 - satisfaction) / 4.0
    perf_factor = (5.0 - performance) / 4.0
    
    score = (attrition_prob * 0.6 + sat_factor * 0.3 + perf_factor * 0.1) * 100
    return np.clip(score, 0, 100)

def get_kpi_metrics(df):
    """Genel KPI metriklerini döner."""
    total_emp = len(df)
    avg_perf = df['PerformanceScore'].mean()
    avg_sat = df['SatisfactionScore'].mean()
    attr_rate = (df['Attrition'] == 'Evet').mean()
    avg_inc = df['MonthlyIncome'].mean()
    overtime_rate = (df['OverTime'] == 'Evet').mean()
    
    return {
        'total_employees': total_emp,
        'avg_performance': round(avg_perf, 2),
        'avg_satisfaction': round(avg_sat, 2),
        'attrition_rate': round(attr_rate, 4),
        'avg_income': round(avg_inc, 2),
        'overtime_rate': round(overtime_rate, 4)
    }

def filter_employees(df, department=None, gender=None, education=None):
    """Filtrelenmiş çalışan verisini döner."""
    filtered = df.copy()
    if department:
        filtered = filtered[filtered['Department'] == department]
    if gender:
        filtered = filtered[filtered['Gender'] == gender]
    if education:
        filtered = filtered[filtered['EducationLevel'] == education]
    return filtered
