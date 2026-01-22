from flask import Flask, render_template, request, redirect, url_for
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import csv
from glob import glob

app = Flask(__name__)
ficheiro = "datasets/utilizadores.dat"
arcaive = ""


#Login

def guardar_utilizador(username, email, password):
    with open(ficheiro, "a", encoding="utf-8") as f:
        f.write(username + ";" + email + ";" + password + "\n")


def verificar_login(username, password):
    if not os.path.exists(ficheiro):
        return False
    with open(ficheiro, "r", encoding="utf-8") as f:
        for linha in f:
            dados = linha.strip().split(";")
            if dados[0] == username and dados[2] == password:
                return True
    return False


@app.route("/registar", methods=["POST"])
def registar():
    username = request.form["username"]
    email = request.form["email"]
    password = request.form["password"]
    guardar_utilizador(username, email, password)
    return redirect("/area_pessoal")


@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    if verificar_login(username, password):
        return redirect("/area_pessoal")
    else:
        return render_template("index.html", msg="Username ou password incorretos.")


#Gráficos
grafico=''
@app.route("/data", methods=["GET", "POST"])
def confirmar():
    global arcaive, grafico
    if not arcaive:
        return redirect("/area_pessoal")
    fileName = f"./datasets/{arcaive}.csv"
    if not os.path.exists(fileName):
        return redirect("/area_pessoal")
    y = ""
    x = ""
    with open(fileName, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        global Data, header
        header = next(reader)
        Data = list(reader)
    for a in header:
        y += f'<option value="{a}">{a}</option>'
        x += f'<option value="{a}">{a}</option>'
    if request.method == 'POST':
        color=request.form.get('color')
        width=(request.form.get('width'))
        if width != '':
            width = float(width)    
        grafico = GenGrafico(header, Data, color,width)
    if grafico == "":
        return render_template("grafico.html", y=y, x=x)
    else:
        return render_template("grafico.html", grafico=grafico, y=y, x=x)

items = []
Count = []
def GenGrafico(header, Data, color='black', width='0'):
    global Count,items
    if request.method == 'POST':
        IPy = request.form.get('y')
        IPx = request.form.get('x')
        IPg = request.form.get('category')
        indexGenre = header.index(IPy)
        for b in Data:
            lista = b[indexGenre].split(', ')
            for XD in lista:
                if XD in items:
                    pos = items.index(XD)
                    Count[pos] += 1
                else:
                    items.append(XD)
                    Count.append(1)
        print(items)
        print(Count)
        chart1Path = "./static/image/plot1.png"
        plt.figure()
        font1 = {'family': 'serif', 'color': 'blue', 'size': 20}

        if IPg == 'pizza':
            explode = [0.1] * len(items)
            plt.pie(Count, labels=items, shadow=True, explode=explode, autopct='%1.1f%%')
            plt.title(f'{IPy}', fontdict=font1, loc="center")
            plt.savefig(chart1Path)
            plt.close()

        if IPg == 'bar':
            plt.xlabel(IPy)
            plt.bar(items,Count,
                    color=color,
                    width=width,
                    )

            plt.title(f'{IPy}', fontdict=font1, loc="center")
            plt.tight_layout()
            plt.savefig(chart1Path)
            plt.close()

        if IPg == 'hodBar':
            plt.ylabel(IPy)
            plt.barh(items, 
                     Count,
                     color=color,
                     height=width,
                     )
            plt.title(f'{IPy}', fontdict=font1, loc="center")
            plt.tight_layout()
            plt.savefig(chart1Path)
            plt.close()

        if IPg == 'stairs':
            coisa=Count.append(1)
            plt.ylabel(IPy)
            plt.stairs(items, 
                     coisa,
                     color=color,
                     )
            plt.title(f'{IPy}', fontdict=font1, loc="center")
            plt.tight_layout()
            plt.savefig(chart1Path)
            plt.close()
        return chart1Path
    return ""


@app.route("/", methods=["GET", "POST"])
def inicio():
    return render_template("index.html")


#Upload de Arquivos

UPLOAD_FOLDER = 'datasets'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'csv'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(url_for('area_pessoal'))
    
    file = request.files['file']

    if file.filename == '':
        return redirect(url_for('area_pessoal'))
    
    if file and allowed_file(file.filename):
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

    return redirect(url_for('area_pessoal'))


#Remover Arquivos

@app.route("/area_pessoal", methods=["GET", "POST"])
def area_pessoal():
    global arcaive
    datasetsList = sorted(glob('datasets/*.csv'))
    escrita = [os.path.basename(nome).replace('.csv', '') for nome in datasetsList]
    if request.method == 'POST':
        arcaive = request.form.get('arcaive')
    return render_template("area_pessoal.html", escrita=escrita, arcaive=arcaive)

def remover_dataset(nome):
    caminho = os.path.join('datasets', f"{nome}.csv")
    if os.path.exists(caminho):
        os.remove(caminho)
        return True
    return False

@app.route("/remover", methods=["POST"])
def remover():
    nome = request.form.get("arcaive")
    if nome:
        remover_dataset(nome)
    return redirect("/area_pessoal")


if __name__ == '__main__':
    app.run(debug=True)

