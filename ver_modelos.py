import google.generativeai as genai
import os

# --- COLE SUA API KEY AQUI ---
api_key = "AIzaSyAyXvWLTSrdQxY_UNE9VFRmVzEFJEzEGAo" 

genai.configure(api_key=api_key)

print(f"Consultando modelos disponíveis para a chave...")

try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"✅ NOME CORRETO: {m.name}")
except Exception as e:
    print(f"❌ Erro: {e}")