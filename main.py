import os
import requests
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

ZAPI_INSTANCE = os.getenv("ZAPI_INSTANCE")
ZAPI_TOKEN = os.getenv("ZAPI_TOKEN")
ZAPI_CLIENT_TOKEN = os.getenv("ZAPI_CLIENT_TOKEN")

def get_contacts():
    try:
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        response = supabase.table('pessoas').select('*').limit(3).execute()
        return response.data
    except Exception as e:
        print(f"Erro ao buscar contatos: {e}")
        return []

def send_message(phone, name):
    url = f"https://api.z-api.io/instances/{ZAPI_INSTANCE}/token/{ZAPI_TOKEN}/send-text"
    
    headers = {
        "Client-Token": ZAPI_CLIENT_TOKEN,
        "Content-Type": "application/json"
    }
    
    message = f"Olá, {name} tudo bem com você?"
    
    payload = {
        "phone": phone,
        "message": message
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        print(f"Mensagem enviada para {name}")
        return True
    except Exception as e:
        print(f"Erro ao enviar para {name}: {e}")
        return False

def main():
    if not all([SUPABASE_URL, SUPABASE_KEY, ZAPI_INSTANCE, ZAPI_TOKEN, ZAPI_CLIENT_TOKEN]):
        print("Variaveis de ambiente nao configuradas")
        return
        
    contacts = get_contacts()
    
    if not contacts:
        print("Nenhum contato encontrado")
        return
        
    for contact in contacts:
        name = contact.get('nome')
        phone = contact.get('numero')
        
        if name and phone:
            send_message(phone, name)

if __name__ == "__main__":
    main()
