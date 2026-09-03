import json
import os

ARCHIVO_DATOS = "horario.json"

# Funcionalidad: Cargar datos para persistencia entre sesiones
def cargar_datos():
    if os.path.exists(ARCHIVO_DATOS):
        with open(ARCHIVO_DATOS, "r", encoding="utf-8") as file:
            return json.load(file)
    return []

# Funcionalidad: Guardar datos en el JSON principal
def guardar_datos(schedule):
    with open(ARCHIVO_DATOS, "w", encoding="utf-8") as file:
        json.dump(schedule, file, indent=4, ensure_ascii=False)

# Funcionalidad: Evitar superposición de horarios
def scheduling_conflict(schedule, start_time, end_time, day, ignore_subject=None):
    for item in schedule:
        # Se ignora la materia actual si se está modificando
        if item["dia"] == day and item.get("materia") != ignore_subject:
            existing_start = item["hora_inicio"]
            existing_end = item["hora_fin"]
            # Lógica simple de intersección de tiempos
            if (start_time < existing_end and end_time > existing_start):
                return True
    return False