# flask microframeworks necessita de auxiliares para um site completo,
# para algoritimos
# exemplo de site usando 
from flask import Flask, render_template, request, redirect
import os

app = Flask(__name__)

ficheiro = "datasets/utilizadores.dat"

@app.route("/area_pessoal")
def area_pessoal():
    return render_template("area_pessoal.html")


@app.route("/")
def inicio():
    return render_template("index.html")

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


@app.route('/blog')
def blog():
    return'bem vindo ao blog'

if __name__ == '__main__':
    app.run(debug=True)



