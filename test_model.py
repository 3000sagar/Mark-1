from models.ollama_model import OllamaModel

model = OllamaModel()

response = model.generate("Say hello like a robot")
print(response)