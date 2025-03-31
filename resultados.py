import json
import os
import shutil
import transform as upscale
from pathlib import Path

# Configurações
WEIGHTS = {
    "Visibility": 2,
    "Face_Deformities": 3,
    "Hand/Finger_Deformities": 3,
    "Anatomical_Proportions": 2,
    "AI_Artifacts": 2,
    "Resolution_&_Sharpness": 1
}
TOTAL_WEIGHT = sum(WEIGHTS.values())  # 13
MAX_SCORE = 5 * TOTAL_WEIGHT  # 65

def calculate_score(entry):
    """Calcula o score final baseado nos critérios e pesos"""
    total = 0
    for criterion, weight in WEIGHTS.items():
        total += int(entry[criterion]) * weight
    return round((total / MAX_SCORE) * 100, 2)

def process_images(response_file='response.json'):
    # Carrega os resultados
    with open(response_file, 'r') as f:
        data = json.load(f)

    # Cria diretórios necessários
    Path("accepted").mkdir(exist_ok=True)
    Path("review").mkdir(exist_ok=True)
    Path("rejected").mkdir(exist_ok=True)

    processed_data = []
    
    for entry in data:
        try:
            # Calcula o score
            score = calculate_score(entry)
            status = "accepted" if score >= 70 else "review" if score >= 50 else "rejected"
            
            # Atualiza entrada com novos dados
            new_entry = entry.copy()
            new_entry["score"] = score
            new_entry["status"] = status
            
            # Move a imagem conforme o score
            img_path = Path("output") / entry["filename"]
            if img_path.exists():
                dest_dir = Path(status) / img_path.name
                shutil.move(str(img_path), str(dest_dir))
                new_entry["new_location"] = str(dest_dir)
            else:
                new_entry["error"] = "Original file not found"

            processed_data.append(new_entry)

        except Exception as e:
            new_entry = entry.copy()
            new_entry["error"] = str(e)
            processed_data.append(new_entry)

    # Salva os novos resultados
    with open('processed_response.json', 'w') as f:
        json.dump(processed_data, f, indent=2)
    
    return processed_data

if __name__ == "__main__":
    results = process_images()
    print("Processamento concluído. Resultados:")
    for item in results:
        print(f"{item['filename']}: Score {item.get('score', 'N/A')} → {item.get('status', 'Erro')}")
    upscale.resize_images("accepted", "accepted-transformed", (2304, 1728))
    print("Imagens redimensionadas e salvas em 'accepted-transformed'.")