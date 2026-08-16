# 🧠 NexHR – Yapay Zeka Destekli Departman & Çalışan Performans Analiz Sistemi

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30%2B-FF4B4B?logo=streamlit&logoColor=white)
![XGBoost](https://img.shields.io/badge/XGBoost-ML-green?logo=xgboost)
![SHAP](https://img.shields.io/badge/SHAP-Explainable_AI-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)

> **NexHR**, organizasyonların çalışan ve departman performansını **yapay zeka destekli analitik, tahminsel modeller ve etkileşimli panolar** kullanarak takip etmesini, analiz etmesini ve optimize etmesini sağlayan modern bir İK (İnsan Kaynakları) analitiği platformudur.

---

## 📋 İçindekiler

* [Genel Bakış](#-genel-bakış)
* [Neden NexHR?](#-neden-nexhr)
* [Temel Özellikler](#-temel-özellikler)
* [Teknoloji Yığını](#️-teknoloji-yığını)
* [Proje Yapısı](#-proje-yapısı)
* [Kurulum ve Çalıştırma](#-kurulum-ve-çalıştırma)
* [Ekran Görüntüleri](#-ekran-görüntüleri)
* [Makine Öğrenmesi Modelleri](#-makine-öğrenmesi-modelleri)
* [Yol Haritası](#️-yol-haritası)
* [Lisans](#-lisans)
* [Geliştirici](#-geliştirici)

---

## 🎯 Genel Bakış

**NexHR**, geleneksel, subjektif ve reaktif İK süreçlerini **objektif, veri odaklı ve prediktif (tahminsel) içgörülerle** değiştirmek üzere tasarlanmış, kurumsal seviyede bir performans yönetim platformudur.

Performans verilerini merkezileştirir, trendleri ve riskleri tespit etmek için makine öğrenmesi uygular ve her şeyi sezgisel, etkileşimli panolar aracılığıyla sunar.

---

## ❓ Neden NexHR?

Geleneksel sistemlerin karşılaştığı sorunlar:

❌ Subjektif değerlendirmeler ve yönetici önyargısı  
❌ Bağlantısız veri kaynakları  
❌ Performans sorunlarına geç tepki  
❌ Pahalı, hantal kurumsal araçlar  
❌ Kullanıcıların kaçındığı kötü arayüzler  

**NexHR bunları şöyle çözer:**

✅ Ölçülebilir KPI'lar ve objektif analitik  
✅ Birleşik performans veri platformu  
✅ Prediktif AI modelleri (tahminleme ve risk tespiti)  
✅ Açık kaynak ve KOBİ dostu  
✅ Temiz, modern ve etkileşimli kullanıcı deneyimi  

---

## ✨ Temel Özellikler

### 📊 Çekirdek Analitik
* Gerçek zamanlı etkileşimli panolar (Dashboard)
* Departman bazlı KPI takibi
* Trend görselleştirme ve karşılaştırmalar
* 9-Box Yetenek Matrisi (Performans × Potansiyel)
* Çalışan profil kartları ve detaylı analiz

### 🤖 AI / ML Yetenekleri
* **İşten Ayrılma (Attrition) Tahmini** – XGBoost Classifier
* **Performans Tahminlemesi** – Facebook Prophet (Zaman Serisi)
* **Çalışan Segmentasyonu** – K-Means Kümeleme
* **Açıklanabilir Yapay Zeka (Explainable AI)** – SHAP Değerleri
* AI destekli risk puanlama sistemi

### 📈 Gelişmiş Özellikler
* Plotly ile yüksek kaliteli etkileşimli grafikler
* Departman radar grafikleri ve ısı haritaları
* Özellik önem sıralaması ve SHAP waterfall grafikleri
* Filtreleme ve arama yetenekleri
* Tek komutla çalışan altyapı (Docker gerektirmez)

---

## 🛠️ Teknoloji Yığını

| Katman | Teknoloji |
|---|---|
| **Frontend / Dashboard** | Streamlit, Plotly |
| **Makine Öğrenmesi** | XGBoost, Prophet, scikit-learn, SHAP |
| **Veri İşleme** | Pandas, NumPy |
| **Görselleştirme** | Plotly Express, Plotly Graph Objects |
| **Programlama Dili** | Python 3.10+ |

---

## 📁 Proje Yapısı

```
nexhr-ai-performance-analytics/
├── app.py                              # Ana sayfa ve Streamlit giriş noktası
├── pages/
│   ├── 1_👥_Calisan_Analizi.py         # Çalışan bazlı detaylı analiz
│   ├── 2_🏢_Departman_Analitigi.py     # Departman karşılaştırma ve analitiği
│   ├── 3_🤖_AI_Tahminleri.py          # XGBoost ile işten ayrılma tahmini
│   └── 4_🧠_Aciklanabilir_AI.py       # SHAP ile AI karar açıklamaları
├── data/
│   ├── generate_data.py                # Sentetik veri seti üretici
│   └── hr_employee_data.csv            # 15.000 satırlık çalışan verisi
├── utils/
│   ├── ml_engine.py                    # ML model motoru (XGBoost, Prophet, SHAP)
│   └── data_processor.py              # Veri işleme yardımcı fonksiyonları
├── models/                             # Eğitilmiş model dosyaları (otomatik oluşur)
├── requirements.txt                    # Python bağımlılıkları
├── .gitignore
└── README.md
```

---

## 🚀 Kurulum ve Çalıştırma

### Ön Gereksinimler
* Python 3.10 veya üzeri
* pip (Python paket yöneticisi)

### Adım Adım Kurulum

```bash
# 1. Projeyi klonlayın
git clone https://github.com/MuhammetOmerd/nexhr-ai-performance-analytics.git
cd nexhr-ai-performance-analytics

# 2. Bağımlılıkları kurun
pip install -r requirements.txt

# 3. Veri setini üretin (ilk çalıştırmada gereklidir)
python data/generate_data.py

# 4. Uygulamayı başlatın
streamlit run app.py
```

Uygulama otomatik olarak tarayıcınızda açılacaktır: **http://localhost:8501**

---

## 🤖 Makine Öğrenmesi Modelleri

| Model | Algoritma | Amaç |
|---|---|---|
| İşten Ayrılma Tahmini | XGBoost Classifier | Hangi çalışanların ayrılma riski taşıdığını tahmin eder |
| Performans Tahminlemesi | Facebook Prophet | Gelecek dönem performans trendlerini öngörür |
| Çalışan Segmentasyonu | K-Means Kümeleme | Benzer profildeki çalışanları gruplar |
| Açıklanabilir AI | SHAP Values | AI kararlarının nedenlerini açıklar |

---

## 🛣️ Yol Haritası

- [x] Etkileşimli Dashboard
- [x] Çalışan & Departman Analitiği
- [x] XGBoost ile İşten Ayrılma Tahmini
- [x] SHAP ile Açıklanabilir AI
- [x] 9-Box Yetenek Matrisi
- [ ] Bildirim sistemi
- [ ] Gerçek zamanlı veri akışı (WebSockets)
- [ ] Mobil uyumlu arayüz
- [ ] PDF/Excel rapor dışa aktarma

---

## 📄 Lisans

MIT License

---

## 👨‍💻 Geliştirici

Bu proje, veri bilimi ve yapay zeka yeteneklerini sergilemek amacıyla **MuhammetOmerd** tarafından baştan sona tasarlanıp geliştirilmiştir.

Sorularınız mı var? Bir **Issue** açın! 🚀
