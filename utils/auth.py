import streamlit as st
from supabase import create_client, Client

def has_supabase_credentials():
    """Secrets icinde Supabase URL ve KEY olup olmadigini kontrol eder."""
    try:
        if "SUPABASE_URL" in st.secrets and "SUPABASE_KEY" in st.secrets:
            return True
        return False
    except FileNotFoundError:
        return False
    except Exception:
        return False

def init_supabase() -> Client:
    """Supabase istemcisini baslatir."""
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

def sign_up(email, password):
    """Yeni kullanici kaydi olusturur."""
    supabase = init_supabase()
    return supabase.auth.sign_up({"email": email, "password": password})

def sign_in(email, password):
    """Kullanici girisi yapar."""
    supabase = init_supabase()
    return supabase.auth.sign_in_with_password({"email": email, "password": password})

def reset_password(email):
    """Sifre sifirlama maili gonderir."""
    supabase = init_supabase()
    return supabase.auth.reset_password_email(email)

def sign_out():
    """Oturumu kapatir."""
    supabase = init_supabase()
    return supabase.auth.sign_out()
