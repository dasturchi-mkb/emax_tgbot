import os
from dotenv import load_dotenv, get_key


db_host = get_key('.env', 'DB_HOST')
db_port = get_key('.env', 'DB_PORT')
db_user = get_key('.env', 'DB_USER')
db_pass = get_key('.env', 'DB_PASSWORD')
db_name = get_key('.env', 'DB_NAME')

BOT_TOKEN = get_key('.env', 'BOT_TOKEN')
print(BOT_TOKEN)
