from fastapi import FastAPI, status, Depends
from fastapi.params import Body
import classes
import model
from database import engine,get_db
from sqlalchemy.orm import Session
from data_ufu_editais import editais_ufu
from typing import Optional
from sqlalchemy.exc import IntegrityError


model.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
async def root(): 
    return {"Hello":"World!!"}

@app.post("/criar", status_code=status.HTTP_201_CREATED)
async def criar_valores(nova_mensagem: classes.Mensagem, db:Session = Depends(get_db)):
    mensagem_criada = model.Model_Mensagem(
        titulo=nova_mensagem.titulo, 
        conteudo=nova_mensagem.conteudo,
        publicada = nova_mensagem.publicada)
    db.add(mensagem_criada)
    db.commit()
    db.refresh(mensagem_criada)

    return {"Inserido na tabela": {
        "id": mensagem_criada.id,
        "titulo": mensagem_criada.titulo,
        "conteudo": mensagem_criada.conteudo,
        "publicada": mensagem_criada.publicada,
        "created_at": mensagem_criada.created_at
    }}

@app.put("/webscraping", status_code=status.HTTP_201_CREATED)
async def popula_banco_editais(db: Session = Depends(get_db)):
    editais_salvos = []
    editais = editais_ufu()

    for edital in editais:
        edital_existente = db.query(model.Model_Editais).filter(
            model.Model_Editais.titulo_edital == edital["titulo"],
            model.Model_Editais.data_publicacao == edital["data_publicacao"]
        ).first()

        if not edital_existente:
            novo_edital = model.Model_Editais(
                numero_edital=edital["numero_edital"],
                orgao_responsavel=edital["orgao_responsavel"],
                titulo_edital=edital["titulo"],
                link_edital=edital["link"],
                tipo=edital["tipo"],
                data_publicacao=edital["data_publicacao"]
            )
            try:
                db.add(novo_edital)
                db.commit()
                db.refresh(novo_edital)
                editais_salvos.append(novo_edital)
            except IntegrityError:
                db.rollback()

    if not editais_salvos:
        return Response(status_code=status.HTTP_304_NOT_MODIFIED, content='{"Mensagem": "Banco de dados já atualizado"}', media_type="application/json")

    return {"Mensagem": editais_salvos}

@app.get("/webscraping")
async def retorna_webscraping(
    db: Session = Depends(get_db),
    filtroOrg: Optional[str] = None,
    filtroTipo: Optional[str] = None
):
    query = db.query(model.Model_Editais)

    if filtroOrg and filtroTipo:
        query = query.filter(
        model.Model_Editais.orgao_responsavel.ilike(f"%{filtroOrg}%"),
        model.Model_Editais.tipo.ilike(f"%{filtroTipo}%"))

    elif filtroOrg:
        query = query.filter(model.Model_Editais.orgao_responsavel == filtroOrg)
    elif filtroTipo:
        query = query.filter(model.Model_Editais.tipo == filtroTipo)

    #print(str(query)) #Debug
    editais = query.all()

    if not editais:
        return {"Mensagem": "Nenhum edital encontrado com os filtros fornecidos"}

    return editais


@app.get("/quadrado/{num}")
def square(num:int):
    return num ** 2
