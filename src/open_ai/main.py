"""
Módulo interactivo para enviar consultas a ChatGPT usando la API de OpenAI.
Permite al usuario interactuar desde consola con historial de entradas.
"""

import json
import os
import readline  # Permite historial de entradas con flechas
from dotenv import load_dotenv
import openai

# Cargar variables de entorno
load_dotenv()

# Obtener la API Key desde .env
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("No se encontró la variable OPENAI_API_KEY en el archivo .env")

# Inicializar el cliente OpenAI
client = openai.OpenAI(api_key=api_key)


def obtener_respuesta_chatgpt(contexto: str, consulta: str) -> str:
    """
    Envía una consulta al modelo de OpenAI y devuelve la respuesta formateada.

    Args:
        contexto (str): Instrucciones para el modelo (rol del sistema).
        consulta (str): Texto de la consulta del usuario.

    Returns:
        str: Respuesta del modelo en formato JSON formateado.
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
        return f"chatGPT: {json.dumps(datos, indent=2, ensure_ascii=False)}"

    except openai.OpenAIError as e:
        if "insufficient_quota" in str(e):
            return ("chatGPT: No tienes crédito suficiente. "
                    "Revisa tu plan en https://platform.openai.com/account/usage")
        return f"chatGPT: Error del modelo: {e}"

    except json.JSONDecodeError as e_json:
        return f"chatGPT: Error al decodificar JSON: {e_json}"

    except Exception as e:  # noqa: W0718
        return f"chatGPT: Error inesperado: {e}"


def main():
    """
    Función principal: ciclo interactivo que permite enviar consultas a ChatGPT.
    """
    contexto = "Responde como un asistente útil que devuelve respuestas claras en JSON."
    ultima_consulta = ""

    while True:
        try:
            user_input = input(
                "Escribe tu consulta para chatGPT (o 'salir' para terminar): ").strip()

            if user_input.lower() == "salir":
                print("Programa terminado.")
                break

            if not user_input:
                print("La consulta está vacía. Por favor, ingresa una pregunta.")
                continue

            readline.add_history(user_input)
            ultima_consulta = user_input

            consulta_formateada = f"You: {user_input}"
            print(consulta_formateada)

            respuesta = obtener_respuesta_chatgpt(contexto, consulta_formateada)
            print(respuesta)

        except KeyboardInterrupt:
            print("\nInterrupción del usuario. Saliendo...")
            break

        except Exception as e:  # noqa: W0718
            print(f"Error inesperado en la entrada: {e}")


if __name__ == "__main__":
    main()
