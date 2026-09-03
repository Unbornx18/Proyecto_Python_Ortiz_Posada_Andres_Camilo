import json
from funciones_horario import cargar_datos, guardar_datos, scheduling_conflict

schedule = cargar_datos()

while True:
    print("\n==========================================")
    print("GENERADOR DE HORARIOS PARA ESTUDIANTES")
    print("==========================================")
    print("1. Registrar una materia o actividad")
    print("2. Ver horario semanal")
    print("3. Modificar una materia o actividad")
    print("4. Eliminar una materia o actividad")
    print("5. Generar reporte del horario")
    print("6. Salir")
    print("==========================================")
    print("Seleccione una opción: ")
    option = input() 

    if option == "1":
        while True:
            subject = input("Ingrese el nombre de la materia o actividad: ")
            if not subject.replace(" ", "").isalpha():
                print("El nombre debe contener solo letras. Intente nuevamente.")
                continue   
            break

        while True:
            day = input("Ingrese el día de la semana (Lunes, Martes, Miércoles, Jueves, Viernes): ").capitalize()
            if day not in ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]:
                print("El día ingresado no es válido. Intente nuevamente.")
                continue
            break

        while True:
            start_time = input("Ingrese la hora de inicio (Formato 24H - Ejemplo: 14:00): ")

            if len(start_time) != 5 or start_time[2] != ':' or not (start_time[:2].isdigit() and start_time[3:].isdigit()):
                print("Error: Formato inválido. Use estrictamente HH:MM con números (ej. 14:00).")
                continue
            
            end_time = input("Ingrese la hora de fin (Formato 24H - Ejemplo: 16:00): ")
            if len(end_time) != 5 or end_time[2] != ':' or not (end_time[:2].isdigit() and end_time[3:].isdigit()):
                print("Error: Formato inválido. Use estrictamente HH:MM con números (ej. 16:00).")
                continue

            if start_time >= end_time:
                print("Error: La hora de inicio debe ser menor a la hora de fin.")
                continue

            if scheduling_conflict(schedule, start_time, end_time, day):
                print("Conflicto de horario detectado. Por favor, elija otro horario.")
                continue
            break
        
        ubicacion = input("Ingrese la ubicación (opcional, presione ENTER para omitir): ")
        if ubicacion == "":
            ubicacion = "Sin asignar"

        schedule.append({
            "materia": subject, 
            "dia": day, 
            "hora_inicio": start_time, 
            "hora_fin": end_time,
            "ubicacion": ubicacion
        })
        
        guardar_datos(schedule)
        print(f"\nMateria \"{subject}\" registrada exitosamente el {day} de {start_time} a {end_time} en {ubicacion}.")

    elif option == "2":
        if not schedule:
            print("El horario está vacío. No hay materias registradas.")
        else:
            print("\n=========================================================================================")
            print(f"| {'Hora':<8} | {'Lunes':<12} | {'Martes':<12} | {'Miércoles':<12} | {'Jueves':<12} | {'Viernes':<12} |")
            print("=========================================================================================")
            
            horas_unicas = []
            for item in schedule:
                if item["hora_inicio"] not in horas_unicas:
                    horas_unicas.append(item["hora_inicio"])
            horas_unicas.sort()

            for hora in horas_unicas:
                fila = {"Lunes": "Libre", "Martes": "Libre", "Miércoles": "Libre", "Jueves": "Libre", "Viernes": "Libre"}
                for item in schedule:
                    if item["hora_inicio"] == hora:
                        fila[item["dia"]] = item["materia"]
                
                print(f"| {hora:<8} | {fila['Lunes']:<12} | {fila['Martes']:<12} | {fila['Miércoles']:<12} | {fila['Jueves']:<12} | {fila['Viernes']:<12} |")
            print("=========================================================================================")

    elif option == "3":
        subject_to_modify = input("Ingrese el nombre de la materia o actividad a modificar: ")
        encontrado = False
        
        for item in schedule:
            if item["materia"] == subject_to_modify:
                encontrado = True
                
                while True:
                    print("Ingrese el nuevo día de la semana:")
                    new_day = input().capitalize()
                    if new_day not in ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]:
                        print("Día no válido. Intente de nuevo.")
                        continue
                    break
                
                while True:
                    new_start_time = input("Ingrese la nueva hora de inicio (Ej. 16:00): ")
                    if len(new_start_time) != 5 or new_start_time[2] != ':' or not (new_start_time[:2].isdigit() and new_start_time[3:].isdigit()):
                        print("Error: Formato inválido. Use estrictamente HH:MM (ej. 16:00).")
                        continue

                    new_end_time = input("Ingrese la nueva hora de fin (Ej. 18:00): ")
                    if len(new_end_time) != 5 or new_end_time[2] != ':' or not (new_end_time[:2].isdigit() and new_end_time[3:].isdigit()):
                        print("Error: Formato inválido. Use estrictamente HH:MM (ej. 18:00).")
                        continue

                    if new_start_time >= new_end_time:
                        print("Error: La hora de inicio debe ser menor a la hora de fin.")
                        continue
                    
                    if scheduling_conflict(schedule, new_start_time, new_end_time, new_day, ignore_subject=item["materia"]):
                        print("Conflicto de horario detectado. Elija otro horario.")
                        continue
                    break

                new_ubicacion = input("Ingrese la nueva ubicación (ENTER para mantener la misma): ")
                if new_ubicacion == "":
                    new_ubicacion = item["ubicacion"]

                item["dia"] = new_day
                item["hora_inicio"] = new_start_time
                item["hora_fin"] = new_end_time
                item["ubicacion"] = new_ubicacion

                guardar_datos(schedule)
                print(f"\nMateria \"{subject_to_modify}\" modificada exitosamente a {new_day} de {new_start_time} a {new_end_time} en {new_ubicacion}.")
                break
                
        if not encontrado:
            print(f"No se encontró la materia {subject_to_modify} en el horario.")

    elif option == "4":
        subject_to_delete = input("Ingrese el nombre de la materia o actividad que desea eliminar: ")
        day_to_delete = input("Ingrese el día de la semana: ").capitalize()
        
        encontrado = False
        for item in schedule:
            if item["materia"] == subject_to_delete and item["dia"] == day_to_delete:
                schedule.remove(item)
                guardar_datos(schedule)
                encontrado = True
                print(f"\nLa materia \"{subject_to_delete}\" ha sido eliminada del horario del día {day_to_delete}.")
                break
                
        if not encontrado:
            print(f"No se encontró la materia {subject_to_delete} el día {day_to_delete}.")

    elif option == "5":
        if not schedule:
            print("El horario está vacío. No hay datos para generar el reporte.")
        else:
            print("\n==========================================")
            print("REPORTE DEL HORARIO SEMANAL")
            print("==========================================")
            
            dias_semana = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]
            reporte_json = []

            for dia in dias_semana:
                eventos_dia = []
                for item in schedule:
                    if item["dia"] == dia:
                        eventos_dia.append({
                            "materia": item["materia"],
                            "hora_inicio": item["hora_inicio"],
                            "hora_fin": item["hora_fin"],
                            "ubicacion": item["ubicacion"]
                        })
                
                if len(eventos_dia) > 0:
                    reporte_json.append({
                        "dia": dia,
                        "eventos": eventos_dia
                    })
                    
                    print(f"{dia}:")
                    for ev in eventos_dia:
                        print(f"- {ev['materia']} ({ev['hora_inicio']} - {ev['hora_fin']}) en {ev['ubicacion']}")
                    print("------------------------------------------")
                    input("Presione ENTER para continuar...")

            with open("reporte_horario.json", "w", encoding="utf-8") as file:
                json.dump(reporte_json, file, indent=4, ensure_ascii=False)
            
            print("\nReporte generado correctamente en 'reporte_horario.json'.")

    elif option == "6":
        print("Saliendo del programa...")
        break