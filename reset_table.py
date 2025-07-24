from app import db
from app import app  # certifique-se de importar o app se necessário para o contexto do banco

with app.app_context():
    db.drop_all()
    db.create_all()
    print("Banco de dados resetado com sucesso.")