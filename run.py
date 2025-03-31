import json
import os
import mimetypes
from google import genai
from google.genai import types
from dotenv import load_dotenv
import time

load_dotenv()

def save_binary_file(file_name, data):
    with open(file_name, "wb") as f:
        f.write(data)

def load_prompts(json_file):
    with open(json_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def generate_images():
    client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
    model = "gemini-2.0-flash-exp-image-generation"
    prompts = load_prompts('prompts.json')

    for item in prompts:
        time.sleep(20)
        print(f"Generating image for: {item['filename']}")
        
        contents = [
            types.Content(
                role="user",
                parts=[types.Part.from_text(text=item["prompt"])]
            )
        ]

        generate_content_config = types.GenerateContentConfig(
            temperature=0.65,
            response_modalities=["image", "text"],
            response_mime_type="text/plain"
        )
        

        for chunk in client.models.generate_content_stream(
            model=model,
            contents=contents,
            config=generate_content_config,
        ):
            if not chunk.candidates or not chunk.candidates[0].content or not chunk.candidates[0].content.parts:
                continue
                
            if chunk.candidates[0].content.parts[0].inline_data:
                inline_data = chunk.candidates[0].content.parts[0].inline_data
                file_extension = mimetypes.guess_extension(inline_data.mime_type)
                save_binary_file(
                    f"output/{item['filename']}{file_extension}", inline_data.data
                )
                print(f"Saved: output/{item['filename']}{file_extension}")
            else:
                print(chunk.text)

if __name__ == "__main__":
    # Create output directory if it doesn't exist
    os.makedirs("output", exist_ok=True)
    generate_images()