from flask import Flask, render_template, jsonify
import pandas as pd
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

EXCEL_PATH = 'Base_Revenda.xlsx'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/empreendimentos')
def listar_empreendimentos():
    try:
        df = pd.read_excel(EXCEL_PATH)
        empreendimentos = sorted(df['Empreendimento'].dropna().unique().tolist())
        return jsonify(empreendimentos)
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@app.route('/api/espelho/<nome_empreendimento>')
def espelho(nome_empreendimento):
    try:
        df = pd.read_excel(EXCEL_PATH)
        filtro = df[df['Empreendimento'] == nome_empreendimento]
        return jsonify(filtro.fillna('').to_dict(orient='records'))
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
