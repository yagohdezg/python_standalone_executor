import pandas as pd


def create_frame(url, name, direction, despacho, n_colegiado, comunidad_autonoma, telefono, description, idiomas, experience):
    return pd.DataFrame({
        "link": [url],
        "nombre": [name],
        "direccion": [direction],
        "despacho": [despacho],
        "numero_colegiado": [n_colegiado],
        "comunidad_autonoma": [comunidad_autonoma],
        "telefono": [telefono],
        "descripcion": [description],
        "idiomas": [idiomas],
        "experiencia": [experience]
    })
