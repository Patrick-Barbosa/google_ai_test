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
    max_retries = 3
    timeout = 60  # seconds

    for item in prompts:
        success = False
        attempts = 0
        
        while not success and attempts < max_retries:
            attempts += 1
            print(f"Generating image for: {item['filename']} (Attempt {attempts}/{max_retries})")
            
            try:
                contents = [
                    types.Content(
                        role="user",
                        parts=[types.Part.from_text(text=item["prompt"])]
                    )
                ]

                generate_content_config = types.GenerateContentConfig(
                    temperature=0.45,
                    response_modalities=["image", "text"],
                    response_mime_type="text/plain"
                )

                start_time = time.time()
                image_generated = False

                for chunk in client.models.generate_content_stream(
                    model=model,
                    contents=contents,
                    config=generate_content_config,
                ):
                    if time.time() - start_time > timeout:
                        print(f"Timeout for {item['filename']} after {timeout} seconds")
                        break

                    if not chunk.candidates:
                        print(f"No candidates in response for {item['filename']}")
                        continue

                    if not chunk.candidates[0].content:
                        print(f"No content in response for {item['filename']}")
                        continue

                    if not chunk.candidates[0].content.parts:
                        print(f"No parts in response for {item['filename']}")
                        continue

                    if chunk.candidates[0].content.parts[0].inline_data:
                        inline_data = chunk.candidates[0].content.parts[0].inline_data
                        file_extension = mimetypes.guess_extension(inline_data.mime_type)
                        save_binary_file(
                            f"output/{item['filename']}{file_extension}", inline_data.data
                        )
                        print(f"Saved: output/{item['filename']}{file_extension}")
                        success = True
                        image_generated = True
                        break
                    else:
                        print(f"Debug - Response text: {chunk.text}")

                if not image_generated:
                    print(f"Failed to generate image for {item['filename']}")
                    if attempts < max_retries:
                        print(f"Waiting 5 seconds before retry...")
                        time.sleep(5)

            except Exception as e:
                print(f"Error generating {item['filename']}: {str(e)}")
                if attempts < max_retries:
                    print(f"Waiting 5 seconds before retry...")
                    time.sleep(5)

        if not success:
            print(f"Failed to generate {item['filename']} after {max_retries} attempts")

if __name__ == "__main__":
    # Create output directory if it doesn't exist
    os.makedirs("output", exist_ok=True)
    generate_images()