import os
from supabase import create_client

url = "https://jemzpxepzcfppuryttxb.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImplbXpweGVwemNmcHB1cnl0dHhiIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjM4MjQxMTUsImV4cCI6MjAzOTM5MjkxNX0.AFIPKBLCLKFFz-ttzg_GnEWP3wz1f7fiEHmGd3aFMo4"

print("Testing URL:", url)
print("Testing Key:", key)

try:
    supabase = create_client(url, key)
    res = supabase.auth.sign_up({"email": "test@example.com", "password": "TestPassword123."})
    print("SUCCESS:", res)
except Exception as e:
    print("ERROR:", str(e))
