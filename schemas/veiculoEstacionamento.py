from pydantic import BaseModel, Field
from typing import List
from datetime import datetime
from model.veiculoEstacionamento import VeiculoEstacionamento

class VeiculoSchema(BaseModel):
    """ Define como um carro deve ser retornado
    """
    placa: str = Field(..., example = "XXX4567")
    cor: str = ""
    data_entrada: str = Field(description="Formato YYYY-MM-DD HH:MM:SS", example=datetime.today().strftime("%Y-%m-%d %H:%M:%S"))
    data_saida: str = Field(description="Formato YYYY-MM-DD HH:MM:SS", default="")
    valor: float = 0

#print(VeiculoSchema.model_json_schema())

class VeiculoAlterarSchema(BaseModel):
    """ Define como um carro deve ser alterado
    """
    id: int = Field(..., example = 1)
    placa: str = Field(..., example = "XXX4567")
    cor: str = ""
    data_entrada: str = Field(description="Formato YYYY-MM-DD HH:MM:SS", example=datetime.today().strftime("%Y-%m-%d %H:%M:%S"))
    data_saida: str = Field(description="Formato YYYY-MM-DD HH:MM:SS", default="")
    valor: float = 0

class VeiculoBuscarSchema(BaseModel):
    """Define a busca feita pela placa do veículo no estacionamento
    """
    placa: str = "XXX0000"

class VeiculoDeletarSchema(BaseModel):
    """Define o parâmetro de deleção do veículo, sendo por id ou placa.
    """
    id: int = 1
    placa: str = ""

class ListagemVeiculosSchema(BaseModel):
    """ Define como a listagem de veículos será retornada
    """
    veiculos:List[VeiculoSchema]


def apresenta_veiculo(veiculo: VeiculoEstacionamento):
    """ Retorna uma representação do registro seguindo o schema definido em
        VeiculoEstacionamentoViewSchema.
    """
    return {
        "id": veiculo.id,
        "placa": veiculo.placa,
        "cor": veiculo.cor,
        "data_entrada": veiculo.data_entrada.strftime("%Y-%m-%d %H:%M:%S"),
        "data_saida": veiculo.data_saida.strftime("%Y-%m-%d %H:%M:%S") if veiculo.data_saida else "",
        "valor": veiculo.valor,
        "data_insercao": veiculo.data_insercao.strftime("%Y-%m-%d %H:%M:%S"),
    }

def apresenta_veiculos(veiculos: List[VeiculoEstacionamento]):
    """ Retorna uma representação da lista de veículos seguindo o schema definido em
        VeiculoSchema.
    """
    result = []
    for veiculo in veiculos:
        result.append({
            "id": veiculo.id,
            "placa": veiculo.placa,
            "cor": veiculo.cor if veiculo.cor else "",
            "dataEntrada": veiculo.data_entrada.strftime("%Y-%m-%d %H:%M:%S"),
            "dataSaida": veiculo.data_saida.strftime("%Y-%m-%d %H:%M:%S") if veiculo.data_saida else "",
            "valor": veiculo.valor,
        })

    return {"veiculos" : result}