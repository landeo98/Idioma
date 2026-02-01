from ingles_cli.logic.funciones import iterar_json_aleatorio,iterar_listenig
import os
from pathlib import Path
import platform
import sys
import pyttsx3
import subprocess

# Detectar sistema y TTS una sola vez
import platform
import subprocess
import os
import os
import platform
import shlex

def convertir_velocidad_termux(rate):
    if rate <= 120:
        return 0.7
    elif rate <= 140:
        return 0.85
    elif rate <= 160:
        return 1.0
    elif rate <= 200:
        return 1.15
    else:
        return 1.3


def pronunciar_palabra(palabra, velocidad=150, volumen=0.9):
    sistema = platform.system()

    try:
        if sistema == "Windows":
            import pyttsx3
            engine = pyttsx3.init()
            engine.setProperty('rate', velocidad)
            engine.setProperty('volume', volumen)

            engine.setProperty(
                'voice',
                r'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0'
            )

            print(f"🔊 Pronunciando: {palabra}")
            engine.say(palabra)
            engine.runAndWait()
            engine.stop()

        elif sistema == "Linux":  # Termux
            if os.system("which termux-tts-speak > /dev/null 2>&1") == 0:
                rate_termux = convertir_velocidad_termux(velocidad)
                texto = shlex.quote(palabra)

                print(f"🔊 Pronunciando: {palabra} (velocidad {rate_termux})")
                os.system(
                    f'termux-tts-speak -l en-US -r {rate_termux} "{texto}"'
                )
            else:
                print(f"⚠️ termux-tts-speak no disponible")

        else:
            print(f"⚠️ Pronunciación no soportada en {sistema}")

    except Exception as e:
        print(f"⚠️ Error de audio: {e}")
        print(f"   Palabra: {palabra}")



# def pronunciar_palabra(palabra,velocidad=150, volumen=0.9):
#     """Pronuncia una palabra en inglés, Windows y Termux"""
#     sistema = platform.system()

#     try:
#         if sistema == "Windows":
#             import pyttsx3
#             engine = pyttsx3.init()
#             engine.setProperty('rate', velocidad)
#             engine.setProperty('volume', volumen)
#             voices = engine.getProperty('voices')
#             if len(voices) > 1:
#                 # Buscar voz en inglés
#                 for v in voices:
#                     engine.setProperty('voice', r'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0')

                    

#             print(f"🔊 Pronunciando: {palabra}")
#             engine.say(palabra)
#             engine.runAndWait()
#             engine.stop()

#         elif sistema == "Linux":  # Termux se detecta como Linux
#             # Verifica que termux-tts-speak esté disponible
#             if os.system("which termux-tts-speak > /dev/null 2>&1") == 0:
#                 print(f"🔊 Pronunciando: {palabra}")
#                 os.system(f'termux-tts-speak -l en-US "{palabra}"')
#             else:
#                 print(f"⚠️ termux-tts-speak no disponible, palabra: {palabra}")

#         else:
#             print(f"⚠️ Pronunciación no soportada en {sistema}: {palabra}")

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


def modo_vocabulario(ruta, velocidad):
  
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
            pronunciar_palabra(palabra['ingles'],velocidad)

            respuesta = input("\n(ENTER=siguiente | r=repetir | s=salir): ").strip().lower()

            if respuesta == 's':
                print(f"\n📊 Practicaste {contador-1} palabras.")
                
                return

            elif respuesta == 'r':
                
                continue

            else:
                
                break

        contador += 1
def modo_escritura(ruta, velocidad ):
    print("\n=== MODO ESCRITURA ===")
    try:
        contador = 1
        for palabra in iterar_json_aleatorio(ruta):
            while True:
                print(f"\n{'='*40}")
                print(f"PALABRA {contador}")
                print(f"{'='*40}")
                print(f"🇪🇸 Español: {palabra['espanol']}")
                print(f"📂 Categoría: {palabra['categoria']}")
                
                pronunciar_palabra(palabra['ingles'],velocidad )
                respuesta = input("'r'=repetir, 'e'=Escribir): ").strip().lower()
                while True:
                    if respuesta == 'r':
                        pronunciar_palabra(palabra['ingles'],velocidad)
                        respuesta = input("'r'=repetir, Enter'=Escribir): ").strip().lower()
                    else:
                        break
                

                entrada = input("INGRESE LA PALABRA ESCUCHADA: ").strip().lower()
                
                if palabra['ingles'].strip().lower() == entrada:
                    print("Muy bien, sigue así")
                else:
                    print(f"🔊 Pronunciando: {palabra["ingles"]}")
                    print(f"❌ Incorrecto. La palabra es: {palabra['ingles']}")
                
                respuesta = input("\n¿Qué deseas? (ENTER=siguiente, 'r'=repetir, 's'=salir): ").strip().lower()
                
                if respuesta == 's':
                    print(f"\n{'='*40}")
                    print("¡SESIÓN TERMINADA!")
                    print(f"Palabras practicadas: {contador}")
                    print(f"{'='*40}")
                    break
                elif respuesta == 'r':
                    continue  # Repetir la misma palabra
                else:
                    break  # Siguiente palabra
            
            if respuesta == 's':
                break  # Salir del bucle principal
            
            contador += 1
        
        print(f"\n📊 Resumen: Practicaste {contador-1} palabras.")
        

    except FileNotFoundError:
        print(f"\n❌ ERROR: No se encuentra el archivo: {ruta}")
        print("Verifica que el archivo existe en esa ubicación.")
    except Exception as e:
        print(f"\n❌ Error inesperado: {type(e).__name__}: {e}")
        
    
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
    ancho = 50  # ancho del menú
    print("\n" + "═" * ancho)
    print("📚 MENÚ PRINCIPAL".center(ancho))
    print("═" * ancho)
    print("1. Vocabulario".center(ancho))
    print("2. Escritura".center(ancho))
    print("3. Listening".center(ancho))
    print("4. Frases".center(ancho))
    print("5. Salir".center(ancho))
    print("═" * ancho)

    while True:
        opcion = input("👉 Selecciona una opción: ".center(ancho)).strip()
        if opcion in ["1","2","3","4","5"]:
            return opcion
        else:
            print("⚠ Opción no válida, intenta de nuevo.".center(ancho))

def pedir_velocidad():
    ancho = 60  # ancho del menú
    print("\n" + "═" * ancho)
    print("🔊 VELOCIDAD DE PRONUNCIACIÓN".center(ancho))
    print("═" * ancho)
    print("⏎ Enter  → Por defecto (150)".center(ancho))
    print("🐢 BAJA   → 120".center(ancho))
    print("🚶 MEDIA  → 140".center(ancho))
    print("🏃 ALTA   → 160".center(ancho))
    print("⚡ APURADO → 200".center(ancho))
    print("═" * ancho)

    while True:
        vel = input("👉 Selecciona una opción: ".center(ancho)).strip().lower()

        if vel == "":
            return 150
        elif vel.isdigit():
            return int(vel)
        elif vel in ["baja"]:
            return 120
        elif vel in ["media"]:
            return 140
        elif vel in ["alta"]:
            return 160
        elif vel in ["apurado"]:
            return 200
        else:
            print("⚠ Opción no válida, intenta de nuevo.".center(ancho))


def main():
    velocidad = pedir_velocidad()
    print(f"🎧 Velocidad configurada en {velocidad}")

    while True:
       
        opcion = menu_principal()

        if opcion == '1':
            #"1. Vocabulario"
            ruta = obtener_ruta("vocabulario.json")
            modo_vocabulario(ruta,velocidad)
        elif opcion == '2':
            #"2. Escritura"
        
            ruta = obtener_ruta("vocabulario.json")
            modo_escritura(ruta,velocidad)
        elif opcion == '3':
            #"3. Listening"
           
            ruta = obtener_ruta("listening.json")
            modo_listening(ruta,velocidad)
        elif opcion == '4':
            #"4. Frases"
          
            ruta = obtener_ruta("vocabulario.json")
            modo_estudio_frases(ruta,velocidad  )
        elif opcion == '5':
            #"5. Salir"
            print("👋 Hasta luego")
            

            break
        else:
            print("❌ Opción inválida")
    
