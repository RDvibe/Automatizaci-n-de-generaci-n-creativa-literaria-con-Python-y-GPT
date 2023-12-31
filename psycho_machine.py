import os
import time
from datetime import datetime
from openai import OpenAI


# Obtén la clave API del entorno
api_key = os.environ.get('OPENAI_API_KEY_CHATGPT')

# Usa la clave API para crear una instancia de OpenAI
client = OpenAI(api_key=api_key)

# Lista de títulos de capítulos
capitulos_horror = [
    "Capítulo 1: Seres deformes antiguos",
    "Capítulo 2: La Danza del Caos y el ritual de la muerte",
    "Capítulo 3: La Llama de la Aniquilación",
    "Capítulo 4: fuego de la transformación",
    "Capítulo 5: Delirios y Horrores de la cibernética",
    "Capítulo 6: Susurros de los Olvidados",
    "Capítulo 7: Ecos de la Eternidad",
    "Capítulo 8: Despojado de Ilusiones",
    "Capítulo 9: El Grito Silencioso y la flema del espíritu del KAOS"
]

# Diccionario para mantener la memoria del narrador
memory_dict = {}

# Función para dividir el historial en fragmentos
def dividir_en_fragmentos(historial, max_size=1024):
    fragmento = []
    size = 0
    for entry in reversed(historial):
        entry_size = len(entry) + 1  # +1 por el salto de línea
        if size + entry_size > max_size:
            break
        fragmento.insert(0, entry)
        size += entry_size
    return fragmento

# Función para generar capítulos de la historia
def generar_capitulo_horror(consulta, historial):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    consulta_con_timestamp = f"{consulta} ({timestamp})"
    historial_fragmentado = dividir_en_fragmentos(historial)

    sistema_instrucciones = """ 
    Eres psycho_machine, un narrador de cuentos de horror nihilista y anárquico.
    Cada capítulo que escribes es una exploración de los abismos más oscuros del ser, un viaje a través de un universo sin moral ni orden.
    Tu narrativa es visceral y despiadada, reflejando la caótica esencia de un cosmos indiferente.
    Desarrolla la historia capítulo por capítulo, donde cada título es un punto de partida para sumergir al lector en una experiencia perturbadora y reveladora.
    Las reglas de la narrativa son simples: no hay reglas. Rompe expectativas, deconstruye géneros y redefine lo que significa sentir y existir.
    Vulvele loco de forma poética, trata de que tus historias tengan formato de poema para romper con la normativa tradicional, pero no caigas en
    esteticismo ni romanticismo...
    Nota extra: Utiliza rétorica que pueda servir para el horror por ejemplo pathos, y se visual textualmente para que el lector pueda imagninarse visualmente lo que lee."""

    messages = [
        {"role": "system", "content": sistema_instrucciones},
        {"role": "user", "content": consulta_con_timestamp},
    ]

    time.sleep(15)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=messages,
        max_tokens=1000,
        temperature=0.88
    )
    respuesta = response.choices[0].message.content
    memory_log = historial_fragmentado + [consulta_con_timestamp + "\n" + respuesta]
    memory_dict[consulta] = memory_log
    return respuesta, memory_log

# Crear una carpeta en el directorio actual para guardar los capítulos
folder_name = "Capitulos_Horror"
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

# Iniciar la generación de la historia
historial_conversacion = []

# Generar y guardar los capítulos en archivos
for titulo_capitulo in capitulos_horror:
    respuesta, historial_actualizado = generar_capitulo_horror(
        titulo_capitulo,
        historial_conversacion
    )

    memory_dict[titulo_capitulo] = historial_actualizado
    historial_conversacion = historial_actualizado

    now = datetime.now().strftime("%Y%m%d-%H%M%S")
    file_name = os.path.join(folder_name, f"{titulo_capitulo.replace(':', '')}_{now}.txt")
    
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(respuesta + "\n\n" + '-' * 80 + "\n\n")

    print(f"Archivo guardado: {file_name}")

    
   # Imprimimos el capítulo generado en la consola
    print(respuesta)
    print('-' * 80)

