import json
import os
import readline  # <-- NUEVO: permite historial con teclas
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
        return f"chatGPT: {json.dumps(datos, indent=2, ensure_ascii=False)}"
    except openai.OpenAIError as e:
        if "insufficient_quota" in str(e):
            return "chatGPT: No tienes crédito suficiente en tu cuenta de OpenAI. Revisa tu plan en https://platform.openai.com/account/usage"
        return f"chatGPT: Error al obtener respuesta del modelo: {e}"
    except Exception as e:
        return f"chatGPT: Error inesperado: {e}"


def main():
    """
    Función principal con historial: permite recuperar la última consulta con flecha arriba.
    """
    contexto = "Responde como un asistente útil que devuelve respuestas claras en JSON."
    ultima_consulta = ""

    while True:
        try:
            # Nivel 1: Entrada del usuario
            user_input = input("Escribe tu consulta para chatGPT (o 'salir' para terminar): ").strip()

            if user_input.lower() == "salir":
                print("Programa terminado.")
                break

            if not user_input:
                print("La consulta está vacía. Por favor, ingresa una pregunta.")
                continue

            # Guardar en historial de readline
            readline.add_history(user_input)
            ultima_consulta = user_input  # guardar para referencia (opcional)

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

        except KeyboardInterrupt:
            print("\nInterrupción del usuario. Saliendo...")
            break
        except Exception as e_entrada:
            print(f"Error al leer la entrada del usuario: {e_entrada}")


if __name__ == "__main__":
    main()
