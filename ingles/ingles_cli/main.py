from ingles_cli.logic.funciones import iterar_json_aleatorio,iterar_listenig
import pyttsx3
import os
from pathlib import Path
import platform
import os
import sys

""" main.py
 ├─ main()
 ├─ menu_principal()
 ├─ modo_vocabulario()
 ├─ modo_escritura()
 ├─ modo_listening()
 └─ modo_estudio_frases()
 """
from pathlib import Path

""" El guion bajo _ al inicio significa:

👉 “esto es interno, no lo uses directamente desde fuera”
Python NO lo hace privado de verdad, pero los programadores entienden:

“esto no se toca desde otros archivos”
🔍 Ejemplo sencillo
_engine = None   # interna
engine = None    # pública

La diferencia no es técnica, es mental / de diseño.
✔ _engine → uso interno del módulo
✔ get_engine() → forma correcta de acceder """
import platform
import os
import sys

def pronunciar_palabra(palabra):
    """Pronuncia una palabra en inglés, Windows y Termux"""
    sistema = platform.system()

    try:
        if sistema == "Windows":
            import pyttsx3
            engine = pyttsx3.init()
            engine.setProperty('rate', 150)
            engine.setProperty('volume', 0.9)
            voices = engine.getProperty('voices')
            if len(voices) > 1:
                # Buscar voz en inglés
                for v in voices:
                    engine.setProperty('voice', r'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0')

                    

            print(f"🔊 Pronunciando: {palabra}")
            engine.say(palabra)
            engine.runAndWait()
            engine.stop()

        elif sistema == "Linux":  # Termux se detecta como Linux
            # Verifica que termux-tts-speak esté disponible
            if os.system("which termux-tts-speak > /dev/null 2>&1") == 0:
                print(f"🔊 Pronunciando: {palabra}")
                os.system(f'termux-tts-speak -l en-US "{palabra}"')
            else:
                print(f"⚠️ termux-tts-speak no disponible, palabra: {palabra}")

        else:
            print(f"⚠️ Pronunciación no soportada en {sistema}: {palabra}")

    except Exception as e:
        print(f"⚠️ Error de audio: {e}")
        print(f"   Palabra: {palabra}")
# def pronunciar_palabra(palabra):
#     """Pronuncia una palabra en inglés"""

#     try:
#         import pyttsx3
#         engine = pyttsx3.init()
#         engine.setProperty('rate', 150)
#         engine.setProperty('volume', 0.9)

#         voices = engine.getProperty('voices')
#         if len(voices) > 1:
#             engine.setProperty('voice', voices[1].id)

#         print(f"🔊 Pronunciando: {palabra}")
#         engine.say(palabra)
#         engine.runAndWait()
#         engine.stop()

#     except Exception as e:
#         print(f"⚠️ Error de audio: {e}")
#         print(f"   Palabra: {palabra}")



def obtener_ruta(nombre_archivo: str) -> Path:
    """
    Devuelve la ruta absoluta a un archivo dentro de Recursos/
    """
    base_dir = Path(__file__).parent
    ruta = base_dir / "Recursos" / nombre_archivo

    if not ruta.exists():
        raise FileNotFoundError(f"No se encuentra el archivo: {ruta}")

    return ruta


def modo_vocabulario(ruta):
  
    print("\n=== MODO VOCABULARIO ===")
    contador = 1

    for palabra in iterar_json_aleatorio(ruta):

        while True:
            print(f"\n{'='*40}")
            print(f"PALABRA {contador}")
            print(f"{'='*40}")
            print(f"🇬🇧 Inglés: {palabra['ingles']}")
            print(f"🇪🇸 Español: {palabra['espanol']}")
            print(f"📂 Categoría: {palabra['categoria']}")
            pronunciar_palabra(palabra['ingles'])

            respuesta = input("\n(ENTER=siguiente | r=repetir | s=salir): ").strip().lower()

            if respuesta == 's':
                print(f"\n📊 Practicaste {contador-1} palabras.")
                
                return

            elif respuesta == 'r':
                
                continue

            else:
                
                break

        contador += 1
def modo_escritura(ruta):
    print("\n=== MODO ESCRITURA ===")
    contador = 1

    for palabra in iterar_json_aleatorio(ruta):
        while True:
            print(f"\nPALABRA {contador}")
            print(f"🇪🇸 Español: {palabra['espanol']}")

            pronunciar_palabra(palabra['ingles'])

            respuesta = input(
                "\n(ENTER=siguiente | s=salir): "
            ).strip().lower()

            if respuesta == 's':
                print(f"\n📊 Practicaste {contador-1} palabras.")
        
                return

            break

        contador += 1
def modo_listening(ruta):
    print("\n=== MODO LISTENING ===")
    contador = 1

    for frase in iterar_listenig(ruta):
        while True:
            print(f"\nFRASE {contador}")
            print(f"🇪🇸 Español: {frase['espanol']}")

            pronunciar_palabra(frase['ingles_informal'])

            entrada = input("ESCRIBE LO QUE ESCUCHASTE: ").lower()

            if entrada in (
                frase['ingles_formal'].lower(),
                frase['ingles_informal'].lower()
            ):
                print("✅ Correcto")
            else:
                print("❌ Incorrecto")
                print("Formal:", frase['ingles_formal'])
                print("Informal:", frase['ingles_informal'])

            respuesta = input(
                "\n(ENTER=siguiente | r=repetir | s=salir): "
            ).strip().lower()

            if respuesta == 's':
                print(f"\n📊 Practicaste {contador-1} frases.")
                
                return

            elif respuesta == 'r':
                continue

            break

        contador += 1
def modo_estudio_frases(ruta):
    print("\n=== MODO ESTUDIO DE FRASES ===")
    contador = 1

    for frase in iterar_listenig(ruta):
        print(f"\nFRASE {contador}")
        print("Formal:", frase['ingles_formal'])
        print("Informal:", frase['ingles_informal'])
        print("Español:", frase['espanol'])

        pronunciar_palabra(frase['ingles_informal'])

        respuesta = input("(ENTER=siguiente | s=salir): ").lower()

        if respuesta == 's':
            print(f"\n📊 Estudiaste {contador-1} frases.")
        
            return

        contador += 1
def menu_principal():
    print("\nMENÚ PRINCIPAL")
    print("1. Vocabulario")
    print("2. Escritura")
    print("3. Listening")
    print("4. Frases")
    print("5. Salir")

    return input("Opción: ").strip()
def main():
    
    while True:
       
        opcion = menu_principal()

        if opcion == '1':
            ruta = obtener_ruta("vocabulario.json")
            modo_vocabulario(ruta)
        elif opcion == '2':
        
            ruta = obtener_ruta("listening.json")
            modo_escritura(ruta)
        elif opcion == '3':
           
            ruta = obtener_ruta("listening.json")
            modo_listening(ruta)
        elif opcion == '4':
          
            ruta = obtener_ruta("vocabulario.json")
            modo_estudio_frases(ruta)
        elif opcion == '5':
            print("👋 Hasta luego")
            

            break
        else:
            print("❌ Opción inválida")
    
