import time
from supabase import create_client, Client

# ⚠️ PEGA AQUÍ TUS MISMAS LLAVES DE SUPABASE
SUPABASE_URL = "https://evzboohkrhvthlonhjkv.supabase.co/rest/v1/"
SUPABASE_KEY = "sb_publishable_AVK-p3tZaowNKWJ1YLQ0Ew_LFgJNSfx"

# Conexión con la base de datos en la nube
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def simular_rastreo_futbol():
    print("🤖 [Robot] Iniciando rastreo de ligas chilenas...")
    
    # Datos de prueba simulando el fútbol chileno
    partidos_detectados = [
        {
            "liga": "Tercera A",
            "equipo_local": "Deportes Linares",
            "equipo_visitante": "Colchagua CD",
            "goles_local": 1,
            "goles_visitante": 0,
            "minuto": 45,
            "estado": "EN_VIVO",
            "notificacion_evento": {"tipo": "GOL", "detalle": "¡Gol de Deportes Linares! (1-0)"}
        },
        {
            "liga": "Tercera B",
            "equipo_local": "Aguará",
            "equipo_visitante": "Tricolor Municipal",
            "goles_local": 0,
            "goles_visitante": 0,
            "minuto": 15,
            "estado": "EN_VIVO",
            "notificacion_evento": {"tipo": "NINGUNO", "detalle": ""}
        }
    ]
    
    for partido in partidos_detectados:
        print(f"⚽ Procesando: {partido['equipo_local']} vs {partido['equipo_visitante']} ({partido['liga']})")
        
        # Revisamos si el partido ya existe en nuestra base de datos para no repetirlo
        existe = supabase.table("partidos_en_vivo")\
            .select("*")\
            .eq("equipo_local", partido["equipo_local"])\
            .eq("liga", partido["liga"])\
            .execute()
            
        if len(existe.data) == 0:
            # Si no existe, lo insertamos por primera vez
            print("  -> Partido nuevo detectado. Registrando...")
            supabase.table("partidos_en_vivo").insert(partido).execute()
        else:
            # Extraemos correctamente el ID del primer elemento de la lista usando [0]
            partido_id = existe.data[0]["id"]
            print(f"  -> Actualizando marcador en vivo (ID: {partido_id}) -> {partido['equipo_local']} {partido['goles_local']}-{partido['goles_visitante']}")
            
            supabase.table("partidos_en_vivo").update({
                "goles_local": partido["goles_local"],
                "goles_visitante": partido["goles_visitante"],
                "minuto": partido["minuto"],
                "estado": partido["estado"],
                "notificacion_evento": partido["notificacion_evento"],
                "actualizado_at": "now()"
            }).eq("id", partido_id).execute()

    print("✅ [Robot] Rastreo finalizado con éxito.")

if __name__ == "__main__":
    simular_rastreo_futbol()

