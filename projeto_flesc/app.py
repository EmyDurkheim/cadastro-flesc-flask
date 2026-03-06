from flask import Flask, render_template, request
import webbrowser
import json 
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PASTA_UPLOADS = os.path.join(BASE_DIR, 'static', 'uploads')
ARQUIVOS_JSON = os.path.join(BASE_DIR, 'dados_flesc.json')

if not os.path.exists(PASTA_UPLOADS):
    os.makedirs(PASTA_UPLOADS)
    
def ler_dados():
    if os.path.exists(ARQUIVOS_JSON):
        with open(ARQUIVOS_JSON, 'r', encoding='utf-8') as f:

            try:
                return json.load(f)
            except:
                return []
    return []

@app.route('/') 

def index():
    return render_template('index.html')

@app.route('/cadastrar', methods=['POST'])

def cadastrar():
    codigo = request.form.get('codigo')
    nome = request.form.get('nome')
    foto = request.files.get('foto')

    if foto:
        #Salva o arquivo na pasta static/uploads
        nome_arquivo = foto.filename
        caminho_completo = os.path.join(PASTA_UPLOADS, nome_arquivo)
        foto.save(caminho_completo)
        
        #Guardamos apenas o nome do arquivo ou o caminho relativo simples
        novo_registro = {
            "codigo": codigo,
            "nome": nome,
            "caminho_imagem": nome_arquivo #guardar so o nome facilita a busca
        }
        
        dados = ler_dados()
        dados.append(novo_registro)

        with open(ARQUIVOS_JSON, 'w', encoding='utf-8') as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)
            
            
    return render_template('index.html', msg="Cadastrado com sucesso!")
    
@app.route('/buscar', methods=['POST'])

def buscar():
    codigo_procurado = request.form.get('codigo_busca')
    dados = ler_dados()
    
    aluno_encontrado = None
    for aluno in dados:
        if aluno['codigo'] == codigo_procurado:
            aluno_encontrado = aluno
            break

    if aluno_encontrado:
        return render_template('index.html', aluno=aluno_encontrado)
    else:
        return render_template('index.html', erro="Aluno não encontrado!")
#roda o app
if __name__ == "__main__":
    app.run(debug=True)