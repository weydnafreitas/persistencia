from fastapi import FastAPI
from http import HTTPStatus
from pydantic import BaseModel

app = FastAPI()


class Vagas(BaseModel):
    titulo: str
    organizacao: str
    descricao: str
    localizacao: str
    status: str


vagas = []


@app.get("/")
def read_root():
    return {"Vagas": vagas}


@app.post("/vagas/inserir", status_code=HTTPStatus.CREATED)
def inserirVaga(vaga: Vagas):
    nova_vaga = {
        "titulo": vaga.titulo,
        "organizacao": vaga.organizacao,
        "descricao": vaga.descricao,
        "localizacao": vaga.localizacao,
        "status": vaga.status,
    }

    vagas.append(nova_vaga)
    return {"Messagem": f"A vaga '{vaga.titulo}' foi criada com sucesso"}
