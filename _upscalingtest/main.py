import cv2
import torch
from realesrgan import RealESRGANer

def upscale_image(imagemPath, width, height, model_path='RealESRGAN_x4plus.pth'):
    """
    Faz o upscale de uma imagem usando o modelo Real-ESRGAN e depois redimensiona para
    as dimensões especificadas (width, height).

    Parâmetros:
        imagemPath (str): Caminho para a imagem de entrada.
        width (int): Largura desejada para a imagem final.
        height (int): Altura desejada para a imagem final.
        model_path (str): Caminho para o arquivo de pesos do modelo Real-ESRGAN.
    
    Retorna:
        output_resized (numpy.ndarray): Imagem com upscale e redimensionada.
    """
    # Carrega a imagem de entrada
    img = cv2.imread(imagemPath)
    if img is None:
        raise ValueError(f"Não foi possível carregar a imagem em {imagemPath}")

    # Define o dispositivo (GPU se disponível, senão CPU)
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    
    # Inicializa o modelo Real-ESRGAN (o parâmetro scale é fixo para este modelo x4)
    model = RealESRGANer(
        scale=4,
        model_path=model_path,
        device=device,
        half=True  # utiliza half precision se estiver usando GPU
    )
    
    # Aplica o upscale usando o modelo
    output, _ = model.enhance(img, outscale=4)
    
    # Redimensiona a imagem para as dimensões desejadas (width x height)
    output_resized = cv2.resize(output, (width, height), interpolation=cv2.INTER_CUBIC)
    
    return output_resized

# Exemplo de uso da função
if __name__ == '__main__':
    input_path = 'image.png'
    output_path = 'imagem_upscaled.png'
    nova_largura = 1024
    nova_altura = 768

    try:
        resultado = upscale_image(input_path, nova_largura, nova_altura)
        cv2.imwrite(output_path, resultado)
        print(f"Imagem upscaled e salva em: {output_path}")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
