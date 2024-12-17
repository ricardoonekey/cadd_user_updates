import csv
from pathlib import Path

# CSV files of creation and updates
creation_file = Path("creation.csv")
updates_file = Path("updates.csv")

if creation_file.is_file() and updates_file.is_file():
    # Creation of the user
    try:
        with open(creation_file, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                print(row)
    except FileNotFoundError:
        print(f"Error: El archivo '{creation_file}' no existe")
    except PermissionError:
        print(f"Error: No tienes permisos para leer el archivo '{creation_file}'.")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")
else:
    print(f"Archivos de creación y/o actualización no encontrados en el mismo directorio")