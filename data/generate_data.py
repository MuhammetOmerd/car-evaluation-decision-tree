import sys
import os
import numpy as np
import pandas as pd

sys.stdout.reconfigure(encoding='utf-8')

# Turkish names
FIRST_NAMES_M = [
    "Ahmet", "Mehmet", "Mustafa", "Ali", "Hüseyin", "Hasan", "İbrahim", "İsmail", "Osman", "Halil",
    "Süleyman", "Yusuf", "Ömer", "Emre", "Kemal", "Murat", "Hakan", "Yasin", "Burak", "Kaan",
    "Fatih", "Volkan", "Gökhan", "Ozan", "Serkan", "Cem", "Cenk", "Turan", "Erdem", "Erkan",
    "Uğur", "Tolga", "Barış", "Sinan", "Oğuz", "Cihan", "Eren", "Can", "Kerem", "Efe",
    "Alp", "Berk", "Ege", "Kadir", "Tahir", "Mert", "Okan", "Bora", "Deniz", "Onur"
]
FIRST_NAMES_F = [
    "Ayşe", "Fatma", "Emine", "Hatice", "Zeynep", "Elif", "Meryem", "Şerife", "Zehra", "Sultan",
    "Hanife", "Merve", "Aslı", "Esra", "Büşra", "Cansu", "Ceren", "Özge", "Tuğba", "Pelin",
    "Gizem", "Seda", "Sinem", "Berna", "Eda", "Melis", "Pınar", "Didem", "Burcu", "Duygu",
    "Aylin", "Banu", "Ceyda", "Ebru", "Filiz", "Gamze", "Hande", "İrem", "Jale", "Kübra",
    "Lale", "Mine", "Nazlı", "Oya", "Rüya", "Selin", "Tuğçe", "Umut", "Vildan", "Yasemin"
]
LAST_NAMES = [
    "Yılmaz", "Kaya", "Demir", "Çelik", "Şahin", "Yıldız", "Yıldırım", "Öztürk", "Aydın", "Özdemir",
    "Arslan", "Doğan", "Kılıç", "Aslan", "Çetin", "Kara", "Koç", "Kurt", "Özkan", "Şimşek",
    "Polat", "Öz", "Erdoğan", "Yavuz", "Can", "Acar", "Boyraz", "Avcı", "Güngör", "Şen",
    "Köse", "Aksoy", "Bulut", "Keskinoğlu", "Yücel", "Turan", "Gül", "Özer", "Aktaş", "Çoban",
    "Er", "Tekin", "Gök", "Gökçe", "Sarı", "Taş", "Bozkurt", "Ateş", "Çakır", "Ergin"
]

DEPARTMENTS = {
    "Bilgi Teknolojileri": ["Yazılım Geliştirici", "Veri Analisti", "Sistem Yöneticisi", "DevOps Mühendisi", "IT Destek"],
    "İnsan Kaynakları": ["İK Uzmanı", "İşe Alım Uzmanı", "Eğitim Yöneticisi", "İK İş Ortağı"],
    "Finans": ["Finansal Analist", "Muhasebeci", "Bordro Uzmanı", "Finans Yöneticisi"],
    "Pazarlama": ["Pazarlama Uzmanı", "Dijital Pazarlama Uzmanı", "İçerik Üreticisi", "Pazarlama Müdürü"],
    "Satış": ["Satış Temsilcisi", "Müşteri Temsilcisi", "Satış Yöneticisi", "Bölge Satış Müdürü"],
    "Operasyon": ["Operasyon Uzmanı", "Lojistik Uzmanı", "Operasyon Yöneticisi"],
    "Ar-Ge": ["Araştırmacı", "Ar-Ge Mühendisi", "Ürün Geliştirici", "Ar-Ge Yöneticisi"],
    "Hukuk": ["Avukat", "Hukuk Müşaviri", "Sözleşme Uzmanı"]
}

EDUCATION_LEVELS = ["Lise", "Ön Lisans", "Lisans", "Yüksek Lisans", "Doktora"]

def generate_data(n_records=15000):
    np.random.seed(42)
    
    emp_ids = np.arange(1000, 1000 + n_records)
    genders = np.random.choice(["Erkek", "Kadın"], size=n_records, p=[0.55, 0.45])
    
    first_names = [np.random.choice(FIRST_NAMES_M) if g == "Erkek" else np.random.choice(FIRST_NAMES_F) for g in genders]
    last_names = np.random.choice(LAST_NAMES, size=n_records)
    
    ages = np.random.normal(loc=35, scale=8, size=n_records)
    ages = np.clip(ages, 22, 62).astype(int)
    
    marital_status = np.random.choice(["Bekar", "Evli", "Boşanmış"], size=n_records, p=[0.3, 0.6, 0.1])
    
    depts = np.random.choice(list(DEPARTMENTS.keys()), size=n_records, p=[0.2, 0.05, 0.1, 0.1, 0.2, 0.15, 0.1, 0.1])
    roles = [np.random.choice(DEPARTMENTS[d]) for d in depts]
    
    education_probs = {"Bilgi Teknolojileri": [0.01, 0.05, 0.6, 0.3, 0.04],
                       "İnsan Kaynakları": [0.05, 0.1, 0.6, 0.2, 0.05],
                       "Finans": [0.01, 0.05, 0.7, 0.2, 0.04],
                       "Pazarlama": [0.05, 0.1, 0.6, 0.2, 0.05],
                       "Satış": [0.1, 0.2, 0.6, 0.1, 0.0],
                       "Operasyon": [0.15, 0.25, 0.5, 0.1, 0.0],
                       "Ar-Ge": [0.0, 0.0, 0.3, 0.5, 0.2],
                       "Hukuk": [0.0, 0.0, 0.6, 0.3, 0.1]}
    
    educations = [np.random.choice(EDUCATION_LEVELS, p=education_probs[d]) for d in depts]
    
    max_tenure_for_age = np.maximum(0, ages - 22)
    years_at_company = np.clip(np.random.normal(loc=5, scale=4, size=n_records), 0, max_tenure_for_age).astype(int)
    years_in_current_role = np.clip(np.random.normal(loc=2, scale=2, size=n_records), 0, years_at_company).astype(int)
    
    distance = np.random.lognormal(mean=2, sigma=0.8, size=n_records)
    distance = np.clip(distance, 1, 50).astype(int)
    
    edu_mult = {"Lise": 1.0, "Ön Lisans": 1.2, "Lisans": 1.5, "Yüksek Lisans": 2.0, "Doktora": 2.5}
    dept_mult = {"Bilgi Teknolojileri": 1.4, "İnsan Kaynakları": 1.0, "Finans": 1.3, "Pazarlama": 1.1, "Satış": 1.2, "Operasyon": 1.0, "Ar-Ge": 1.5, "Hukuk": 1.4}
    
    base_income = 10000
    incomes = []
    for i in range(n_records):
        inc = base_income * edu_mult[educations[i]] * dept_mult[depts[i]]
        inc += years_at_company[i] * 1000
        noise = np.random.normal(0, inc * 0.1)
        inc = np.clip(inc + noise, 5000, 80000)
        incomes.append(int(inc))
        
    perf_scores = np.clip(np.random.normal(loc=3.5, scale=0.8, size=n_records), 1.0, 5.0)
    sat_scores = np.clip(np.random.normal(loc=3.2, scale=1.0, size=n_records), 1.0, 5.0)
    wlb_scores = np.clip(np.random.normal(loc=3.0, scale=0.9, size=n_records), 1.0, 5.0)
    
    overtime_prob = 1.0 - (wlb_scores - 1.0) / 4.0
    overtime = np.random.binomial(1, overtime_prob)
    overtime_str = ["Evet" if o == 1 else "Hayır" for o in overtime]
    
    training_hours = np.clip(np.random.normal(loc=20 + perf_scores*5, scale=10), 0, 100).astype(int)
    promotions = np.clip(np.random.poisson(lam=years_at_company / 5.0), 0, 5).astype(int)
    
    attr_probs = []
    for i in range(n_records):
        prob = 0.1 # base
        if sat_scores[i] < 2.5: prob += 0.2
        if wlb_scores[i] < 2.5: prob += 0.15
        if overtime[i] == 1: prob += 0.15
        if incomes[i] < 20000: prob += 0.1
        if years_at_company[i] <= 2: prob += 0.1
        if perf_scores[i] < 2.5: prob += 0.1
        prob = np.clip(prob + np.random.normal(0, 0.05), 0, 0.95)
        attr_probs.append(prob)
        
    attrition = np.random.binomial(1, attr_probs)
    attrition_str = ["Evet" if a == 1 else "Hayır" for a in attrition]
    
    df = pd.DataFrame({
        "EmployeeID": emp_ids,
        "FirstName": first_names,
        "LastName": last_names,
        "Age": ages,
        "Gender": genders,
        "Department": depts,
        "JobRole": roles,
        "EducationLevel": educations,
        "YearsAtCompany": years_at_company,
        "YearsInCurrentRole": years_in_current_role,
        "MonthlyIncome": incomes,
        "PerformanceScore": np.round(perf_scores, 2),
        "SatisfactionScore": np.round(sat_scores, 2),
        "WorkLifeBalance": np.round(wlb_scores, 2),
        "OverTime": overtime_str,
        "TrainingHoursLastYear": training_hours,
        "NumberOfPromotions": promotions,
        "DistanceFromHome": distance,
        "MaritalStatus": marital_status,
        "Attrition": attrition_str
    })
    
    return df

if __name__ == "__main__":
    print("Generating synthetic HR data...")
    df = generate_data(15000)
    
    out_dir = os.path.dirname(os.path.abspath(__file__))
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "hr_employee_data.csv")
    
    df.to_csv(out_path, index=False, encoding='utf-8-sig')
    
    print(f"Data saved to {out_path}")
    print("\n--- Summary Statistics ---")
    print(f"Total records: {len(df)}")
    print(f"Attrition rate: {df['Attrition'].value_counts(normalize=True).get('Evet', 0)*100:.2f}%")
    print("\nAverage scores:")
    print(f"Performance: {df['PerformanceScore'].mean():.2f}")
    print(f"Satisfaction: {df['SatisfactionScore'].mean():.2f}")
    print(f"Work-Life Balance: {df['WorkLifeBalance'].mean():.2f}")
