"""API de avaliação: sessões isoladas em memória; dados fictícios somente."""
import os
import threading
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from google import genai
from google.genai import types

app = FastAPI(title="Vita - API de Saúde e Bem-estar (IoB)", version="1.0")
SYSTEM_PROMPT = os.getenv("SYSTEM_PROMPT", "Você é Vita, assistente educacional sobre wearables. Não dê diagnósticos nem prescrições. Responda em português.")
MODELO_GEMINI = os.getenv("MODELO_GEMINI", "gemini-2.5-flash-lite")
SESSOES = {}
LOCK = threading.RLock()

class MensagemChat(BaseModel):
    session_id: str = Field(min_length=1,max_length=80,pattern=r"^[a-zA-Z0-9_-]+$")
    mensagem: str = Field(min_length=1,max_length=3000)
    modelo: str = "gemini"
    temperatura: float = Field(default=0.3,ge=0,le=1)

@app.get("/health")
def health():
    return {"status":"ok","modelo":MODELO_GEMINI}

@app.get("/sessions")
def sessions():
    with LOCK:
        return {"total":len(SESSOES),"ids":list(SESSOES)}

@app.delete("/sessions/{session_id}")
def delete_session(session_id: str):
    with LOCK:
        if session_id not in SESSOES:
            raise HTTPException(status_code=404, detail="Sessão não encontrada")
        del SESSOES[session_id]
    return {"status":"excluida","session_id":session_id}

@app.post("/chat")
def chat(dados: MensagemChat):
    if dados.modelo != "gemini":
        raise HTTPException(status_code=400, detail="Na API bônus, use modelo='gemini'. A interface e o chat do notebook permitem dois modelos.")
    chave = os.getenv("GEMINI_API_KEY")
    if not chave:
        raise HTTPException(status_code=503, detail="GEMINI_API_KEY não configurada")
    with LOCK:
        # Serialização simples evita perda de mensagens concorrentes em uma mesma sessão.
        anterior=list(SESSOES.get(dados.session_id, []))
        candidato=anterior + [{"role":"user","text":dados.mensagem}]
        conteudos=[types.Content(role=item["role"],parts=[types.Part.from_text(text=item["text"])]) for item in candidato]
        try:
            cliente=genai.Client(api_key=chave)
            resposta=cliente.models.generate_content(
                model=MODELO_GEMINI, contents=conteudos,
                config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT,temperature=dados.temperatura,max_output_tokens=450))
            texto=resposta.text
            if not texto:
                raise ValueError("Resposta vazia do modelo")
        except Exception as erro:
            # Não devolver tokens ou detalhes de erro do provedor.
            raise HTTPException(status_code=502,detail=f"Falha no provedor: {type(erro).__name__}") from erro
        candidato.append({"role":"model","text":texto})
        SESSOES[dados.session_id]=candidato
        return {"session_id":dados.session_id,"modelo":dados.modelo,"resposta":texto,"mensagens":len(candidato)}
