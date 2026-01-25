from flask import Flask, render_template, request, redirect, url_for
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import csv
from glob import glob
import shutil

app = Flask(__name__)
ficheiro = "datasets/utilizadores.bin"
arcaive = ""
username =""
adm=False

#Login

def guardar_utilizador(username, email, password):
    linha = f"{username};{email};{password};0\n"
    with open(ficheiro, "ab") as f:  # 'ab' = append binary
        f.write(linha.encode("utf-8"))


def verificar_login(username, password):
    global adm
    if not os.path.exists(ficheiro):
        return False
    
    with open(ficheiro, "rb") as f: # 'rb' = read binary
        for linha in f:
            dados = linha.decode("utf-8").strip().split(";")
            if dados[0] == username and dados[2] == password:
                return True
        if dados[3] == '1':
            adm = True
        else:
            adm = False
        return False


@app.route("/registar", methods=["POST"])
def registar():
    global username
    username = request.form["username"]
    email = request.form["email"]
    password = request.form["password"]
    lista=[]
    with open(ficheiro, "r", encoding="utf-8") as f:
        for linha in f:
            dados = linha.strip().split(";")
            lista+=dados
        if lista.count(username) != 0 or lista.count(email) != 0:
            return "<p>Usuario e/ou email ja cadastrados esolher outro</p><a href='/'><button>voltar</button></a>"
        
        else:
            guardar_utilizador(username, email, password)
            os.mkdir(f'./Users/{username}')
            datasetsList = sorted(glob('datasets/*.csv'))
            for origem in datasetsList:
                escrita = os.path.basename(origem)
                shutil.copy(origem, f'./Users/{username}/{escrita}')
            return redirect("/area_pessoal")


@app.route("/login", methods=["POST"])
def login():
    global username
    username = request.form["username"]
    password = request.form["password"]
    if verificar_login(username, password):
        return redirect("/area_pessoal")
    else:
        return render_template("index.html",)

#Area pessoal
@app.route("/area_pessoal", methods=["GET", "POST"])
def area_pessoal():
    global arcaive,username,adm
    if 'arcaive' not in globals():
        arcaive = ""
    if adm == True:
        datasetsList = sorted(glob(f'./datasets/*.csv'))
        titulo='Modo Adiministrador'
    else:
        datasetsList = sorted(glob(f'./Users/{username}/*.csv'))
        titulo=f'Área do {username}'
    
    escrita = [os.path.basename(nome).replace('.csv', '') for nome in datasetsList]

    atributos = []
    num_linhas=0
    num_atributos = 0

    if request.method == 'POST':
        arcaive = request.form.get('arcaive')

    if arcaive:
        caminho = os.path.join('datasets', f"{arcaive}.csv")

        if os.path.exists(caminho):
            with open(caminho, newline='', encoding='utf-8') as f:
                reader = csv.reader(f, delimiter=",")
                List = list(reader) 

                if len(List) > 0:    
                    header = List[0]

                    for i in header:   
                        atributos.append(i)

            num_atributos = len(atributos)
            num_linhas = len(List)-1

    return render_template("area_pessoal.html",escrita=escrita,arcaive=arcaive,atributos=atributos,num_atributos=num_atributos,num_linhas=num_linhas,titulo=titulo)


#Gráficos
grafico=''
@app.route("/data", methods=["GET", "POST"])
def confirmar():
    global arcaive, grafico,username,adm
    if not arcaive:
        return redirect("/area_pessoal")
    if adm == True:
        fileName = f'./datasets/{arcaive}.csv'
    else:
        fileName = f'./Users/{username}/{arcaive}.csv'
    
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
        w=request.form.get('w')
        h=request.form.get('h')
        grid=request.form.get('grid')
       
        if width != '' :
            width = float(width) 
        if w != '':
            w=int(w)
        if h != '':
            h=int(h)   
        grafico = GenGrafico(header, Data, color,width,w,h,grid)
    if grafico == "":
        return render_template("grafico.html", y=y, x=x)
    else:
        return render_template("grafico.html", grafico=grafico, y=y, x=x)

items = []
Count = []
def GenGrafico(header, Data, color='black', width='',w='',h='',grid=''):
    global Count,items
    items = []
    Count = []

    # Valores por defeito
    if width == '':
        width = 0.8   # largura da barra (menor = mais espaço)
    else:
        width = float(width)

    if w == '':
        w = 6
    else:
        w = float(w)

    if h == '':
        h = 5
    else:
        h = float(h)

    if request.method == 'POST':
        IPy = request.form.get('y')
        IPx = request.form.get('x')
        IPg = request.form.get('category')

        indexGenre = header.index(IPy)

         # Contagem dos itens
        for b in Data:
            lista = b[indexGenre].split(', ')
            for XD in lista:
                if XD in items:
                    pos = items.index(XD)
                    Count[pos] += 1
                else:
                    items.append(XD)
                    Count.append(1)
        
        chart1Path = "./static/image/plot1.png"

        plt.figure(figsize=(w, h))
        font1 = {'family': 'serif', 'color': 'blue', 'size': 20}

        if grid =='on':
            plt.grid()

        # PIZZA
        if IPg == 'pizza':
            explode = [width] * len(items)
            plt.pie(Count, labels=items, shadow=True, explode=explode, autopct='%1.1f%%')
            plt.title(f'{IPy}', fontdict=font1, loc="center")
            plt.savefig(chart1Path)
            plt.close()

        # BARRA VERTICAL
        if IPg == 'bar':
            plt.xlabel(IPy)
            plt.bar(items,Count,
                    color=color,
                    width=width,
                    )

            plt.title(f'{IPy}', fontdict=font1, loc="center")
      
            plt.savefig(chart1Path)
            plt.close()

        # BARRA HORIZONTAL
        if IPg == 'hodBar':
            plt.ylabel(IPy)
            plt.barh(items, 
                     Count,
                     color=color,
                     height=width,
                     )
            plt.title(f'{IPy}', fontdict=font1, loc="center")
      
            plt.savefig(chart1Path)
            plt.close()

        # STAIRS
        if IPg == 'stairs':
            coisa=Count.append(1)
            plt.ylabel(IPy)
            plt.stairs(items, 
                     coisa,
                     color=color,
                     )
            plt.title(f'{IPy}', fontdict=font1, loc="center")
        
            plt.savefig(chart1Path)
            plt.close()

        # HISTOGRAMA
        if IPg == 'hist':
            coisa=Count.append(1)
            plt.xlabel(IPy)
            plt.hist(items, 
                     coisa,
                     color=color,
                     )
            plt.title(f'{IPy}', fontdict=font1, loc="center")
            
            plt.savefig(chart1Path)
            plt.close()

        return chart1Path
    
    return ""


@app.route("/", methods=["GET", "POST"])
def inicio():
    global adm
    adm = False
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
    global adm,username
    if 'file' not in request.files:
        return redirect(url_for('area_pessoal'))
    
    file = request.files['file']
    

    if file.filename == '':
        return redirect(url_for('area_pessoal'))
    
    if file and allowed_file(file.filename):
        if adm == True:
            filepath = f'./datasets/{file.filename}'
            file.save(filepath)
            lista = (sorted(glob('./Users/*')))
            for dd in lista:
                cc=dd+f'/{file.filename}'
                print('cc ',cc)
                file.save(cc)  
            
        else:    
            filepath = f'./Users/{username}/{file.filename}'
            file.save(filepath)

    return redirect(url_for('area_pessoal'))


#Remover Arquivos

def remover_dataset(nome):
    global username,adm
    if adm == True:
        caminho = f'./datasets/{nome}.csv'
        if os.path.exists(caminho):
            os.remove(caminho)
        lista = (sorted(glob('./Users/*')))
        for dd in lista:
            cc=dd+f'/{nome}.csv'
            print('cc ',cc)
            if os.path.exists(cc):
                os.remove(cc)
        return True  
    else:    
        caminho = f'./Users/{username}/{nome}.csv'
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

