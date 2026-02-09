import json
import random
import time 


# ========== FUNCIÓN PARA LEER JSON ==========
def iterar_json_aleatorio(ruta):
    """Itera elementos JSON en orden aleatorio sin repetir"""
    with open(ruta, 'r', encoding='utf-8') as f:
        datos = json.load(f)
    
    palabras = datos['vocabulario_ingles']['palabras'].copy()
    random.shuffle(palabras)
    
    for palabra in palabras:
        yield palabra
def iterar_ordenado_json(ruta):
    """Itera elementos JSON en orden sin repetir"""
    with open(ruta, 'r', encoding='utf-8') as f:
        datos_ordenados = json.load(f)
    
    palabras = datos_ordenados['clasess']['palabra']
    
    for oraciones in palabras:
        yield oraciones

# FUNCION PARA WRITING
def iterar_listenig(ruta):
    """Itera frases de listening en orden aleatorio sin repetir"""
    with open(ruta, 'r', encoding='utf-8') as f:
        datos = json.load(f)
    
    frases = []
    # Extraer todas las frases de todas las categorías
    for categoria in datos['frases_listening_ingles']['categorias']:
        for frase in categoria['frases']:
            # Crear un objeto con todas las claves del JSON
            item = {
                'ingles_formal': frase['escrito_formal'],
                'ingles_informal': frase['escrito_informal'],
                'pronunciacion_real': frase['pronunciacion_real'],
                'espanol': frase['espanol'],
                'contracciones': frase['contracciones'],
                'ejemplo_sonido': frase['ejemplo_sonido'],
                'categoria': categoria['nombre'],
                'contexto': categoria['contexto']
            }
            frases.append(item)
    
    random.shuffle(frases)
    
    for frase in frases:
        yield frase 

#