import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from supabase import create_client, Client

app = FastAPI(title="API Fútbol Chileno Completo")

# ⚠️ PEGA AQUÍ TUS DATOS DE SUPABASE SIN BORRAR LAS COMILLAS ""
SUPABASE_URL = "https://evzboohkrhvthlonhjkv.supabase.co/rest/v1/"
SUPABASE_KEY = "sb_publishable_qYr1x7NRYyRAxX6-Y7gH_w_8HSB99EZ"

# Conexión automática con la base de datos
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.get("/")
def inicio():
    return {"mensaje": "API de Fútbol Chileno conectada a Supabase correctamente"}

@app.get("/api/partidos")
def obtener_partidos(liga: str = None):
    try:
        consulta = supabase.table("partidos_en_vivo").select("*")
        if liga:
            consulta = consulta.eq("liga", liga)
        response = consulta.execute()
        return {"partidos": response.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



