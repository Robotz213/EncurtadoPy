from app import db
import bcrypt

salt = bcrypt.gensalt()

class Users(db.Model):
    
    __tablename__ = 'users'
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
        return bcrypt.checkpw(senha_texto_claro.encode("utf-8"), self.password.encode("utf-8"))  
    
class Encurtados(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    url_normal = db.Column(db.String(length=512), nullable=False, unique=True, default = "https://example.com")
    seed  = db.Column(db.String(length=8), nullable=False, unique=True, default = "DE4356QE")
    

    