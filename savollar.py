from gpt4all import GPT4All

model = GPT4All("codellama-7b-instruct.Q4_0.gguf")
output = model.generate("Python’da ikkita sonni qo‘shish kodi", max_tokens=200)
print(output)
