import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

# Holaaa, esto es una prueba

# Esto tambien es una prueba

# Prueba 3 

load_dotenv() # Esto carga el archivo .env
TOKEN_HF = os.getenv("TOKEN_HF") # Lee la variable sin mostrarla en el código

client_ia = InferenceClient("Qwen/Qwen2.5-72B-Instruct", token=TOKEN_HF)

def chat():
    print("--- IA SISTEMA ---")
    while True:
        user_input = input("Tú: ")
        if user_input.lower() in ["salir", "exit"]:
            break
            
        try:
            response = client_ia.chat_completion(
                messages=[{"role": "user", "content": user_input}],
                max_tokens=300
            )
            
            respuesta = response.choices[0].message.content
            print("IA:", respuesta)
            
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    chat()