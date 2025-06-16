from flask import Flask, jsonify, render_template
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

app = Flask(__name__)

# Autenticação com a API do Google Sheets
escopo = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credenciais = ServiceAccountCredentials.from_json_keyfile_name("credenciais.json", escopo)
cliente = gspread.authorize(credenciais)

# Nome da planilha e da aba
NOME_PLANILHA = "Base_Revenda"  # pode ser o nome completo visível no Google Sheets
NOME_ABA = "Espelho"            # ou "Base" ou o nome que você usa

def carregar_dados():
    planilha = cliente.open(NOME_PLANILHA)
    aba = planilha.worksheet(NOME_ABA)
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
