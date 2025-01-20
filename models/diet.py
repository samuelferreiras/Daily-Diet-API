from datetime import datetime
from database import db

class Refeicao(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  nome = db.Column(db.String(80), nullable=False)
  descricao = db.Column(db.String(255), nullable=True)
  data_hora = db.Column(db.DateTime, nullable=False)
  dentro_dieta = db.Column(db.Boolean, nullable=False)