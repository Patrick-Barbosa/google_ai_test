import json
import os
from pathlib import Path
from google import genai
from google.genai import types
from dotenv import load_dotenv
import time

load_dotenv()

def generate():
    client = genai.Client(
        api_key=os.environ.get("GEMINI_API_KEY"),
    )

    model = "gemini-2.0-flash"
    image_dir = Path("output")
    image_files = list(image_dir.glob("*.[pj][np]g"))
    all_results = []

    for idx, img_path in enumerate(image_files, 1):
        time.sleep(3)
        try:
            # Build prompt with filename
            prompt = f"{os.environ.get('USER_PROMPT')}\nImage name: {img_path.name}\nImage number: {idx}"
            
            # Create parts for this image
            parts = [
                types.Part.from_text(text=prompt),
                types.Part.from_bytes(
                    data=img_path.read_bytes(),
                    mime_type="image/jpeg" if img_path.suffix.lower() in [".jpg", ".jpeg"] else "image/png"
                )
            ]

            # Generate content for single image
            response = client.models.generate_content(
                model=model,
                contents=[types.Content(role="user", parts=parts)],
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    system_instruction=types.Content(
                        parts=[types.Part.from_text(text=os.environ.get("SYS_INSTRUCTIONS"))]
                    )
                )
            )

            # Process response
            if response.text:
                try:
                    result = json.loads(response.text)
                    result["filename"] = img_path.name  # Add filename to result
                    all_results.append(result)
                    print(f"Processed {img_path.name} successfully")
                except json.JSONDecodeError:
                    print(f"Invalid JSON response for {img_path.name}")
                    all_results.append({
                        "filename": img_path.name,
                        "error": "Invalid JSON response"
                    })
            else:
                print(f"Empty response for {img_path.name}")
                all_results.append({
                    "filename": img_path.name,
                    "error": "Empty response"
                })

        except Exception as e:
            print(f"Error processing {img_path.name}: {str(e)}")
            all_results.append({
                "filename": img_path.name,
                "error": str(e)
            })

    # Save all results to JSON
    with open("response.json", "w") as f:
        json.dump(all_results, f, indent=2)
    print("All results saved to response.json")

if __name__ == "__main__":
    generate()