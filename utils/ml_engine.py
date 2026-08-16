"""
Makine öğrenmesi motoru modülü.
"""
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report
from sklearn.cluster import KMeans
from xgboost import XGBClassifier
from prophet import Prophet
import shap

class DataPreprocessor:
    """Veri ön işleme sınıfı."""
    def __init__(self):
        self.label_encoders = {}
        self.scaler = StandardScaler()
        self.feature_names = []
        self.target_encoder = LabelEncoder()
        
    def fit_transform(self, df):
        """Veriyi ön işleme adımlarından geçirir (fit + transform)."""
        df_proc = df.copy()
        
        # Gereksiz sütunları çıkar
        drop_cols = ['EmployeeID', 'FirstName', 'LastName']
        for col in drop_cols:
            if col in df_proc.columns:
                df_proc.drop(col, axis=1, inplace=True)
                
        # Hedef değişkeni ayır
        y = None
        if 'Attrition' in df_proc.columns:
            y = self.target_encoder.fit_transform(df_proc['Attrition'].astype(str))
            df_proc.drop('Attrition', axis=1, inplace=True)
            
        self.feature_names = df_proc.columns.tolist()
        
        # Kategorik sütunları tespit et ve encode et
        categorical_cols = df_proc.select_dtypes(include=['object', 'category']).columns.tolist()
        for col in categorical_cols:
            le = LabelEncoder()
            df_proc[col] = le.fit_transform(df_proc[col].astype(str))
            self.label_encoders[col] = le
        
        # Tüm sütunları sayısala dönüştür
        df_proc = df_proc.apply(pd.to_numeric, errors='coerce').fillna(0)
                
        X = self.scaler.fit_transform(df_proc)
        return X, y
        
    def transform(self, df):
        """Yeni veriyi daha önce fit edilmiş dönüştürücülerle işler."""
        df_proc = df.copy()
        drop_cols = ['EmployeeID', 'FirstName', 'LastName', 'Attrition']
        for col in drop_cols:
            if col in df_proc.columns:
                df_proc.drop(col, axis=1, inplace=True)
                
        for col, le in self.label_encoders.items():
            if col in df_proc.columns:
                df_proc[col] = df_proc[col].astype(str).map(
                    lambda s, _le=le: s if s in _le.classes_ else _le.classes_[0]
                )
                df_proc[col] = le.transform(df_proc[col])
        
        # Tüm sütunları sayısala dönüştür
        df_proc = df_proc[self.feature_names]
        df_proc = df_proc.apply(pd.to_numeric, errors='coerce').fillna(0)
        X = self.scaler.transform(df_proc)
        return X
        
    def get_feature_names(self):
        """Özellik isimlerini döndürür."""
        return self.feature_names


class AttritionPredictor:
    """İşten ayrılma tahmini için XGBoost sınıfı."""
    def __init__(self):
        self.model = XGBClassifier(
            n_estimators=200,
            max_depth=6,
            learning_rate=0.1,
            subsample=0.8,
            colsample_bytree=0.8,
            random_state=42,
            eval_metric='logloss'
        )
        self.feature_names = None
        
    def train(self, X_train, y_train, feature_names=None):
        """Modeli eğitir."""
        self.model.fit(X_train, y_train)
        if feature_names:
            self.feature_names = feature_names
            
    def predict(self, X):
        """Tahmin yapar."""
        return self.model.predict(X)
        
    def predict_proba(self, X):
        """Olasılık tahmini yapar."""
        return self.model.predict_proba(X)
        
    def get_feature_importance(self, feature_names=None):
        """Özellik önem sıralamasını döndürür."""
        if feature_names is not None:
            self.feature_names = feature_names
        if self.feature_names is None:
            return pd.DataFrame()
        importance = self.model.feature_importances_
        return pd.DataFrame({'feature': self.feature_names, 'importance': importance})
        
    def evaluate(self, X_test, y_test):
        """Model performansını değerlendirir."""
        y_pred = self.predict(X_test)
        return {
            'accuracy': accuracy_score(y_test, y_pred),
            'precision': precision_score(y_test, y_pred, zero_division=0),
            'recall': recall_score(y_test, y_pred, zero_division=0),
            'f1_score': f1_score(y_test, y_pred, zero_division=0),
            'confusion_matrix': confusion_matrix(y_test, y_pred).tolist(),
            'classification_report': classification_report(y_test, y_pred, output_dict=True)
        }


class PerformanceForecaster:
    """Departman performans tahmini (Prophet) sınıfı."""
    def __init__(self):
        self.model = None
        
    def prepare_data(self, df, department):
        dept_data = df[df['Department'] == department]
        avg_perf = dept_data['PerformanceScore'].mean()
        
        # Sentetik zaman serisi (son 24 ay)
        dates = pd.date_range(end=pd.Timestamp.today(), periods=24, freq='ME')
        y_values = avg_perf + np.linspace(-0.2, 0.1, 24) + np.random.normal(0, 0.05, 24)
        y_values = np.clip(y_values, 1.0, 5.0)
        
        prophet_df = pd.DataFrame({'ds': dates, 'y': y_values})
        return prophet_df
        
    def forecast(self, df, department, periods=6):
        prophet_df = self.prepare_data(df, department)
        self.model = Prophet(yearly_seasonality=False, weekly_seasonality=False, daily_seasonality=False)
        self.model.fit(prophet_df)
        
        future = self.model.make_future_dataframe(periods=periods, freq='ME')
        forecast = self.model.predict(future)
        return forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(periods)


class EmployeeSegmenter:
    """KMeans ile çalışan segmentasyonu."""
    def __init__(self):
        self.model = None
        
    def segment(self, df, n_clusters=4):
        self.model = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        X = df[['PerformanceScore', 'SatisfactionScore']].values
        labels = self.model.fit_predict(X)
        centers = self.model.cluster_centers_
        return labels, centers


class ExplainableAI:
    """SHAP ile model açıklanabilirliği."""
    def __init__(self, model, feature_names):
        self.model = model
        self.feature_names = feature_names
        self.explainer = shap.TreeExplainer(self.model)
        
    def get_shap_values(self, X):
        return self.explainer.shap_values(X)
        
    def get_summary_data(self, shap_values, X):
        if len(shap_values.shape) == 3:
            mean_abs_shap = np.abs(shap_values).mean(axis=(0, 2))
        else:
            mean_abs_shap = np.abs(shap_values).mean(axis=0)
        return pd.DataFrame({'feature': self.feature_names, 'importance': mean_abs_shap})
        
    def get_individual_explanation(self, shap_values, X, idx):
        if len(shap_values.shape) == 3:
            s_vals = shap_values[idx, :, 1]
        else:
            s_vals = shap_values[idx]
        return pd.DataFrame({
            'feature': self.feature_names,
            'feature_value': X[idx],
            'shap_value': s_vals
        })
