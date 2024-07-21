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

@app.route("/", methods = ["GET", "POST"])
def index():
    
    
    form: Type[FlaskForm] = ShortenerForm()
    if form.validate_on_submit():
        
        origin = request.origin.replace("https://", "").replace("http://", "").split("/")[0]
        url = form.url_encurtar.data
        check_already_shortened = Encurtados.query.filter(Encurtados.url_normal == url).first()
        
        if check_already_shortened:
            
            session["message"] = "This URL has already been shortened"
            session["url"] = f"https://{origin}/{check_already_shortened.seed}"
            flash(f'Url Já encurtada!, {url}' , "error")
            return redirect(url_for("index"))   
            
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
    
    user = request.json.get("username", None)
    password = request.json.get("password", None)
    
    if user and password:
        
        usuario_logado = Users.query.filter(Users.username == user).first()
        if usuario_logado:
            checkpw = usuario_logado.converte_senha(password)
            if checkpw:
                
                expires = timedelta(hours=2)
                access_token = create_access_token(identity=user, expires_delta=expires)
                return jsonify(access_token=access_token)
            
    return jsonify({"error": "require auth"}), 401

@app.route("/encurtar_url", methods = ["POST"])
@jwt_required()
def encurtar():
    
    ## Pega a url a ser encurtada
    url = request.json.get("url_encurtar", None)
    
    ## 
    check_already_shortened = Encurtados.query.filter(Encurtados.url_normal == url).first()
    
    if check_already_shortened:
        return jsonify({"error": "Url already shortened!"}), 401
    
    if url:
        
        new_seed = generate_id()
        gen_seed = Encurtados(
                url_normal = url,
                seed = new_seed)
        
        db.session.add(gen_seed)
        db.session.commit()
        
        return jsonify({"success": f' Your url is http://{request.host}/{new_seed}'})
        
    return jsonify({"success": "200"}), 200
        
@app.route("/encurtado/<seed>", methods = ["GET"])
@jwt_required()
def encurtado(seed: str):
    
    return jsonify({"success": "200"}), 200

@app.route("/<seed>", methods = ["GET"])
def ir_encurtado(seed: str):
    
    url_normal = Encurtados.query.filter(Encurtados.seed == seed).first()
    Encurtados.url_normal
    
    if url_normal:
    
        return redirect(url_normal.url_normal), 301
    
    return jsonify({"error": "Url not found"}), 401