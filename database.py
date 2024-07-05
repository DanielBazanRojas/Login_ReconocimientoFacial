import os
import mysql.connector as db
import json

# Obtener el directorio del script actual
script_dir = os.path.dirname(__file__) 

# Usar la ruta absoluta del archivo keys.json
json_path = os.path.join(script_dir, 'keys.json')

# Cargar las claves de la base de datos desde keys.json
with open(json_path) as json_file:
    keys = json.load(json_file)

def convertToBinaryData(filename):
    # Convertir datos digitales a formato binario
    try:
        with open(filename, 'rb') as file:
            binaryData = file.read()
        return binaryData
    except Exception as e:
        print(f"Error al convertir a binario: {e}")
        return None

def write_file(data, path):
    # Convertir datos binarios a formato adecuado y escribir en el disco
    with open(path, 'wb') as file:
        file.write(data)

def registerUser(name, photo):
    id = 0
    inserted = 0

    try:
        con = db.connect(host=keys["host"], user=keys["user"], password=keys["password"], database=keys["database"])
        cursor = con.cursor()
        sql = "INSERT INTO `user`(name, photo) VALUES (%s,%s)"
        pic = convertToBinaryData(photo)

        if pic:
            cursor.execute(sql, (name, pic))
            con.commit()
            inserted = cursor.rowcount
            id = cursor.lastrowid
    except db.Error as e:
        print(f"Error al insertar la imagen: {e}")
    finally:
        if con.is_connected():
            cursor.close()
            con.close()
    return {"id": id, "affected":inserted}

def getUser(name, path):
    id = 0
    rows = 0

    try:
        con = db.connect(host=keys["host"], user=keys["user"], password=keys["password"], database=keys["database"])
        cursor = con.cursor()
        sql = "SELECT * FROM `user` WHERE name = %s"

        cursor.execute(sql, (name,))
        records = cursor.fetchall()

        for row in records:
            id = row[0]
            write_file(row[2], path)
        rows = len(records)
    except db.Error as e:
        print(f"Error al leer la imagen: {e}")
    finally:
        if con.is_connected():
            cursor.close()
            con.close()
    return {"id": id, "affected": rows}
