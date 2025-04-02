import csv
import json  # Adicionado para parsear a resposta do Gemini
import os
from pathlib import Path
from google import genai
from google.genai import types
from dotenv import load_dotenv
import time
from datetime import datetime

load_dotenv()

# Mapeamento de Categorys (número -> nome)
CATEGORIES = {
    1: "Animals",
    2: "Buildings and Architecture",
    3: "Business",
    4: "Beverages",
    5: "Environment",
    6: "Feelings, Emotions, and Mental States",
    7: "Food",
    8: "Graphic Resources",
    9: "Hobbies and Leisure",
    10: "Industry",
    11: "Landscapes",
    12: "Lifestyle",
    13: "People",
    14: "Plants and Flowers",
    15: "Religion and Culture",
    16: "Science",
    17: "Social Issues",
    18: "Sports",
    19: "Technology",
    20: "Transportation",
    21: "Travel"
}

def generate_csv():
    client = genai.Client(
        api_key=os.environ.get("GEMINI_API_KEY"),
    )

    dt_hoje = datetime.now().strftime('%d-%m-%Y')
    pasta_de_hoje = f"{dt_hoje}_generations"

    model = "gemini-2.0-flash"
    image_dir = Path(pasta_de_hoje)  # Pasta com as imagens
    image_files = list(image_dir.glob("*.[pj][np]g"))  # Captura .jpg e .png
    csv_rows = []

    for img_path in image_files:
        time.sleep(5)  # Evita rate limit
        try:
            # Instruções CLARAS para o Gemini (ajuste conforme necessário)
            prompt = f"""
                **Analyze the image and return a STRICT JSON (no markdown, only the JSON) containing:**

                - **`Title`**: A short description (max. 200 characters).
                - **`Keywords`**: 10-20 keywords separated by commas, in order of relevance.
                - **`Category`**: The corresponding number from the list: `{CATEGORIES}`.
                - **`Releases`**: The names of any authorizations (if none, leave it empty).

                **Valid Response Example:**
                {{"Title": "Vintage wine bottle", "Keywords": "wine, bottle, drink, vintage, luxury", "Category": 4, "Releases": ""}}
            """

            parts = [
                types.Part.from_text(text=prompt),
                types.Part.from_bytes(
                    data=img_path.read_bytes(),
                    mime_type="image/jpeg" if img_path.suffix.lower() in [".jpg", ".jpeg"] else "image/png"
                )
            ]

            response = client.models.generate_content(
                model=model,
                contents=[types.Content(role="user", parts=parts)],
                config=types.GenerateContentConfig(
                    response_mime_type="application/json"
                )
            )

            if response.text:
                # Remove possíveis markdown ou textos extras (ex: ```json)
                json_str = response.text.strip().replace('```json', '').replace('```', '')
                data = json.loads(json_str)  # Parseia o JSON
                csv_rows.append({
                    "Filename": img_path.name,
                    "Title": data.get("Title", ""),
                    "Keywords": data.get("Keywords", ""),
                    "Category": data.get("Category", ""),
                    "Releases": data.get("Releases", "")
                })
                print(f"✅ Processado: {img_path.name}")
            else:
                print(f"❌ Erro: Resposta vazia para {img_path.name}")
                csv_rows.append({
                    "Filename": img_path.name,
                    "Title": "",
                    "Keywords": "",
                    "Category": "",
                    "Releases": ""
                })

        except Exception as e:
            print(f"❌ Erro em {img_path.name}: {str(e)}")
            csv_rows.append({
                "Filename": img_path.name,
                "Title": "",
                "Keywords": "",
                "Category": "",
                "Releases": ""
            })

    # Salva o CSV FINAL (sem arquivos temporários)
    with open(f"{pasta_de_hoje}/labels.csv", "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=[
            "Filename", "Title", "Keywords", "Category", "Releases"
        ])
        writer.writeheader()
        writer.writerows(csv_rows)
    print("\n✅ CSV gerado: labels.csv")

if __name__ == "__main__":
    generate_csv()