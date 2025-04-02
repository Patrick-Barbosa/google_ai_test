import os
import shutil

# === CONFIGURAÇÕES ===

# Caminho da pasta que será esvaziada
pastas_alvo = [
    "output/",
    "accepted/",
    "review"
]

# Lista de arquivos JSON a serem removidos (com caminho completo ou relativo)
jsons_para_remover = [
    "prompts.json",
    "processed_response.json",
    "response.json"
]

# === 1. Deletar tudo dentro da pasta ===
def esvaziar_pasta(pasta_alvo):
    if os.path.exists(pasta_alvo):
        for item in os.listdir(pasta_alvo):
            item_path = os.path.join(pasta_alvo, item)
            try:
                if os.path.isfile(item_path) or os.path.islink(item_path):
                    os.remove(item_path)
                elif os.path.isdir(item_path):
                    shutil.rmtree(item_path)
                print(f"Removido: {item_path}")
            except Exception as e:
                print(f"Erro ao remover {item_path}: {e}")
    else:
        print(f"Pasta '{pasta_alvo}' não encontrada.")

# === 2. Deletar arquivos JSON específicos ===

def deletar_jsons(jsons_para_remover):
    for json_path in jsons_para_remover:
        if os.path.exists(json_path):
            try:
                os.remove(json_path)
                print(f"JSON removido: {json_path}")
            except Exception as e:
                print(f"Erro ao remover {json_path}: {e}")
        else:
            print(f"JSON não encontrado: {json_path}")

# === EXECUÇÃO ===
# Limpa os arquivos temporários
for pasta in pastas_alvo:
    esvaziar_pasta(pasta)

deletar_jsons(jsons_para_remover)