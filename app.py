from flask import Flask, jsonify, render_template
import pandas as pd
import gspread
import os
import json
from oauth2client.service_account import ServiceAccountCredentials
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Função para carregar as credenciais do ambiente
def get_google_credentials():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds_json = os.getenv("GOOGLE_CREDENTIALS_JSON")
    if not creds_json:
        raise Exception("GOOGLE_CREDENTIALS_JSON não configurado no ambiente.")
    creds_dict = json.loads(creds_json)
    return ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)

# Função para carregar os dados do Google Sheets
def carregar_dados():
    credenciais = get_google_credentials()
    cliente = gspread.authorize(credenciais)
    planilha = cliente.open_by_key("1LyhymqJ8QKezAiR8ZCidyO9w2hKejP7F-IMFlBGyMJ8")
    aba = planilha.worksheet("Espelho")
    dados = aba.get_all_records()
    df = pd.DataFrame(dados)
    return df

@app.route('/api/empreendimentos')
def listar_empreendimentos():
    df = carregar_dados()
    empreendimentos = sorted(df['Empreendimento'].dropna().unique())
    return jsonify(empreendimentos)

@app.route('/api/espelho/<nome>')
def espelho(nome):
    df = carregar_dados()
    df_filtrado = df[df['Empreendimento'] == nome].copy()
    df_filtrado.fillna('', inplace=True)
    resultado = df_filtrado.to_dict(orient='records')
    return jsonify(resultado)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
