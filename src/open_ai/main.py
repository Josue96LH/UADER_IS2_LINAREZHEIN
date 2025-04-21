import json
import os
from dotenv import load_dotenv
import openai

# Cargar variables de entorno desde archivo .env
load_dotenv()

# Obtener la API Key desde variable de entorno
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("No se encontró la variable OPENAI_API_KEY en el archivo .env")

# Inicializar el cliente de OpenAI
client = openai.OpenAI(api_key=api_key)


def obtener_respuesta_chatgpt(contexto: str, consulta: str) -> str:
    """
    Realiza una consulta al modelo GPT de OpenAI y devuelve la respuesta como texto.
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
    except openai.OpenAIError as e:
        if "insufficient_quota" in str(e):
            return "chatGPT: No tienes crédito suficiente en tu cuenta de OpenAI. Revisa tu plan en https://platform.openai.com/account/usage"
        return f"chatGPT: Error al obtener respuesta del modelo: {e}"
    except Exception as e:
        return f"chatGPT: Error inesperado: {e}"


def main():
    """
    Función principal con manejo de errores en tres niveles:
    1. Entrada del usuario
    2. Procesamiento/formateo
    3. Llamada al modelo
    """
    contexto = "Responde como un asistente útil que devuelve respuestas claras en JSON."

    try:
        # Nivel 1: Aceptar entrada
        user_input = input("Escribe tu consulta para chatGPT: ").strip()
        if not user_input:
            print("La consulta está vacía. Por favor, ingresa una pregunta.")
            return

        try:
            # Nivel 2: Procesamiento
            consulta_formateada = f"You: {user_input}"
            print(consulta_formateada)

            try:
                # Nivel 3: Llamada al modelo
                respuesta = obtener_respuesta_chatgpt(contexto, consulta_formateada)
                print(respuesta)

            except Exception as e_modelo:
                print(f"Error al invocar el modelo: {e_modelo}")

        except Exception as e_proceso:
            print(f"Error al procesar la entrada: {e_proceso}")

    except Exception as e_entrada:
        print(f"Error al leer la entrada del usuario: {e_entrada}")


if __name__ == "__main__":
    main()
