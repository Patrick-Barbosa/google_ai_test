import subprocess

env_path = ".env"
chave = 'GEMINI_PROMPT_THEME'
prompt = "criador_prompt.py"
gera_img = "run.py"
avalia_img = "jurado.py"
separando_arquivos = "resultados.py"
upscale = "resultado-sem-filtro.py"
deletando_temp = "delete_temp.py"
catalogador = "catalogador.py"

def atualiza_env(path, key, value):
    try:
        # Lê todas as linhas do .env
        with open(path, "r") as f:
            linhas = f.readlines()

        # Atualiza a linha correspondente
        with open(path, "w") as f:
            for linha in linhas:
                if linha.startswith(key + "="):
                    f.write(f"{key}={value}\n")
                else:
                    f.write(linha)
    except ValueError:
        print(ValueError)
while True:
    try:
        number_generation = int(input("Quantas imagens deseja gerar? (digite somente o número)\n"))
        theme = str(input("Qual tema deseja gerar? (seja curto, de 3 a 5 palavras):\n"))
        atualiza_env(env_path, chave, theme)
        break
    except ValueError:
        print("Entrada inválida. Por favor, insira um número.")

# Gera prompts
for i in range(number_generation):
    print(f"Execução {i+1} do {prompt}")
    subprocess.run(["python3", prompt])

# Gera imagens
print(f"Executando {gera_img}")
subprocess.run(["python3", gera_img])

""" # Avalia as imgens
print(f"Executando {avalia_img}")
subprocess.run(["python3", avalia_img])

# Separando arquivos
print(f"Executando {separando_arquivos}")
subprocess.run(["python3", separando_arquivos])
 """

#Subindo a qualidade das imagens
print(f"Executando {upscale}")
subprocess.run(["python3", upscale])

# Catalogando as imagens
print(f"Executando {catalogador}")
subprocess.run(["python3", catalogador])

#Limpa os arquivos
print(f"Executando {deletando_temp}")
subprocess.run(["python3", deletando_temp])