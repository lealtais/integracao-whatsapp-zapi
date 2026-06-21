# Integracao Supabase Z-API

Script para envio de mensagens via Z-API buscando contatos no Supabase.

## Requisitos
- Python 3.8+

## Como rodar
1. Instale as dependencias:
   ```bash
   pip install -r requirements.txt
   ```
2. Configure o arquivo `.env` com as variaveis:
   - SUPABASE_URL
   - SUPABASE_KEY
   - ZAPI_INSTANCE
   - ZAPI_TOKEN
   - ZAPI_CLIENT_TOKEN

3. O Supabase deve conter uma tabela chamada `pessoas` com as colunas `id`, `nome` e `numero`. O campo de numero precisa estar no formato internacional.

4. Execute o script:
   ```bash
   python main.py
   ```
