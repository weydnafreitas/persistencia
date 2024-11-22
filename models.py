from pydantic import BaseModel

class Vaga(BaseModel):
    id : int 
    titulo: str
    organizacao: str
    descricao: str
    localizacao: str
    status: str