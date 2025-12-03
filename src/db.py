import gspread
from oauth2client.service_account import ServiceAccountCredentials
import streamlit as st
from datetime import datetime

# Usar credencial do Streamlit Secrets
# O secrets deve conter o JSON inteiro do service account
# Exemplo:
# [gcp]
# creds = { ...json aqui... }
creds_json = st.secrets["gcp"]["creds"]

scope = ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_json, scope)
gc = gspread.authorize(creds)

# ID da planilha (pega da URL)
SHEET_ID = st.secrets["gcp"]["sheet_id"]

sheet = gc.open_by_key(SHEET_ID).sheet1


def save_rating(role, date, rating, comment):
    created_at = datetime.utcnow().isoformat()
    sheet.append_row([role, date, rating, comment, created_at])


def list_ratings():
    rows = sheet.get_all_values()
    if len(rows) <= 1:
        return []
    header = rows[0]
    return [dict(zip(header, row)) for row in rows[1:]]
