import csv
import json
import re
from pathlib import Path

# CSV files of creation and updates
creation_file = Path("creation.csv")
updates_file = Path("updates.csv")

print("Leyendo archivo creation.csv y updates.csv...")

if creation_file.is_file() and updates_file.is_file():

    email_regex = r'^[a-zA-Z0-9._%+-]+@dalton\.com\.mx$'
    while True:
        email = input("Ingresa el correo del usuario (debe ser del dominio @dalton.com.mx): ")
        if re.match(email_regex, email):
            break
        else:
            print("Correo inválido. Asegúrate de ingresar un correo válido con el dominio '@dalton.com.mx'")

    print(f"Comenzando búsqueda del usuario {email}...\n")

    jdata = None
    found = False
    # Creation of the user
    try:
        # Load queues data fro JSON file
        with open("queues.json", 'r', encoding='utf-8') as json_file:
            jdata = json.load(json_file)
        with open(creation_file, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                data = json.loads(row[6])
                if data["loginId"] == email:
                    found = True
                    print(f"Creado por: {row[0]}")
                    print(f"Fecha de creación: {row[3]}")
                    if data["features"].get("matching"):
                        # Print queues if exists
                        if data["features"]["matching"].get("queues"):
                            print(f"Colas:")
                            for cola in data["features"]["matching"]["queues"]:
                                for queue_data in jdata:
                                    if queue_data["queueId"] == cola["queueId"]:
                                        print(f"- {queue_data["name"]}")
                        else:
                            print(f"There are not queues registered at creation time")
                        # Print attributes if exists
                        if data["features"]["matching"].get("attributes"):
                            print(f"Atributos:")
                            for attribute in data["features"]["matching"]["attributes"]:
                                print(f"- {attribute}")
            if not found:
                print(f"User not found")
    except FileNotFoundError:
        print(f"Error: El archivo '{creation_file}' no existe")
    except PermissionError:
        print(f"Error: No tienes permisos para leer el archivo '{creation_file}'.")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")

    # Updates of the user
    try:
        with open(updates_file, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)

            print(f"\n\n####### ACTUALIZACIONES DE: {email} #######")
            for row in reader:
                new_data = json.loads(row[6])
                if new_data["loginId"] == email and row[0] != "System":
                    print(f"-----------------------------------------------------------------------------")
                    print("INFORMACION ACTUALIZADA:\n")
                    print(f"Actualizado por: {row[0]}")
                    print(f"Fecha de actualización: {row[3]}")
                    if new_data["features"].get("matching"):
                        # Print queues if exists
                        if new_data["features"]["matching"].get("queues"):
                            print(f"Colas Actualizadas:")
                            for cola in new_data["features"]["matching"]["queues"]:
                                for queue_data in jdata:
                                    if queue_data["queueId"] == cola["queueId"]:
                                        print(f"- {queue_data["name"]}")
                        else:
                            print(f"There are not queues registered at creation time")
                        # Print attributes if exists
                        if new_data["features"]["matching"].get("attributes"):
                            print(f"Atributos:")
                            for attribute in new_data["features"]["matching"]["attributes"]:
                                print(f"- {attribute}")
                    print(f"---------------------------------------------------------------------------")
    except FileNotFoundError:
        print(f"Error: El archivo '{updates_file}' no existe")
    except PermissionError:
        print(f"Error: No tienes permisos para leer el archivo '{updates_file}'.")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")
else:
    print(f"Archivos de creación y/o actualización no encontrados en el mismo directorio")