from sqlalchemy import Column, String, Integer, DateTime, Float
from datetime import datetime
from typing import Union

from  model import Base

class VeiculoEstacionamento(Base):
    __tablename__ = 'veiculo_estacionamento'

    id = Column("id", Integer, primary_key=True)
    placa = Column(String(10))
    cor = Column(String(20))
    data_entrada = Column(DateTime)
    data_saida = Column(DateTime)
    valor = Column(Float)
    data_insercao = Column(DateTime, default=datetime.now())

    def __init__(self, placa:str, data_entrada: datetime, cor:str = None,
                 data_saida: datetime = None, valor: float = None, data_insercao: datetime = None):
        """
        Registra um veícuo no estacionamento

        Arguments:
            placa: placa do veiculo
            cor: cor do veiculo
            data_entrada: data hora que o veículo entrou no estacionamento
            data_saida: data hora que o veículo saiu do estacionamento
            valor: valor tarifado
            data_insercao: data de quando registro foi inserido à base
        """
        self.placa = placa
        self.cor = cor
        self.data_entrada = data_entrada
        self.data_saida = data_saida
        self.valor = valor
        self.data_insercao = data_insercao

