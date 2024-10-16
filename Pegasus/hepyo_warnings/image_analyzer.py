import warnings
warnings.filterwarnings("ignore", message="`clean_up_tokenization_spaces` was not set")

from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
from deep_translator import GoogleTranslator

# Função para buscar a imagem a partir de uma URL
def fetch_image(url):
    try:
        image = Image.open(requests.get(url, stream=True).raw)
        return image
    except Exception as e:
        print(f"Erro ao baixar a imagem: {e}")
        return None

# Função para gerar uma legenda usando o BLIP
def generate_caption(image):
    try:
        # Carrega o processador e o modelo BLIP
        processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
        model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
        inputs = processor(image, return_tensors="pt")
        
        # Gera a legenda com limite de 50 tokens
        output = model.generate(**inputs, max_new_tokens=250)
        
        # Decodifica a legenda
        caption = processor.decode(output[0], skip_special_tokens=True, clean_up_tokenization_spaces=True)
        
        return caption
    except Exception as e:
        print(f"Erro ao gerar a legenda: {e}")
        return None

# Função para traduzir a legenda usando o deep-translator
def translate_caption(caption, target_language='pt'):
    try:
        translator = GoogleTranslator(source='auto', target=target_language)
        translated_caption = translator.translate(caption)
        return translated_caption + "."
    except Exception as e:
        print(f"Erro ao traduzir a legenda: {e}")
        return None