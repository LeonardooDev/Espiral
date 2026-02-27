import json
import requests

MODELO_LOCAL = "llama3.2:3b"
URL_OLLAMA = "http://localhost:11434/api/generate"

class ChatLocal:
    def __init__(self):
        """Inicia el motor y precarga el modelo en RAM"""
        print(f"--- DESPERTANDO IA ({MODELO_LOCAL})... ---")
        self._precargar_modelo()

    def _precargar_modelo(self):
        """Envía una señal vacía a Ollama para que suba el modelo a la RAM de una vez"""
        try:
            # Enviamos un prompt vacío solo para que Ollama cargue el archivo
            requests.post(URL_OLLAMA, json={"model": MODELO_LOCAL, "prompt": "", "stream": False}, timeout=15)
        except:
            print("--- AVISO: No se pudo precargar, podría tardar en la primera respuesta ---")

    def obtener_respuesta(self, prompt_usuario: str) -> str:
        """Envía la petición al modelo local"""
        instruccion_sistema = (
            "Responde de forma concisa y directa."
        )

        payload = {
            "model": MODELO_LOCAL,
            "prompt": f"System: {instruccion_sistema}\nUser: {prompt_usuario}",
            "stream": False
        }

        try:
            response = requests.post(URL_OLLAMA, json=payload, timeout=30)
            response.raise_for_status()
            return response.json().get("response", "").strip()
        except Exception as e:
            return f"Error de conexión local: {e}"

if __name__ == "__main__":
    ia = ChatLocal()
    while True:
        entrada = input("Prueba IA: ")
        if entrada.lower() in ["salir", "exit"]:
            break
        print("Espiral:", ia.obtener_respuesta(entrada))