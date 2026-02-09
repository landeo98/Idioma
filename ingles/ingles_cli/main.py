from ingles_cli.logic.funciones import iterar_json_aleatorio,iterar_listenig
from ingles_cli.logic.shadowing import shadowing_parrafos
from ingles_cli.logic.funciones import iterar_ordenado_json
from pathlib import Path
# Detectar sistema y TTS una sola vez
import platform
import os
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

                print(f"🔊 Pronunciando: {palabra} \n(velocidad {rate_termux})")
                os.system(
                    f'termux-tts-speak -l en-US -r {rate_termux} {texto}'
                )
            else:
                print(f"⚠️ termux-tts-speak no disponible")

        else:
            print(f"⚠️ Pronunciación no soportada en {sistema}")

    except Exception as e:
        print(f"⚠️ Error de audio: {e}")
        print(f"   Palabra: {palabra}")

def obtener_ruta(nombre_archivo: str, carpeta: str ) -> Path:
    """
    Devuelve la ruta absoluta a un archivo dentro de Recursos/
    """
    base_dir = Path(__file__).parent
    ruta = base_dir / carpeta / nombre_archivo

    if not ruta.exists():
        raise FileNotFoundError(f"No se encuentra el archivo: {ruta}")

    return ruta

def obtener_carpeta_shadowing(carpeta_nombre: str) -> str:
    """Obtiene la ruta de la carpeta 'Recursos_shadowing' relativa al script."""
    return os.path.join(os.path.dirname(__file__), carpeta_nombre)

def modo_vocabulario( velocidad,ruta):
  
    print("\n=== MODO VOCABULARIO ===")
    contador = 1

    for palabra in iterar_json_aleatorio(ruta):
        

        while True:
            print(f"\n{'='*30}")
            print(f"PALABRA {contador}")
            print(f"{'='*30}")
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


def modo_clases( velocidad,ruta):
  
    print("\n=== MODO CLASES ===")
    contador = 1

    for clases in iterar_ordenado_json(ruta):
        

        while True:
            print(f"\n{'='*30}")
            print(f"PALABRA {contador}")
            print(f"{'='*30}")
            print(f"Inglés: {clases['ingles']}")
            print(f"Español: {clases['espanol']}")
            pronunciar_palabra(clases['ingles'],velocidad)

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
def modo_listening(ruta, velocidad):
    print("\n=== MODO LISTENING ===")
    print("En desarrollo...")
    #falta correguir salidas y entradas para que sean mas claras y no se confundan con las opciones de repetir o salir
    # contador = 1

    # for frase in iterar_listenig(ruta):
    #     while True:
    #         print(f"\nFRASE {contador}")
    #         print(f"🇪🇸 Español: {frase['espanol']}")

    #         pronunciar_palabra(frase['ingles_informal'], velocidad)

    #         entrada = input("ESCRIBE LO QUE ESCUCHASTE: ").lower()

    #         if entrada in (
    #             frase['ingles_formal'].lower(),
    #             frase['ingles_informal'].lower()
    #         ):
    #             print("✅ Correcto")
    #         else:
    #             print("❌ Incorrecto")
    #             print("Formal:", frase['ingles_formal'])
    #             print("Informal:", frase['ingles_informal'])

    #         respuesta = input(
    #             "\n(ENTER=siguiente | r=repetir | s=salir): "
    #         ).strip().lower()

    #         if respuesta == 's':
    #             print(f"\n📊 Practicaste {contador-1} frases.")
                
    #             return

    #         elif respuesta == 'r':
    #             continue

    #         break

    #     contador += 1
def modo_estudio_frases(ruta, velocidad):
    print("\n=== en desarrollo ===")

def menu_principal():
    ancho = 30  # ancho del menú
    print("\n" + "═" * ancho)
    print("📚 MENÚ PRINCIPAL".center(ancho))
    print("═" * ancho)
    print("1. Vocabulario".center(ancho))
    print("2. Escritura".center(ancho))
    print("3. Listening".center(ancho))
    print("4. Frases".center(ancho))
    print("5. Shadowing".center(ancho))
    print("0. Clases".center(ancho))
    print("6. Salir".center(ancho))
    print("═" * ancho)

    while True:
        opcion = input("👉 Que deseas hacer hoy: ".center(ancho)).strip()
        if opcion in ["1","2","3","4","5","0","6"]:
            return opcion
        else:
            print("⚠ Opción no válida, intenta de nuevo.".center(ancho))

def menu_clases():
    ancho = 30  # ancho del menú
    print("\n" + "═" * ancho)
    print("📚 MENÚ CLASES".center(ancho))
    print("═" * ancho)
    print("1. SECION 1".center(ancho))
    print("2. SECION 2".center(ancho))
    print("3. SECION 3".center(ancho))
    print("4. SECION 4".center(ancho))
    print("6. Salir".center(ancho))
    print("═" * ancho)

    while True:
        entrada = input("👉 seleciono una clase: ".center(ancho)).strip()
        if entrada in ["1","2","3","4","6"]:
            return entrada
        else:
            print("⚠ Opción no válida, intenta de nuevo.".center(ancho))
def pedir_velocidad():
    ancho = 30  # ancho del menú
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
        vel = input("👉 Selecciona una opción:".center(ancho)).strip().lower()

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
            carpeta= "Recursos"
            ruta = obtener_ruta("vocabulario.json", carpeta)
            modo_vocabulario(velocidad,ruta)
        elif opcion == '2':
            #"2. Escritura"
            carpeta= "Recursos"
        
            ruta = obtener_ruta("vocabulario.json", carpeta)
            modo_escritura(ruta,velocidad)
        elif opcion == '3':
            carpeta= "Recursos"
            #"3. Listening"
           
            ruta = obtener_ruta("listening.json", carpeta)
            modo_listening(ruta,velocidad)
        elif opcion == '4':
            carpeta= "Recursos"
            #"4. Frases"
          
            ruta = obtener_ruta("vocabulario.json", carpeta)
            modo_estudio_frases(ruta,velocidad  )
        
        
        elif opcion == '5':
            carpeta = obtener_carpeta_shadowing("Recursos_shadowing")
            shadowing_parrafos(carpeta, pronunciar_palabra, velocidad)
        
        elif opcion == '0':
            print("\n📚 Módulo de clases .")
            while True:
                # el modo vocabulario tambien funcionar para las calsesl o que varia son 
                #las  rutas  y el iterador 

                sub_opcion = menu_clases()
                
                if sub_opcion == '1':
                    carpeta = "ingles_basico"
                    ruta = obtener_ruta("primera.json", carpeta)
                    modo_clases(velocidad, ruta)

                elif sub_opcion == '2':
                    carpeta = "ingles_basico"
                    ruta = obtener_ruta("segunda.json", carpeta)             
                    modo_clases(velocidad, ruta)

                elif sub_opcion == '3':
                    carpeta = "ingles_basico"
                    ruta = obtener_ruta("tercera.json", carpeta)                  
                    modo_clases(velocidad, ruta)

                elif sub_opcion == '4':
                    carpeta = "ingles_basico"
                    ruta = obtener_ruta("cuarta.json", carpeta)
                    modo_clases(velocidad, ruta)

                elif sub_opcion == '6':
                    print("👋 finalizado")
                    return
                else:
                    print("⚠ Opción no válida, intenta de nuevo.")


        elif opcion == '6':
            #"5. Salir"
            print("👋 Hasta luego")

            break
        else:
            print("❌ Opción inválida")
    
