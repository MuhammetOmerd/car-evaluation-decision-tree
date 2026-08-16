<div align="center">
  <img src="https://img.icons8.com/color/150/000000/brain.png" alt="NexHR Logo"/>
  <h1>NexHR - AI Performans Analitiği (SaaS)</h1>
  <p><strong>İnsan Kaynakları verilerinizi makine öğrenmesi ile analiz edin, yetenekleri keşfedin ve riskleri önceden tahmin edin.</strong></p>

  <a href="https://muhammetomer-nexhr.streamlit.app" target="_blank">
    <img src="https://img.shields.io/badge/CANLI_DEMO_İÇİN_TIKLAYIN-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Canlı Demo" />
  </a>
</div>

<br>

## 🚀 Proje Hakkında

**NexHR**, modern şirketlerin veri odaklı kararlar almasını sağlayan, tamamen bulut tabanlı bir İK Asistanı ve Analitik Platformudur. Çalışan performans verilerini işleyerek kimlerin işten ayrılma riski taşıdığını saniyeler içinde analiz eder. 

Geleneksel raporlamanın aksine **NexHR**, Supabase altyapısıyla güvenli bir "Multi-Tenant" (Çoklu Müşteri) SaaS deneyimi sunar. Şirketler kendi kurumsal markalarını sisteme tanımlayabilir ve kendilerine özel analiz raporları oluşturabilirler.

## ✨ Öne Çıkan Özellikler

- **🔐 Güvenli Bulut Altyapısı (Supabase):** JWT tabanlı tam yetkilendirme, güvenli kayıt ve şifre sıfırlama işlemleri.
- **🏢 Kurumsal Özelleştirme (White-Label):** Sisteme giriş yapan müşteriler, raporları ve analiz ekranlarını kendi şirket isimleriyle özelleştirebilirler.
- **🧠 Yapay Zeka & Makine Öğrenmesi:** Çalışan verileri Scikit-Learn (Decision Tree) modeli ile analiz edilerek ayrılma ihtimali yüksek yetenekler tespit edilir.
- **📈 Anında Raporlama (PDF & Excel):** Tek tıkla yönetim kuruluna sunulmaya hazır, formatlı ve logolu İK raporları oluşturulur.
- **🔍 Açıklanabilir AI (SHAP):** Yapay zekanın "bu çalışan neden ayrılacak?" kararını hangi verilere (maaş, memnuniyet vb.) dayanarak verdiğini şeffafça açıklar.

## 🛠️ Kullanılan Teknolojiler

- **Frontend:** Streamlit, Plotly, HTML/CSS
- **Backend & Veritabanı:** Python, Supabase (PostgreSQL)
- **Yapay Zeka:** Pandas, Scikit-Learn, SHAP
- **Raporlama:** FPDF2, OpenPyXL

## 💻 Yerel Kurulum (Geliştiriciler İçin)

Projeyi kendi bilgisayarınızda çalıştırmak isterseniz:

```bash
# 1. Repoyu bilgisayarınıza indirin
git clone https://github.com/MuhammetOmerd/-nexhr-ai-performance-analytics.git
cd -nexhr-ai-performance-analytics

# 2. Gerekli kütüphaneleri kurun
pip install -r requirements.txt

# 3. .streamlit/secrets.toml dosyası oluşturun ve Supabase bilgilerinizi ekleyin
# SUPABASE_URL = "https://..."
# SUPABASE_KEY = "eyJ..."

# 4. Uygulamayı başlatın
streamlit run app.py
```

<hr>
<div align="center">
  <p>💡 <b>Muhammet Ömer</b> tarafından tasarlandı ve geliştirildi.</p>
</div>
