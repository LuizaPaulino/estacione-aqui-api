from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote
from flask_cors import CORS
from sqlalchemy.sql import text

from datetime import datetime
from model import Session
from schemas import *

from logger import logger

info = Info(title="Estacione Aqui API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

#tags
veiculo_tag = Tag(name="Veículo", description="Registrar veículo, data e hora da entrada e saída de veiculos.")


@app.route('/')
def home():
    return redirect('/openapi')

# Listar
@app.get('/veiculos', tags=[veiculo_tag],
         responses={"200": ListagemVeiculosSchema, "404": ErrorSchema})
def get_veiculos():
    """Faz a busca por todos os veículos cadastrados
    Retorna uma representação da listagem de veículos
    """
    session = Session()
    veiculos = session.query(VeiculoEstacionamento).all()

    if not veiculos:
        return {"veiculos": []}, 200
    else:
        return apresenta_veiculos(veiculos), 200

# Adicionar
@app.post('/veiculo', tags=[veiculo_tag],
          responses={"200": VeiculoSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_veiculo(form: VeiculoSchema):
    """Adiciona um veículo, data hora da entrada e saída do estacionamento e valor cobrado à base de dados
    Retorna uma representação do veículo
    """

    try:
        veiculo = VeiculoEstacionamento(
            placa=form.placa,
            cor=form.cor if form.cor else None,
            data_entrada=validarData(form.data_entrada),
            data_saida=validarData(form.data_saida),
            valor=form.valor if form.valor else 0
        )
        session = Session()
        session.add(veiculo)
        session.commit()
        return apresenta_veiculo(veiculo), 200

    except Exception as e:
        return {"mesage": "Não foi possível adicionar o veículo"}, 400

# Alterar
@app.put('/veiculo', tags=[veiculo_tag],
          responses={"200": VeiculoSchema, "409": ErrorSchema, "400": ErrorSchema})
def alt_veiculo(form: VeiculoAlterarSchema):
    """Altera o registro de um veículo
    !Importante! Todos os campos são alterados na solicitação
    Retorna uma representação do veículo
    """
    sql_set = ""

    if form.id <= 0:
        return {"message": "Id inválido"}

    sql_set += ", placa = '" + form.placa.upper() + "'"
    sql_set += ", cor = '" + unquote(form.cor) + "'"
    sql_set += ", data_entrada = '" + str(validarData(form.data_entrada)) + "'"
    if validarData(form.data_saida):
        data_saida = "'" + str(validarData(form.data_saida)) + "'"
    else:
        data_saida = "NULL"
    sql_set += ", data_saida = " + data_saida
    sql_set += ", valor = '" + str(form.valor) + "'"
    
    try:
        session = Session()
        sql_update = "update veiculo_estacionamento set " + sql_set[1:] + " where id = " + str(form.id)
        session.execute(text(sql_update))
        session.commit()
        veiculo = session.query(VeiculoEstacionamento).filter(VeiculoEstacionamento.id == form.id).first()
        return apresenta_veiculo(veiculo), 200

    except Exception as e:
        return {"mesage": "Não foi possível alterar o veículo"}, 400

# Deletar
@app.delete('/veiculo', tags=[veiculo_tag],
            responses={"200": VeiculoSchema, "409": ErrorSchema, "404": ErrorSchema})
def deletar_veiculo(query: VeiculoDeletarSchema):
    """Deleta um veículo pelo id do registro ou todos os registros da placa
    Prioridade de deleção pelo id
    Pela placa, mais de um registro pode ser deletado
    Retorna uma mensagem de confirmação da remoção
    """

    session = Session()
    if query.id and isinstance(query.id, int):
        veiculo_id = unquote(str(query.id))
        count = session.query(VeiculoEstacionamento).filter(VeiculoEstacionamento.id == veiculo_id).delete()
    else:
        veiculo_placa = unquote(query.placa)
        count = session.query(VeiculoEstacionamento).filter(VeiculoEstacionamento.placa == veiculo_placa).delete()

    session.commit()

    if count:
        return {"mesage": "Veículo(s) removido(s)", "quantidade" : count}
    else:
        error_msg = "Veículo não encontrado na base"
        return {"mesage": error_msg}, 404

# Verifica se a data esta no formato e é válida
def validarData(strData):
    return None if not strData else datetime.strptime(strData, "%Y-%m-%d %H:%M:%S")