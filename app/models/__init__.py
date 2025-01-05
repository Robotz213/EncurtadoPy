from app import app, db

from .app_models import Encurtados, Users

__all__ = [Users, Encurtados]

with app.app_context():

    db.create_all()

    # Lógica para criar o usuário JWT
    # root = Users.query.filter_by(username = 'test').first()

    # if root is None:

    #     usuario = Users(
    #         username = 'test',
    #         senhacrip = "14285714"
    #         )

    #     db.session.add(usuario)
    #     db.session.commit()
