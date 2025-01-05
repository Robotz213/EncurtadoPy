import bcrypt

from app import db

salt = bcrypt.gensalt()

"""
This module defines the Users model for the application.

    Classes:
        Users: Represents a user in the database.
"""


class Users(db.Model):
    """
    Represents a user in the database.

    Attributes:
        id (int): The primary key of the user.
        username (str): The username of the user, must be unique and not nullable.
        password (str): The hashed password of the user, must be unique and not nullable.

    Properties:
        senhacrip (str): Property to get or set the user's password in a hashed format.

    Methods:
        senhacrip (str): Property setter to hash the password.
        converte_senha (bool): Method to check if a plaintext password matches the hashed password.
    """

    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(length=60), nullable=False, unique=True)
    password = db.Column(db.String(length=60), nullable=False, unique=True)

    @property
    def senhacrip(self):
        return self.senhacrip

    @senhacrip.setter
    def senhacrip(self, senha_texto):
        self.password = bcrypt.hashpw(senha_texto.encode(), salt).decode("utf-8")

    def converte_senha(self, senha_texto_claro) -> bool:
        return bcrypt.checkpw(
            senha_texto_claro.encode("utf-8"), self.password.encode("utf-8")
        )


class Encurtados(db.Model):
    """
    Encurtados Model
    Attributes:
        id (int): Primary key for the table.
        url_normal (str): The original URL to be shortened. Must be unique and not null.
        seed (str): The unique seed used to generate the shortened URL. Must be unique and not null.
    """

    id = db.Column(db.Integer, primary_key=True)
    url_normal = db.Column(
        db.String(length=512),
        nullable=False,
        unique=True,
        default="https://example.com",
    )
    seed = db.Column(
        db.String(length=8), nullable=False, unique=True, default="DE4356QE"
    )
