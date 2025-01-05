from datetime import timedelta

from typing import Type

from flask import current_app as app
from flask import (
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for,
    Blueprint,
)
from flask_jwt_extended import create_access_token
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm

from .forms import ShortenerForm
from .misc.gen_seed import generate_id
from .models import Encurtados, Users


short = Blueprint("short", __name__)

"""
This module defines the routes for the URL shortener application.

Routes:
    - /: Handles the index route for the URL shortener application.
    - /login: Handles user login and JWT authentication.
    - /encurtar_url: Shortens a given URL and returns the shortened version.
    - /<seed>: Redirects to the original URL based on the provided shortened URL seed.

Functions:
    - without_http(orig: str) -> str: Removes the "http://" or "https://" prefix from a URL.
    - url_conventer(url: str) -> str: Converts a given URL to use "https://" if it does not already.
    - index(): Handles the index route for the URL shortener application.
    - login(): Handles user login and JWT authentication.
    - encurtar(): Shortens a given URL and returns the shortened version.
    - ir_encurtado(seed: str): Redirects to the original URL based on the provided shortened URL seed.

"""


message = ""
url = ""


def without_http(orig: str) -> str:

    return orig.replace("https://", "").replace("http://", "").split("/")[0]


def url_conventer(url: str) -> str:
    """
    Converts a given URL to use "https://" if it does not already.

    This function checks if the input URL contains "http://". If it does,
    it replaces "http://" with "https://". If the URL does not contain
    "https://", it prepends "https://" to the URL.

    Args:
        url (str): The URL to be converted.

    Returns:
        str: The converted URL with "https://".
    """

    # Corrige a URL caso ela não possua "https://"

    if "http://" in url:
        url = url.replace("http://", "https://")

    if "https://" not in url:
        url = "https://" + url

    return url


@short.route("/", methods=["GET", "POST"])
def index():
    """
    Handles the index route for the URL shortener application.

    This function processes both GET and POST requests. On a GET request, it renders the index page with a form.
    On a POST request, it validates the form submission, processes the URL shortening, and handles the following cases:
    - If the URL has already been shortened, it retrieves the shortened URL and displays a message.
    - If the URL has not been shortened, it generates a new seed, stores it in the database, and displays the shortened URL.

    Returns:
        Response: The rendered template for the index page with the form and any messages or shortened URLs.
    """

    db: SQLAlchemy = app.extensions["sqlalchemy"]
    form: Type[FlaskForm] = ShortenerForm()

    if form.validate_on_submit():

        # Formata o Url de origem

        # Fiz dessa forma pois tem casos como o Reverse Proxy
        # que se usar o "request.host" ele fica com o endereço do host (127.0.0.1).
        # com o origin não ocorre isso, o lado ruim é que fica com o http/https
        # no texto, coisa que não ocorre no "request.host"

        origin = without_http(request.origin)
        url = url_conventer(form.url_encurtar.data)
        # Verifica se a url que o usuário está tentando encurtar já se encontra no servidor

        check_already_shortened = Encurtados.query.filter(
            Encurtados.url_normal == url
        ).first()

        # Adicionei um if para colocar "http://" no caso de testes em localhost
        url_prefix = f"http://{origin}"

        if ":" in origin:
            port_origin = origin.split(":")[1]

        if origin != f"127.0.0.1:{port_origin}":
            url_prefix = url_prefix.replace("http://", "https://")

        if check_already_shortened:

            # Caso esteja, ele retorna a url encurtada
            session["message"] = "Esta url já foi encurtada!"

            session["url"] = f"{url_prefix}/{check_already_shortened.seed}"

            flash(f"Url Já encurtada!, {url}", "error")
            return redirect(url_for("short.index"))

        # Caso não esteja, ele gera uma seed para essa url e adiciona no database
        new_seed = generate_id()
        gen_seed = Encurtados(url_normal=url, seed=new_seed)

        db.session.add(gen_seed)
        db.session.commit()

        session["message"] = "URL encurtada com sucesso!"
        session["url"] = f"{url_prefix}/{new_seed}"

        flash(category="success", message=f"Sua url é {url}")

        return redirect(url_for("short.index"))

    return render_template(
        "index.html",
        form=form,
        message=session.get("message", ""),
        url=session.get("url", ""),
    )


@short.route("/login", methods=["POST"])
def login():
    """
    Handles user login and JWT authentication.
    This function retrieves the username and password from the request JSON,
    verifies the credentials against the database, and generates a JWT token
    if the authentication is successful.
    Returns:
        Response: A JSON response containing the JWT token and a 200 status code
                  if authentication is successful.
                  A JSON response with an error message and a 401 status code
                  if authentication fails.
    """

    # Sistema de autenticação JWT
    user = request.json.get("username", None)
    password = request.json.get("password", None)

    # Verifica se no request.json tem esses dois parâmetros
    if user and password:

        # Verifica se o usuário informado está no database
        usuario_logado = Users.query.filter(Users.username == user).first()
        if usuario_logado:

            # Verifica a senha
            checkpw = usuario_logado.converte_senha(password)
            if checkpw:

                # Define o tempo de expiração do Token JWT e retorna ele
                expires = timedelta(hours=2)
                access_token = create_access_token(identity=user, expires_delta=expires)
                return jsonify(access_token=access_token), 200

    return jsonify({"error": "require auth"}), 401


@short.route("/encurtar_url", methods=["POST"])
# Descomente o decorator para habilitar a autenticação JWT
# @jwt_required()
def encurtar():
    """
    Shortens a given URL and returns the shortened version.
    This function handles a POST request containing a JSON payload with a URL to be shortened.
    It checks if the URL has already been shortened and returns the existing shortened URL if found.
    If the URL has not been shortened yet, it generates a new shortened URL, stores it in the database,
    and returns the newly shortened URL.
    Returns:
        Response: A JSON response containing either the shortened URL or an error message.
                  - If the URL is already shortened, returns a JSON response with an error message and the existing shortened URL.
                  - If the URL is successfully shortened, returns a JSON response with the new shortened URL.
                  - If the URL parameter is missing, returns a JSON response with an error message.
    Raises:
        401 Unauthorized: If the URL parameter is missing or if the URL is already shortened.
        200 OK: If the URL is successfully shortened.
    """

    db: SQLAlchemy = app.extensions["sqlalchemy"]
    # Pega a url a ser encurtada
    url = request.json.get("url", None)

    # Verifica se o request não está em branco
    if url:

        # Formata o Url de origem

        # Fiz dessa forma pois tem casos como o Reverse Proxy
        # que se usar o "request.host" ele fica com o endereço do host (127.0.0.1).
        # com o origin não ocorre isso, o lado ruim é que fica com o http/https
        # no texto, coisa que não ocorre no "request.host"

        origin = without_http(request.origin)

        # Verifica se a url que o usuário está tentando encurtar já se encontra no servidor
        check_already_shortened = Encurtados.query.filter(
            Encurtados.url_normal == url
        ).first()

        if check_already_shortened:

            # Caso esteja, ele retorna a url encurtada
            return (
                jsonify(
                    {
                        "error": "Url already shortened!",
                        "url": f"https://{origin}/{check_already_shortened.seed}",
                    }
                ),
                401,
            )

        url = url_conventer(url)
        # Caso não esteja, ele gera uma seed para essa url e adiciona no database
        new_seed = generate_id()
        gen_seed = Encurtados(url_normal=url, seed=new_seed)

        db.session.add(gen_seed)
        db.session.commit()

        # Retorna o sucesso
        return jsonify({"success": f" Your url is https://{origin}/{new_seed}"}), 200

    return jsonify({"error": "Requiere 'URL' parameter"}), 401


@short.route("/<seed>", methods=["GET"])
def ir_encurtado(seed: str):
    """
    Redirects to the original URL based on the provided shortened URL seed.
    This function checks if the provided seed exists in the database. If it does,
    it retrieves the corresponding original URL and redirects the user to that URL.
    If the seed does not exist in the database, it returns a JSON response with an error message.
    Args:
        seed (str): The seed string representing the shortened URL.
    Returns:
        Response: A Flask redirect response to the original URL with a 301 status code if the seed is found.
        Response: A JSON response with an error message and a 404 status code if the seed is not found.
    """

    # Verifica se a seed está cadastrada no database
    url_normal = Encurtados.query.filter(Encurtados.seed == seed).first()
    Encurtados.url_normal

    if url_normal:

        url = url_normal.url_normal
        # Se cadastrada, redireciona o user para a url que foi encurtada
        return redirect(url), 301

    # Caso não esteja, retorna erro
    return jsonify({"error": "Url not found"}), 404
