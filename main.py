from fastapi import FastAPI, HTTPException
from models import Vaga
import csv
import os

app = FastAPI()

csv_file = "csv/vagas_csv.csv"  # Caminho para o arquivo CSV


def obter_proximo_id() -> int:
    """Obtém o próximo ID disponível no CSV."""
    if not os.path.exists(csv_file) or os.path.getsize(csv_file) == 0:
        return 1

    with open(csv_file, "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader, None)  # Ignora o cabeçalho
        ids = [int(row[0]) for row in reader if row and row[0].isdigit()]

    return max(ids, default=0) + 1


def salvar_vaga_csv(vaga: Vaga):
    """Salva a vaga no arquivo CSV."""
    try:
        # Verifica se o cabeçalho é necessário
        file_needs_header = not os.path.exists(csv_file) or os.path.getsize(csv_file) == 0

        # Gera o próximo ID
        vaga.id = obter_proximo_id()

        # Adiciona a vaga ao CSV
        with open(csv_file, mode="a", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)

            # Escreve o cabeçalho, se necessário
            if file_needs_header:
                writer.writerow(["id", "titulo", "organizacao", "descricao", "localizacao"])

            # Escreve os dados da vaga
            writer.writerow([vaga.id, vaga.titulo, vaga.organizacao, vaga.descricao, vaga.localizacao])

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao salvar vaga no CSV: {e}")


@app.post("/vagas/")
async def criar_vaga(vaga: Vaga):
    """
    Endpoint para criar uma nova vaga.
    Envia um JSON no corpo da requisição com os dados da vaga.
    """
    try:
        salvar_vaga_csv(vaga)
        return {"message": "Vaga criada com sucesso!", "id": vaga.id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def ler_vagas_csv():
    """Lê o arquivo CSV e retorna todas as vagas como uma lista de objetos."""
    if not os.path.exists(csv_file) or os.path.getsize(csv_file) == 0:
        return []  # Retorna lista vazia se o arquivo não existir ou estiver vazio

    vagas = []
    with open(csv_file, "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader, None)  # Ignora o cabeçalho
        for row in reader:
            if row and len(row) >= 5:  # Alterado para 5 campos
                vaga = Vaga(
                    id=int(row[0]),
                    titulo=row[1],
                    organizacao=row[2],
                    descricao=row[3],
                    localizacao=row[4]
                )
                vagas.append(vaga)
    
    return vagas

@app.post("/vagas/")
async def criar_vaga(vaga: Vaga):
    """
    Endpoint para criar uma nova vaga.
    Envia um JSON no corpo da requisição com os dados da vaga.
    O id será atribuído automaticamente e incrementado.
    """
    try:
        salvar_vaga_csv(vaga)
        return {"message": "Vaga criada com sucesso!", "id": vaga.id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/vagas/")
async def listar_vagas():
    """
    Endpoint para listar todas as vagas cadastradas no arquivo CSV.
    Retorna todas as vagas como um JSON.
    """
    try:
        vagas = ler_vagas_csv()
        if not vagas:
            return {"message": "Nenhuma vaga encontrada."}
        return {"vagas": [vaga.dict() for vaga in vagas]}  # Converte os objetos para dicionários
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar as vagas: {str(e)}")