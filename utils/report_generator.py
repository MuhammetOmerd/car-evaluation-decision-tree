import io
import pandas as pd
from fpdf import FPDF
from datetime import datetime
import streamlit as st

class PDFReport(FPDF):
    def header(self):
        self.set_font('helvetica', 'B', 15)
        self.cell(0, 10, 'NexHR - AI Performans Analitigi Raporu', 0, 1, 'C')
        self.set_font('helvetica', 'I', 10)
        self.cell(0, 10, f'Olusturulma Tarihi: {datetime.now().strftime("%Y-%m-%d %H:%M")}', 0, 1, 'C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', 'I', 8)
        self.cell(0, 10, f'Sayfa {self.page_no()}', 0, 0, 'C')

@st.cache_data(show_spinner=False)
def generate_pdf_report(df, kpi):
    """Verilen metriklerle bir PDF raporu uretir ve byte dizisi olarak doner."""
    pdf = PDFReport()
    pdf.add_page()
    
    # KPI Bolumu
    pdf.set_font('helvetica', 'B', 14)
    pdf.cell(0, 10, '1. Genel Performans Gostergeleri (KPI)', 0, 1)
    
    pdf.set_font('helvetica', '', 12)
    pdf.cell(0, 8, f"Toplam Calisan: {kpi['total_employees']}", 0, 1)
    pdf.cell(0, 8, f"Isten Ayrilma Orani: %{kpi['attrition_rate']:.1f}", 0, 1)
    pdf.cell(0, 8, f"Ortalama Performans: {kpi['avg_performance']:.2f} / 5.0", 0, 1)
    pdf.cell(0, 8, f"Ortalama Memnuniyet: {kpi['avg_satisfaction']:.2f} / 5.0", 0, 1)
    pdf.cell(0, 8, f"Ortalama Maas: {kpi['avg_income']:,.0f} TL", 0, 1)
    pdf.cell(0, 8, f"Fazla Mesai Yapanlarin Orani: %{kpi['overtime_rate']:.1f}", 0, 1)
    pdf.ln(10)
    
    # Departman Ozeti
    pdf.set_font('helvetica', 'B', 14)
    pdf.cell(0, 10, '2. Departmanlara Gore Isten Ayrilma', 0, 1)
    pdf.set_font('helvetica', '', 11)
    
    def replace_tr(text):
        tr_map = {'ı':'i', 'İ':'I', 'ş':'s', 'Ş':'S', 'ğ':'g', 'Ğ':'G', 'ü':'u', 'Ü':'U', 'ö':'o', 'Ö':'O', 'ç':'c', 'Ç':'C'}
        for s, r in tr_map.items():
            text = text.replace(s, r)
        return text

    dept_attr = df[df['Attrition'] == 'Evet'].groupby('Department').size().reset_index(name='Ayrilan_Kisi')
    for _, row in dept_attr.iterrows():
        dept_name = replace_tr(str(row['Department']))
        pdf.cell(0, 8, f"- {dept_name} Departmani: {row['Ayrilan_Kisi']} kisi ayrildi.", 0, 1)
        
    pdf.ln(10)
    pdf.set_font('helvetica', 'I', 10)
    pdf.cell(0, 10, 'Bu rapor NexHR Yapay Zeka Sistemi tarafindan otomatik uretilmistir.', 0, 1)
    
    # Byte dizisine cevir
    return bytes(pdf.output())

@st.cache_data(show_spinner=False)
def generate_excel_report(df):
    """DataFrame'i Excel formatinda bellege yazar ve byte dizisi olarak doner."""
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Calisan Verileri')
        
        # Ozet sekmesi
        summary = pd.DataFrame({
            'Metrik': ['Toplam Calisan', 'Ayrilan Sayisi', 'Ortalama Performans'],
            'Deger': [len(df), len(df[df['Attrition'] == 'Evet']), df['PerformanceScore'].mean()]
        })
        summary.to_excel(writer, index=False, sheet_name='Ozet')
        
    processed_data = output.getvalue()
    return processed_data
