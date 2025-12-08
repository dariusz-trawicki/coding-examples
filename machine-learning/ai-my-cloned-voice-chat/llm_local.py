from gpt4all import GPT4All

MODEL_PATH = "Meta-Llama-3-8B-Instruct.Q4_0.gguf"

model = GPT4All(MODEL_PATH)

print("GPT4All model initialized:", model)

def chat_reply(prompt: str) -> str:
    with model.chat_session():
        return model.generate(prompt, max_tokens=256)
