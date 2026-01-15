
from flask import Flask, render_template, request, redirect
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import csv
from glob import glob
app = Flask(__name__)

ficheiro = "datasets/utilizadores.dat"



# registrar utilizador
def guardar_utilizador(username, email, password): 
    f = open(ficheiro, "a", encoding="utf-8") 
    f.write(username + ";" + email + ";" + password + "\n")
    f.close()


# login
def verificar_login(username, password):
    # Se o ficheiro não existir, não há utilizadores
    if not os.path.exists(ficheiro):
        return False
    
    f = open(ficheiro, "r", encoding="utf-8")

    for linha in f:
        dados = linha.strip().split(";") 

        # dados[0] = username
        # dados[2] = password
        if dados[0] == username and dados[2] == password:
            f.close()
            return True

    f.close()
    return False


# pg de registro
@app.route("/registar", methods=["POST"])
def registar():
    username = request.form["username"]
    email = request.form["email"]
    password = request.form["password"]

    guardar_utilizador(username, email, password)

    return redirect("/area_pessoal")


# pg de login
@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    if verificar_login(username, password):
        return redirect("/area_pessoal")
    else:
        return render_template("index.html", msg="Username ou password incorretos.")
    


# escolher o data set
@app.route("/data", methods=["GET", "POST"])
def confirmar():
    global arcaive
    print(arcaive , 'tipo de arquivo no data')
    fileName=f'./datasets/{arcaive}.csv'
    print(fileName)
    y=''
    x=''
    with open(fileName, newline='', encoding='utf-8') as csvfile:
        Reade = csv.reader(csvfile, delimiter=',', quotechar='"')
        global Data, header
        header = next(Reade)  # Skip header
        Data = list(Reade) 
        csvfile.close()
    for a in header:
        y+=f'<option value="{a}">{a}</option>'
        x+=f'<option value="{a}">{a}</option>'
    
    grafico = GenGrafico(header, Data)
    if grafico == '':
        return render_template("grafico.html", y=y,x=x)
    else:
        return render_template("grafico.html", grafico=grafico,y=y,x=x)
    

# gerar grafico
def GenGrafico(header, Data):
    items = []              
    Count = []              
    
    if request.method=='POST':
        IPy = request.form.get('y')
        IPx = request.form.get('x')
        IPg = request.form.get('category')
        print('y ', IPy)
        print('x', IPx)
        print('g ', IPg)
        indexGenre = header.index(IPy)
        for b in Data:      
            lista = b[indexGenre].split(', ')  
    
            for XD in lista: 
                if XD in items:
                    pos=items.index(XD) 
                    Count[pos]+= 1
                else:
                    items.append(XD)
                    Count.append(1)
        print(Count)
        chart1Path = "./static/image/plot1.png"
        plt.figure()
        font1 = {'family':'serif','color':'blue','size':20}
        if IPg == 'pizza':
            myExplode = []
            for i in range (len(items)):
                myExplode.append(0.1)

            ypoints = (Count)
            
            plt.pie(ypoints, 
                    labels=items, 
                    shadow=True,
                    explode = myExplode,
                    autopct='%1.1f%%')   # Atributo para evidenciar valores percentuais e respetiva formatação
                
            plt.title(f'{IPy}', fontdict= font1, loc = "center")   # loc = left, center, right
            plt.savefig(chart1Path)
            plt.close()

        if IPg == 'bar':
            plt.xlabel(IPy)
            plt.bar(items,Count)
            plt.title(f'{IPy}', fontdict= font1, loc = "center")
            plt.tight_layout()
            plt.savefig(chart1Path)
            plt.close()

        if IPg == 'hodBar':
            plt.ylabel(IPy)
            plt.barh(items,Count)
            plt.title(f'{IPy}', fontdict= font1, loc = "center")
            plt.tight_layout()
            plt.savefig(chart1Path)
            plt.close()
        return chart1Path


# Tela inicial
@app.route("/",methods=["GET", "POST"])
def inicio():
    
    return render_template("index.html")


# area pessoal
arcaive=''
@app.route("/area_pessoal",methods=["GET", "POST"])
def area_pessoal():
   escrita=''
   datasetsList = sorted(glob(r'./datasets/*.csv'))

   print(datasetsList)

   for nome in datasetsList:
     nome=nome.split('\\')
     nome=nome[1].split('.')
     escrita+=f'<option value="{nome[0]}">{nome[0]}</option>'

   if request.method=='POST': 
        print(request.method)
        global arcaive
        
        arcaive = request.form.get('arcaive')
        print('acquivo : ',arcaive)

   return render_template("area_pessoal.html",escrita=escrita,arcaive=arcaive)


# uploude de arquivos
UPLOAD_FOLDER = 'datasets'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# Extensões permitidas
ALLOWED_EXTENSIONS = {'csv'}
def allowed_file(filename):
    """Verifica se o arquivo tem uma extensão permitida."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# o local para baixar o arquivo
@app.route('/upload', methods=['POST'])
def upload_file():
    voltar="<form action='/area_pessoal' method='get'><button>voltar</button></form>"
    if 'file' not in request.files:
        return f"Nenhum arquivo enviado{voltar}"

    file = request.files['file']

    if file.filename == '':
        return f"Nenhum arquivo selecionado{voltar}"

    if file and allowed_file(file.filename):
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        return f"Arquivo '{file.filename}' salvo com sucesso em {UPLOAD_FOLDER}! {voltar}"
    else:
        return f"Tipo de arquivo não permitido{voltar}"


if __name__ == '__main__':
    app.run(debug=True)
    app.dump()