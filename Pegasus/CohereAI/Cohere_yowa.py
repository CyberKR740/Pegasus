from deep_translator import GoogleTranslator
import cohere

class CohereResponsePipeline:
    def __init__(self, api_key):
        self.cohere_client = cohere.Client(api_key)
        self.translator = GoogleTranslator(source='auto', target='en')

    def traduzir(self, texto, idioma_destino):
        try:
            return GoogleTranslator(source='auto', target=idioma_destino).translate(texto)
        except Exception as e:
            return f"Erro na tradução: {e}"

    def cohere_respond_pipeline(self, prompt, max_tokens=300, temperature=0.7, p=0.9):
        prompt_traduzido = self.traduzir(prompt, 'en')

        try:
            # Gerar a resposta usando a API do Cohere
            resposta = self.cohere_client.generate(
                model='command-xlarge-nightly',
                prompt=prompt_traduzido,
                max_tokens=max_tokens,  # Definindo um número maior para tokens
                temperature=temperature,
                p=p,
                return_likelihoods='NONE'
            )

            # Obter o texto gerado em inglês
            resposta_ingles = resposta.generations[0].text.strip()

            # Traduzir a resposta de volta para português
            resposta_traduzida = self.traduzir(resposta_ingles, 'pt')

            return resposta_traduzida

        except Exception as e:
            return f"Erro ao gerar resposta: {e}"