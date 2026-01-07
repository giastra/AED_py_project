
from flask import Flask, render_template
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import csv

app = Flask(__name__)







fileName='./datasets/imdb_top_250_movies.csv'

with open(fileName, newline='', encoding='utf-8') as csvfile:
        filmsReader = csv.reader(csvfile, delimiter=',', quotechar='"')
        global Data, header
        header = next(filmsReader)  # Skip header
        Data = list(filmsReader) 
        
#  ----------------------------------------------------------
print(header )
    
#  ----------------------------------------------------------


def filmsByGenreChart(header, Data):
    genreItems = []              # LISTA de generos
    genreCount = []              # LISTA de contador de filmes para cada genero
    
    
    indexGenre = header.index('Year')
    for film in Data:      # Percorrer todos os filmes (agora 89 filmes)
        genresFilm = film[indexGenre].split(', ')  # Um filme pode ter vários géneros
    
        for genre in genresFilm:    # percorre todos os generos de UM DETERMINADO FILME 
            if genre in genreItems:
                pos=genreItems.index(genre) 
                genreCount[pos]+= 1
            else:
                genreItems.append(genre)
                genreCount.append(1)

    print(genreCount)
    chart1Path = "./static/image/plot1.png"
    plt.figure()

    myExplode = []
    for i in range (len(genreItems)):
        myExplode.append(0.1)

    ypoints = (genreCount)
    plt.pie(ypoints, 
            labels=genreItems, 
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
    return render_template("index.html", grafico=grafico)

if __name__ == '__main__':
    app.run(debug=True)
    app.dump()