from app import app
from app.models.app_models import *
from app import db



with app.app_context():

    db.create_all()
    
    ## Lógica para criar o usuário JWT
    # root = Users.query.filter_by(username = 'test').first()
    
    # if root is None:
        
    #     usuario = Users(
    #         username = 'test',
    #         senhacrip = "14285714"
    #         )
        
    #     db.session.add(usuario)
    #     db.session.commit()