
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
def filmsByGenreChart(header, Data):
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


def confirmar():
    arcaive = request.form.get('arcaive')
    if arcaive == 'fs':
        fileName='./datasets/fantasy_series.csv'
    if arcaive == 'IMDB250':
        fileName='./datasets/imdb_top_250_movies.csv'
    if arcaive == 'IMDBVG':
        fileName='./datasets/imdb-videogames.csv'
    else:
        fileName='./datasets/imdb_top_250_movies.csv'
    return fileName

@app.route("/",methods=["GET", "POST"])
def inicio():
    global Data, header
    fileName=confirmar()   
    print('file name ',fileName) 
    with open(fileName, newline='', encoding='utf-8') as csvfile:
        Reade = csv.reader(csvfile, delimiter=',', quotechar='"')
        global Data, header
        header = next(Reade)  # Skip header
        Data = list(Reade) 
    
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