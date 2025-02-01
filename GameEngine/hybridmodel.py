# This class is called eveytime a section ends
# Caluclates the scores of the player and sends to personalotyres.py
# Uses sentiment analysis and vectorizer to calculate sentiment

import voyageai
import os
from dotenv import load_dotenv

load_dotenv()

KEY = os.getenv("API_KEY")
vo = voyageai.Client(api_key=KEY)

## Given the text, create an embedded vector


def embed(text):
    # Uses voyage-3-lite: context length = 32,000    embedding dimension = 512
    return vo.embed(text, model="voyage-3-lite", input_type="document")


if __name__=="__main__":
    texts = ["Sample text 1", "Sample text 2"]

    result = embed(texts)
    print("length of vector1: ",len(result.embeddings[0]))
    print("length of vector2: ",len(result.embeddings[1]))