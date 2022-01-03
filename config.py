import os
from dotenv import load_dotenv

# load from .env
load_dotenv()

TOKEN = os.getenv("TOKEN")
ADMINS_IDS = ['925441528921477150']
PROGRESS_USER_MSG_COUNT = 20

# db
user = 'postgres'
password = 'N9w/C#Q[\qYr<}#d8+IA'
host = 'db.wmvhrqvpxibjlcanbdlm.supabase.co'
db_name = 'postgres'
