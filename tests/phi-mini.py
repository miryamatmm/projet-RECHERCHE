from transformers import pipeline

messages = [
    {"role": "user", "content": "Who are you?"},
]
pipe = pipeline("text-generation", model="unsloth/Phi-3.5-mini-instruct")
output = pipe(messages)
print(output)