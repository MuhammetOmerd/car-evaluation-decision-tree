import streamlit as st
import sys, os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from utils.data_processor import load_data, get_kpi_metrics, get_department_stats
from utils.report_generator import generate_pdf_report, generate_excel_report
from utils.auth import has_supabase_credentials, sign_up, sign_in, reset_password

st.set_page_config(page_title='NexHR - AI Performans Analitiği', page_icon='🧠', layout='wide')

# --- 1. LOGIN (KIMLIK DOGRULAMA) SISTEMI ---
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

if not has_supabase_credentials():
    st.markdown("<h2 style='text-align: center;'>⚠️ Veritabanı Kurulumu Gerekli</h2>", unsafe_allow_html=True)
    st.info("Bu uygulamayı ticari bir SaaS ürünü olarak kullanabilmeniz için ücretsiz bir Supabase veritabanına bağlamalısınız.")
    st.markdown("### Nasıl Yapılır?")
    st.markdown("1. [Supabase](https://supabase.com/)'e gidin ve ücretsiz kayıt olun.")
    st.markdown("2. Yeni bir proje oluşturun.")
    st.markdown("3. Proje ayarlarından (Settings > API) **Project URL** ve **anon public KEY** değerlerini kopyalayın.")
    st.markdown("4. Streamlit Cloud'daki uygulamanızın ayarlarına (App Settings > Secrets) girin ve şu formatta yapıştırın:")
    st.code("SUPABASE_URL = \"buraya_url_gelecek\"\nSUPABASE_KEY = \"buraya_key_gelecek\"")
    st.markdown("5. Kaydettikten sonra uygulama otomatik olarak Gerçek Kayıt Ol/Giriş Yap ekranına dönecektir.")
    st.stop()

if not st.session_state['authenticated']:
    if not st.session_state.get('show_login', False):
        st.markdown("<h1 style='text-align: center; font-size: 3.5rem; margin-top: 40px;'>Geleceğin İK Yönetimi: <span style='color: #EC4899;'>NexHR</span></h1>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; font-weight: normal; color: #a0a0b2;'>Yapay Zeka ile şirketinizin yeteneklerini keşfedin, riskleri önceden tahmin edin.</h3>", unsafe_allow_html=True)
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        with col1:
            st.info("🧠 **AI Destekli Analiz**\n\nİşten ayrılma risklerini ve performans metriklerini makine öğrenmesi ile önceden tahmin edin.")
        with col2:
            st.success("📊 **Dinamik Raporlama**\n\nŞirket verilerinizi anında görselleştirin ve yönetim kuruluna sunulmaya hazır PDF'ler indirin.")
        with col3:
            st.warning("🏢 **Kurumsal Özelleştirme**\n\nKendi şirket adınızla ve verilerinizle (White-label) sistemi tamamen size özel kullanın.")
            
        st.markdown("<br><br>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns([1,1,1])
        with c2:
            if st.button("🚀 Sisteme Giriş Yap / Ücretsiz Dene", use_container_width=True, type="primary"):
                st.session_state['show_login'] = True
                st.rerun()
        st.stop()
    else:
        st.markdown("<br>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns([1,2,1])
        with c2:
            if st.button("⬅️ Vitrine Geri Dön"):
                st.session_state['show_login'] = False
                st.rerun()
                
        st.markdown("<h2 style='text-align: center;'>🔒 NexHR SaaS Platformu</h2>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            tab1, tab2, tab3 = st.tabs(["Giriş Yap", "Kayıt Ol", "Şifremi Unuttum"])
            
            with tab1:
                with st.form("login_form"):
                    email = st.text_input("E-posta Adresi")
                    password = st.text_input("Şifre", type="password")
                    submit = st.form_submit_button("Giriş Yap", use_container_width=True)
                    if submit:
                        try:
                            res = sign_in(email, password)
                            st.session_state['authenticated'] = True
                            st.session_state['user_email'] = email
                            st.success("Giriş başarılı! Yönlendiriliyorsunuz...")
                            st.rerun()
                        except Exception as e:
                            st.error("Kullanıcı adı veya şifre hatalı! (Veya E-postanızı henüz onaylamadınız)")
                            
            with tab2:
                with st.form("register_form"):
                    new_email = st.text_input("E-posta Adresi (Geçerli bir adres girin)")
                    new_password = st.text_input("Şifre (En az 6 karakter)", type="password")
                    submit_reg = st.form_submit_button("Kayıt Ol", use_container_width=True)
                    if submit_reg:
                        try:
                            res = sign_up(new_email, new_password)
                            st.success("Kayıt başarılı! Lütfen E-postanıza gelen onay linkine tıklayın.")
                            st.info("Not: Spam (Gereksiz) kutusunu kontrol etmeyi unutmayın.")
                        except Exception as e:
                            st.error(f"Kayıt sırasında hata oluştu: {str(e)}")
                            
            with tab3:
                with st.form("reset_form"):
                    reset_email = st.text_input("Şifrenizi sıfırlamak için E-posta adresinizi girin")
                    submit_reset = st.form_submit_button("Şifre Sıfırlama Bağlantısı Gönder", use_container_width=True)
                    if submit_reset:
                        try:
                            reset_password(reset_email)
                            st.success("Şifre sıfırlama bağlantısı E-posta adresinize gönderildi!")
                        except Exception as e:
                            st.error("Bir hata oluştu, lütfen e-posta adresinizi kontrol edin.")
        st.stop()

# --- GÜVENLİ ALAN ---
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

company = st.session_state.get('company_name', 'NexHR')
st.title(f"🧠 {company} - AI Performans Analitiği")
st.markdown("İnsan kaynakları verilerini yapay zeka ile analiz ederek çalışan performansı ve işten ayrılma risklerini tahmin eden akıllı analitik platformu.")

# --- 2. DOSYA YUKLEME (FILE UPLOAD) SİSTEMİ ---
with st.sidebar:
    st.header("⚙️ Ayarlar & Veri")
    if 'user_email' in st.session_state:
        st.caption(f"👤 {st.session_state['user_email']}")
        
    company_name = st.text_input("🏢 Şirket Adınız (Örn: Koç Holding)", value=st.session_state.get('company_name', 'NexHR'))
    st.session_state['company_name'] = company_name
    st.markdown("---")
    
    st.markdown("Kendi şirket verinizi yükleyin.")
    uploaded_file = st.file_uploader("Excel veya CSV Yükle", type=['csv', 'xlsx'])
    
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.csv'):
                custom_df = pd.read_csv(uploaded_file)
            else:
                custom_df = pd.read_excel(uploaded_file)
            st.session_state['custom_df'] = custom_df
            st.success("Özel veri başarıyla yüklendi!")
        except Exception as e:
            st.error(f"Dosya okuma hatası: {e}")
            
    if st.button("Orijinal Veriye Dön", use_container_width=True):
        if 'custom_df' in st.session_state:
            del st.session_state['custom_df']
            st.rerun()

    st.markdown("---")
    if st.button("Çıkış Yap", type="secondary", use_container_width=True):
        st.session_state['authenticated'] = False
        if 'user_email' in st.session_state:
            del st.session_state['user_email']
        st.rerun()

@st.cache_data(ttl=60) # Cache süresi verip özel verinin güncellenmesini sağla
def get_cached_data():
    return load_data()

try:
    # Veriyi session state veya dosyadan al (data_processor icinde yazili)
    df = load_data() 
    
    kpi = get_kpi_metrics(df)
    
    # --- 3. RAPOR İNDİRME ---
    st.sidebar.markdown("---")
    st.sidebar.header("📥 Raporlar")
    
    pdf_data = generate_pdf_report(df, kpi, company_name=st.session_state.get('company_name', 'NexHR'))
    st.sidebar.download_button(
        label="📄 PDF Özeti İndir",
        data=pdf_data,
        file_name="NexHR_Raporu.pdf",
        mime="application/pdf",
        use_container_width=True
    )
    
    excel_data = generate_excel_report(df)
    st.sidebar.download_button(
        label="📊 Detaylı Excel İndir",
        data=excel_data,
        file_name="NexHR_Veriler.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True
    )

    # --- KPI KARTLARI ---
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f'<div class="metric-card"><div class="metric-title">Toplam Çalışan</div><div class="metric-value">{kpi["total_employees"]}</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-card"><div class="metric-title">İşten Ayrılma Oranı</div><div class="metric-value">%{kpi["attrition_rate"]*100:.1f}</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="metric-card" style="border-left-color: #10B981;"><div class="metric-title">Ort. Performans</div><div class="metric-value">{kpi["avg_performance"]:.2f}</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-card" style="border-left-color: #10B981;"><div class="metric-title">Ort. Maaş</div><div class="metric-value">₺{kpi["avg_income"]:,.0f}</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="metric-card" style="border-left-color: #EC4899;"><div class="metric-title">Ort. Memnuniyet</div><div class="metric-value">{kpi["avg_satisfaction"]:.2f}</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-card" style="border-left-color: #EC4899;"><div class="metric-title">Fazla Mesai Oranı</div><div class="metric-value">%{kpi["overtime_rate"]*100:.1f}</div></div>', unsafe_allow_html=True)

    dept_stats = pd.DataFrame(get_department_stats(df))
    
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
st.markdown(f"<div style='text-align: center; color: #666;'>© 2026 {company} Analytics Powered by NexHR</div>", unsafe_allow_html=True)
