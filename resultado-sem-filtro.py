from pathlib import Path
from datetime import datetime
from up import ImageUpscaler

if __name__ == "__main__":
    dt_hoje = datetime.now().strftime('%d-%m-%Y')
    pasta_de_hoje = f"{dt_hoje}_generations"

    Path(pasta_de_hoje).mkdir(exist_ok=True)
    upscaler = ImageUpscaler(new_dpi=600)
    upscaler.upscale_folder(
        input_folder="output",
        output_folder= pasta_de_hoje
    )