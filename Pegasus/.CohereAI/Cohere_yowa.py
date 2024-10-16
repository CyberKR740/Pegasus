from deep_translator import GoogleTranslator
import cohere

class CohereResponsePipeline:
    def __init__(self, api_key):
        self.cohere_client = cohere.Client(api_key)
        self.translator = GoogleTranslator(source='auto', target='en')

    def cohere_respond_pipeline(self, prompt, max_tokens=43, temperature=0.7, p=0.9):
        translated_prompt = self.translator.translate(prompt)

        try:
            response = self.cohere_client.generate(
                model='command-xlarge-nightly',
                prompt=translated_prompt,
                max_tokens=max_tokens,
                temperature=temperature,
                p=p,
                return_likelihoods='NONE'
            )

            response_in_english = response.generations[0].text.strip()
            translated_response = GoogleTranslator(source='en', target='pt').translate(response_in_english)

            return translated_response

        except Exception as e:
            return f"Erro ao gerar resposta: {e}"