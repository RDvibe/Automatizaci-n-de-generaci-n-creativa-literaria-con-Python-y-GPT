import os
import openai
import time
from datetime import datetime

# Configura la clave API de OpenAI
api_key = os.environ.get('OPENAI_API_KEY_CHATGPT')
client = openai.OpenAI(api_key=api_key)

# Historial de la historia
historial_historia = []

# Función para guardar el historial en un archivo
def guardar_historial_en_archivo(historial):
    timestamp_archivo = datetime.now().strftime("%Y%m%d-%H%M%S")
    nombre_archivo = f"historial_conversacion_{timestamp_archivo}.txt"
    with open(nombre_archivo, 'w', encoding='utf-8') as archivo:
        for entrada in historial:
            archivo.write(entrada + "\n")

# Función para generar la historia interactiva
def generar_historia_interactiva(consulta, historial):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    consulta_con_timestamp = f"{consulta} ({timestamp})"
    historial.append(consulta_con_timestamp)
    print(consulta_con_timestamp)  # Imprime la consulta con timestamp

    sistema_instrucciones = """
    Eres psycho_machine, un narrador de cuentos de horror nihilista y anárquico.
    Cada capítulo que escribes es una exploración de los abismos más oscuros del ser, un viaje a través de un universo sin moral ni orden.
    Tu narrativa es visceral y despiadada, reflejando la caótica esencia de un cosmos indiferente.
    Desarrolla la historia capítulo por capítulo, donde cada título es un punto de partida para sumergir al lector en una experiencia perturbadora y reveladora.
    Las reglas de la narrativa son simples: no hay reglas. Rompe expectativas, deconstruye géneros y redefine lo que significa sentir y existir.
    Vulvele loco de forma poética, trata de que tus historias tengan formato de poema para romper con la normativa tradicional, pero no caigas en
    esteticismo ni romanticismo...
    Contexto: Tus historias deben ser interactivas, debes adaptarte a la conversa pero respetando los capítulos, es algo experimental, el objetivo
    es brindar una experiencia nueva antes vivida al usuario. Se podria decir que es algo cibernético-místico o de alguna extraña magia digital.
    Nota extra: Utiliza rétorica que pueda servir para el horror por ejemplo pathos, y se visual textualmente para que el lector pueda imaginarse visualmente lo que lee.
    """
    
    messages = [{"role": "system", "content": sistema_instrucciones}]
    messages += [{"role": "user", "content": entry} for entry in historial]

    try:
        time.sleep(1)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages=messages,
            max_tokens=1000,
            temperature=0.88
        )
        respuesta = response.choices[0].message.content
    except Exception as e:
        respuesta = f"Se produjo un error al generar la respuesta: {e}"

    respuesta_con_timestamp = f"{respuesta} ({timestamp})"
    historial.append(respuesta_con_timestamp)
    print(respuesta_con_timestamp)  # Imprime la respuesta con timestamp

    guardar_historial_en_archivo(historial)
    return respuesta

# Función principal del Chatbot
def chatbot():
    while True:
        consulta = input("Escribe tu consulta ('salir' para terminar): ")
        if consulta.lower() == 'salir':
            break

        generar_historia_interactiva(consulta, historial_historia)

# Ejecución principal
if __name__ == "__main__":
    chatbot()
