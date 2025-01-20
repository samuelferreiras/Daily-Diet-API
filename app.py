# app.py
from flask import Flask, request, jsonify
from database import db
from models.diet import Refeicao
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db.init_app(app)

with app.app_context():
    db.create_all()  

@app.route('/refeicoes', methods=['POST'])
def adicionar_refeição():
    data = request.json
    nome = data.get("nome")
    descricao = data.get("descricao")
    data_hora = datetime.strptime(data.get("data_hora"), "%d/%m/%Y %H:%M:%S")
    dentro_dieta = data.get("dentro_dieta")
    
    nova_refeicao = Refeicao(
        nome=nome,
        descricao=descricao,
        data_hora=data_hora,
        dentro_dieta=dentro_dieta
    )
    db.session.add(nova_refeicao)
    db.session.commit()
    return jsonify({"message": "Refeição adicionada com sucesso!"}), 200

@app.route('/refeicoes/<int:id>', methods=['PUT'])
def editar_refeicao(id):
  data = request.json
  refeicao = Refeicao.query.get(id)
  if not refeicao:
    return jsonify({"message": "Refeição não encontrada"}), 404
  
  refeicao.nome = data.get("nome")
  refeicao.descricao = data.get("descricao")
  refeicao.data_hora = datetime.strptime(data.get("data_hora"), "%d/%m/%Y %H:%M:%S")
  refeicao.dentro_dieta = data.get("dentro_dieta")
  
  db.session.commit()
  return jsonify({"message": "Refeição editada com sucesso!"})

@app.route('/refeicoes/<int:id>', methods=['DELETE'])
def deletar_refeição(id):
  refeicao = Refeicao.query.get(id)
  if not refeicao:
    return jsonify({"message": "Refeição não encontrada"}), 404
  
  db.session.delete(refeicao)
  db.session.commit()
  return jsonify({"message": "Refeição deletada com sucesso!"})
  
@app.route('/refeicoes', methods=['GET'])
def listar_refeicoes():
  refeicoes = Refeicao.query.all()
  refeicoes_json = []
  for refeicao in refeicoes:
    refeicoes_json.append({
      "id": refeicao.id,
      "nome": refeicao.nome,
      "descricao": refeicao.descricao,
      "data_hora": refeicao.data_hora.strftime("%d/%m/%Y %H:%M:%S"),
      "dentro_dieta": refeicao.dentro_dieta
    })
  return jsonify(refeicoes_json)

@app.route('/refeicoes/<int:id>', methods=['GET'])
def visualizar_refeicao(id):
  refeicao = Refeicao.query.get(id)
  if not refeicao:
    return jsonify({"message": "Refeição não registrada"}), 404
  
  resultado = {
    "id": refeicao.id,
    "nome": refeicao.nome,
    "descricao": refeicao.descricao,
    "data_hora": refeicao.data_hora.strftime("%d/%m/%Y %H:%M:%S"),
    "dentro_dieta": refeicao.dentro_dieta
  }
  return jsonify(resultado)

if __name__ == '__main__':
    app.run(debug=True)
