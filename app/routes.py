from flask import jsonify, request, redirect, render_template, flash, url_for, session
from flask_jwt_extended import jwt_required 
from flask_jwt_extended import create_access_token

from flask_wtf import FlaskForm
from typing import Type

from app import app
from app import db
from app.models import Users, Encurtados
from app.misc.gen_seed import generate_id
from app.forms import ShortenerForm

from datetime import timedelta

message = ""
url = ""

def without_http(orig: str) -> str:
    
    return orig.replace("https://", "").replace("http://", "").split("/")[0]

def url_conventer(url: str) -> str:
    
    ## Corrige a URL caso ela não possua "https://"
    
    if "http://" in url:
        url = url.replace("http://", "https://")
        
    if not "https://" in url:
        url = "https://" + url
        
    return url

@app.route("/", methods = ["GET", "POST"])
def index():
    
    
    form: Type[FlaskForm] = ShortenerForm()
    if form.validate_on_submit():
        
        ## Formata o Url de origem
        
        ## Fiz dessa forma pois tem casos como o Reverse Proxy
        ## que se usar o "request.host" ele fica com o endereço do host (127.0.0.1). 
        ## com o origin não ocorre isso, o lado ruim é que fica com o http/https
        ## no texto, coisa que não ocorre no "request.host"
        
        origin = without_http(request.origin)
        url = url_conventer(form.url_encurtar.data)
        ## Verifica se a url que o usuário está tentando encurtar já se encontra no servidor
        
        check_already_shortened = Encurtados.query.filter(Encurtados.url_normal == url).first()
        
        if check_already_shortened:
            
            ## Caso esteja, ele retorna a url encurtada
            session["message"] = "This URL has already been shortened"
            session["url"] = f"https://{origin}/{check_already_shortened.seed}"
            flash(f'Url Já encurtada!, {url}' , "error")
            return redirect(url_for("index"))   
        
        ## Caso não esteja, ele gera uma seed para essa url e adiciona no database
        new_seed = generate_id()
        gen_seed = Encurtados(url_normal = url, seed = new_seed)
        
        db.session.add(gen_seed)
        db.session.commit()
        
        session["message"] = "Your URL has been shortened successfully!"
        session["url"] = f"https://{origin}/{new_seed}"
        flash(category = "success", message = f'Your url is {url}')
        
        return redirect(url_for("index"))        
    
    return render_template("index.html", form = form, message = session.get("message", ""), url = session.get("url", ""))

@app.route("/login", methods = ["POST"])
def login():
    
    ## Sistema de autenticação JWT
    user = request.json.get("username", None)
    password = request.json.get("password", None)
    
    ## Verifica se no request.json tem esses dois parâmetros
    if user and password:
        
        ## Verifica se o usuário informado está no database
        usuario_logado = Users.query.filter(Users.username == user).first()
        if usuario_logado:
            
            ## Verifica a senha
            checkpw = usuario_logado.converte_senha(password)
            if checkpw:
                
                ## Define o tempo de expiração do Token JWT e retorna ele
                expires = timedelta(hours=2)
                access_token = create_access_token(identity=user, expires_delta=expires)
                return jsonify(access_token=access_token), 200
            
    return jsonify({"error": "require auth"}), 401

@app.route("/encurtar_url", methods = ["POST"])
# Descomente o decorator para habilitar a autenticação JWT
# @jwt_required()
def encurtar():
    
    ## Pega a url a ser encurtada
    url = request.json.get("url", None)
    
    ## Verifica se o request não está em branco
    if url:
        
        ## Formata o Url de origem
            
        ## Fiz dessa forma pois tem casos como o Reverse Proxy
        ## que se usar o "request.host" ele fica com o endereço do host (127.0.0.1). 
        ## com o origin não ocorre isso, o lado ruim é que fica com o http/https
        ## no texto, coisa que não ocorre no "request.host"
        
        origin = without_http(request.origin)
            
        ## Verifica se a url que o usuário está tentando encurtar já se encontra no servidor
        check_already_shortened = Encurtados.query.filter(Encurtados.url_normal == url).first()
        
        if check_already_shortened:
            
            ## Caso esteja, ele retorna a url encurtada
            return jsonify({"error": "Url already shortened!",
                            "url": f"https://{origin}/{check_already_shortened.seed}"}), 401
        

        url = url_conventer(url)
        ## Caso não esteja, ele gera uma seed para essa url e adiciona no database
        new_seed = generate_id()
        gen_seed = Encurtados(
                url_normal = url,
                seed = new_seed)
        
        db.session.add(gen_seed)
        db.session.commit()
        
        ## Retorna o sucesso
        return jsonify({"success": f' Your url is https://{origin}/{new_seed}'}), 200

    return jsonify({"error": "Requiere 'URL' parameter"}), 401

@app.route("/<seed>", methods = ["GET"])
def ir_encurtado(seed: str):
    
    ## Verifica se a seed está cadastrada no database
    url_normal = Encurtados.query.filter(Encurtados.seed == seed).first()
    Encurtados.url_normal
    
    if url_normal:
        
        url = url_normal.url_normal
        ## Se cadastrada, redireciona o user para a url que foi encurtada
        return redirect(url), 301
    
    ## Caso não esteja, retorna erro
    return jsonify({"error": "Url not found"}), 404
