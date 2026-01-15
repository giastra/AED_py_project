from flask import Flask, request, render_template_string
import os

app = Flask(__name__)

# Pasta onde os arquivos serão salvos
UPLOAD_FOLDER = 'datasets'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Extensões permitidas
ALLOWED_EXTENSIONS = {'txt', 'csv'}

def allowed_file(filename):
    """Verifica se o arquivo tem uma extensão permitida."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Página inicial com formulário de upload
@app.route('/')
def index():
    return render_template_string('''
        <!doctype html>
        <html>
        <head><title>Selecionar Arquivo</title></head>
        <body>
            <h1>Selecione um arquivo para enviar</h1>
            <form method="POST" action="/upload" enctype="multipart/form-data">
                <input type="file" name="file" required>
                <input type="submit" value="Enviar">
            </form>
        </body>
        </html>
    ''')

# Rota para processar o upload
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "Nenhum arquivo enviado", 400

    file = request.files['file']

    if file.filename == '':
        return "Nenhum arquivo selecionado", 400

    if file and allowed_file(file.filename):
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        return f"Arquivo '{file.filename}' salvo com sucesso em {UPLOAD_FOLDER}!"
    else:
        return "Tipo de arquivo não permitido", 400

if __name__ == '__main__':
    app.run(debug=True)
