from huggingface_hub import InferenceClient

# Configuración
TOKEN_HF = "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"
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