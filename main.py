from fastapi import FastAPI, status, Depends
from fastapi.params import Body
import classes
import model
from database import engine,get_db
from sqlalchemy.orm import Session


model.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
async def root(): 
    return {"Hello":"World!"}

@app.post("/criar", status_code=status.HTTP_201_CREATED)
async def criar_valores(nova_mensagem: classes.Mensagem, db:Session = Depends(get_db)):
    mensagem_criada = model.Model_Mensagem(
        titulo=nova_mensagem.titulo, 
        conteudo=nova_mensagem.conteudo,
        publicada = nova_mensagem.publicada)
    db.add(mensagem_criada)
    db.commit()
    db.refresh(mensagem_criada)

    return {"Mensagem criada": {
        "id": mensagem_criada.id,
        "titulo": mensagem_criada.titulo,
        "conteudo": mensagem_criada.conteudo,
        "publicada": mensagem_criada.publicada,
        "created_at": mensagem_criada.created_at
    }}

@app.get("/quadrado/{num}")
def square(num:int):
    return num ** 2
