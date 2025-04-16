import json
import os
from dotenv import load_dotenv
import openai

# Cargar variables de entorno desde archivo .env
load_dotenv()

# Obtener la API Key de la variable de entorno
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("No se encontró la variable OPENAI_API_KEY en el archivo .env")

# Inicializar el cliente de OpenAI
client = openai.OpenAI(api_key=api_key)

def obtener_respuesta_chatgpt(contexto: str, consulta: str) -> str:
    """
    Realiza una consulta al modelo GPT de OpenAI y devuelve la respuesta en texto.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini-2024-07-18",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": contexto},
                {"role": "user", "content": consulta}
            ],
            temperature=1,
            max_tokens=16384,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        respuesta_json = response.choices[0].message.content
        datos = json.loads(respuesta_json)
        return f"chatGPT: {json.dumps(datos, indent=2)}"
    except Exception as e:
        return f"chatGPT: Error al obtener respuesta del modelo: {e}"

def main():
    """
    Función principal que captura una consulta del usuario, valida su contenido,
    e imprime tanto la consulta como la respuesta de chatGPT.
    """
    contexto = "Responde como un asistente útil que devuelve respuestas claras en JSON."
    user_input = input("Escribe tu consulta para chatGPT: ").strip()

    if not user_input:
        print("La consulta está vacía. Por favor, ingresa una pregunta.")
        return

    consulta_formateada = f"You: {user_input}"
    print(consulta_formateada)

    respuesta = obtener_respuesta_chatgpt(contexto, consulta_formateada)
    print(respuesta)

if __name__ == "__main__":
    main()
