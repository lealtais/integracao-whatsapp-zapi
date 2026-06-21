import os
import re
import logging
import requests
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
ZAPI_INSTANCE = os.getenv("ZAPI_INSTANCE")
ZAPI_TOKEN = os.getenv("ZAPI_TOKEN")
ZAPI_CLIENT_TOKEN = os.getenv("ZAPI_CLIENT_TOKEN")


def get_contacts():
    logger.info("Buscando contatos no Supabase...")
    try:
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        response = supabase.table('pessoas').select('*').limit(3).execute()
        contatos = response.data
        logger.info(f"{len(contatos)} contato(s) encontrado(s)")
        return contatos
    except Exception as e:
        logger.error(f"Erro ao buscar contatos: {e}")
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
        logger.info(f"Mensagem enviada com sucesso para {name} ({phone})")
        return True
    except Exception as e:
        logger.error(f"Erro ao enviar mensagem para {name} ({phone}): {e}")
        return False


def main():
    logger.info("Iniciando script de envio de mensagens")

    if not all([SUPABASE_URL, SUPABASE_KEY, ZAPI_INSTANCE, ZAPI_TOKEN, ZAPI_CLIENT_TOKEN]):
        logger.error("Variáveis de ambiente não configuradas")
        return

    contacts = get_contacts()
    if not contacts:
        logger.warning("Nenhum contato encontrado")
        return

    enviados = 0
    falhas = 0

    for contact in contacts:
        name = contact.get('nome')
        phone = contact.get('numero')

        if not name or not phone:
            logger.warning(f"Contato com dados incompletos, ignorado: {contact}")
            continue

        name = str(name).strip()
        phone = re.sub(r'\D', '', str(phone))

        if not phone:
            logger.warning(f"Telefone inválido para {name}, ignorado")
            continue

        if send_message(phone, name):
            enviados += 1
        else:
            falhas += 1

    logger.info(f"Execução finalizada: {enviados} enviada(s), {falhas} falha(s)")


if __name__ == "__main__":
    main()
