
from flask import Flask, render_template, request, redirect
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import csv

app = Flask(__name__)

ficheiro = "datasets/utilizadores.dat"

@app.route("/area_pessoal")
def area_pessoal():
    return render_template("area_pessoal.html")

def guardar_utilizador(username, email, password): 
    # Abre o ficheiro em modo de acrescentar (a = append) 
    f = open(ficheiro, "a", encoding="utf-8") 
    f.write(username + ";" + email + ";" + password + "\n")
    f.close()

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
        
        
fileName='./datasets/imdb_top_250_movies.csv'

with open(fileName, newline='', encoding='utf-8') as csvfile:
        Reade = csv.reader(csvfile, delimiter=',', quotechar='"')
        global Data, header
        header = next(Reade)  # Skip header
        Data = list(Reade) 
        
#  ----------------------------------------------------------
print(header)
#  ----------------------------------------------------------


def filmsByGenreChart(header, Data):
    items = []              # LISTA de generos
    Count = []              # LISTA de contador de filmes para cada genero
    
    
    indexGenre = header.index('Year')
    for film in Data:      # Percorrer todos os filmes (agora 89 filmes)
        genresFilm = film[indexGenre].split(', ')  # Um filme pode ter vários géneros
    
        for genre in genresFilm:    # percorre todos os generos de UM DETERMINADO FILME 
            if genre in items:
                pos=items.index(genre) 
                Count[pos]+= 1
            else:
                items.append(genre)
                Count.append(1)

    print(Count)
    chart1Path = "./static/image/plot1.png"
    plt.figure()

    myExplode = []
    for i in range (len(items)):
        myExplode.append(0.1)

    ypoints = (Count)
    plt.pie(ypoints, 
            labels=items, 
            shadow=True,
            explode = myExplode,
            autopct='%1.1f%%')   # Atributo para evidenciar valores percentuais e respetiva formatação
          

    font1 = {'family':'serif','color':'blue','size':20}
    plt.title("Films by Genre", fontdict= font1, loc = "center")   # loc = left, center, right

   
    plt.tight_layout()
    plt.savefig(chart1Path)
    plt.close()
    return chart1Path

@app.route("/",methods=["GET", "POST"])
def inicio():
    global Data, header
    grafico = filmsByGenreChart(header, Data)
    y=''
    x=''
    for a in header:
        y+=f'<option value="{a}">{a}</option>'
        x+=f'<option value="{a}">{a}</option>'
    return render_template("index.html", grafico=grafico,y=y,x=x)

if __name__ == '__main__':
    app.run(debug=True)
    app.dump()