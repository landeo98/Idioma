import os
import random
import shlex
import platform

def shadowing_parrafos(carpeta, pronunciar_palabra, velocidad=150):
    """
    Shadowing con párrafos completos, soporta párrafos multilínea.
    - carpeta: ruta donde están los .txt
    - pronunciar_palabra: función que reproduce TTS (Windows/Termux)
    - velocidad: velocidad de pronunciación
    """
    # Lista todos los archivos .txt de la carpeta
    archivos = [f for f in os.listdir(carpeta) if f.endswith(".txt")]
    if not archivos:
        print("⚠️ No hay archivos .txt en la carpeta")
        return

    archivo_elegido = random.choice(archivos)
    ruta = os.path.join(carpeta, archivo_elegido)

    print(f"\n🎲 Leyendo aleatoriamente: {archivo_elegido}\n")

    # Leer líneas crudas del archivo
    with open(ruta, "r", encoding="utf-8") as f:
        lineas_raw = f.readlines()

    # Unir líneas en párrafos completos
    parrafos = []
    parrafo_temp = []
    for linea in lineas_raw:
        linea = linea.strip()
        if not linea:  # línea en blanco = fin de párrafo
            if parrafo_temp:
                parrafos.append(" ".join(parrafo_temp))
                parrafo_temp = []
        else:
            parrafo_temp.append(linea)
    if parrafo_temp:
        parrafos.append(" ".join(parrafo_temp))  # último párrafo

    # Procesar cada párrafo
    for parrafo_completo in parrafos:
        # Separar párrafo y traducción usando '||'
        if "||" in parrafo_completo:
            parrafo, trad = map(str.strip, parrafo_completo.split("||"))
        else:
            parrafo, trad = parrafo_completo, ""

        print(parrafo)                        # Mostrar párrafo en inglés
        pronunciar_palabra(parrafo, velocidad) # Pronunciar con TTS
        if trad:
            print(f"   ↳ {trad}")             # Mostrar traducción
        input("Presiona Enter para siguiente párrafo...")  # Pausa opcional

    print("\n✅ Fin del archivo\n")






