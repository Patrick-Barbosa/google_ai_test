import os
import json
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

# Captura as variáveis de ambiente necessárias
API_KEY = os.getenv("GEMINI_API_KEY")
SYSTEM_INSTRUCTIONS = os.getenv("GEMINI_CREATING_INSTRUCTIONS")
THEME = os.getenv("GEMINI_PROMPT_THEME")

if not API_KEY or not SYSTEM_INSTRUCTIONS:
    raise EnvironmentError("As variáveis GEMINI_API_KEY e GEMINI_SYSTEM_INSTRUCTIONS devem estar definidas.")

# Inicializa o cliente do Gemini
client = genai.Client(api_key=API_KEY)

# Texto de entrada que instrui o modelo a gerar um prompt detalhado no formato JSON
input_text = (
    f"Generate a good image prompt with the theme: {THEME} and retrieve a JSON object"
)

# Chama a API do Gemini para gerar o prompt usando as system_instructions capturadas
response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=[input_text],
    config=types.GenerateContentConfig(
        system_instruction=SYSTEM_INSTRUCTIONS,
        max_output_tokens=8192,
        temperature=1.3
    )
)

# Captura o texto gerado
generated_prompt_text = str(response.text).replace('```json', '').replace('```', '').strip()

# Tenta interpretar o resultado como JSON
try:
    print(generated_prompt_text)
    generated_prompt = json.loads(generated_prompt_text)
except json.JSONDecodeError as e:
    raise ValueError("A resposta da API não é um JSON válido: " + str(e))

# Define o caminho do arquivo de prompts
PROMPTS_FILE = "prompts.json"

# Carrega o conteúdo atual do arquivo (se existir)
if os.path.exists(PROMPTS_FILE):
    with open(PROMPTS_FILE, "r", encoding="utf-8") as f:
        try:
            prompts_data = json.load(f)
        except json.JSONDecodeError:
            prompts_data = []
else:
    prompts_data = []

# Adiciona o novo prompt à lista
prompts_data.append(generated_prompt)

# Salva (apenda) o novo conteúdo no arquivo prompts.json
with open(PROMPTS_FILE, "w", encoding="utf-8") as f:
    json.dump(prompts_data, f, ensure_ascii=False, indent=2)

print("Novo prompt gerado e adicionado ao arquivo prompts.json.")
