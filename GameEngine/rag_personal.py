import os
import anthropic
import getpass
import time


import numpy as np
import intersystems_iris.dbapi as iris
from sentence_transformers import SentenceTransformer
from langchain_anthropic import ChatAnthropic

from sklearn.metrics.pairwise import cosine_similarity
import intersystems_iris.dbapi._DBAPI as dbapi


if not os.environ.get("ANTHROPIC_API_KEY"):
  os.environ["ANTHROPIC_API_KEY"] = ""


model = ChatAnthropic(model="claude-3-5-sonnet-20240620")

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")


config = {
    "hostname": "localhost",
    "port": 1972,
    "namespace": "USER",
    "username": "demo",
    "password": "demo",
}


# Load embedding model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

conn = dbapi.connect(**config)
cursor = conn.cursor()

# Drop table if exists
table_name = "Psychology.PersonalityEmbeddings"

try:
    cursor.execute(f"DROP TABLE {table_name}")  
except Exception as e:
    print(f"Table drop failed: {e}")

# Create table with vector storage
table_definition = """(
    ID SERIAL PRIMARY KEY,
    Trait VARCHAR(50),
    Description TEXT,
    Embedding VECTOR(DOUBLE, 384)
)"""
cursor.execute(f"CREATE TABLE {table_name} {table_definition}")

print("Table created successfully.")

# Define personality descriptions
personality_data = [
    ("Openness", "People high in Openness enjoy creativity, abstract thinking, and exploring new ideas."),
    ("Openness", "Individuals with high Openness scores embrace novelty and diverse perspectives."),
    ("Conscientiousness", "Conscientious individuals are detail-oriented, highly disciplined, and reliable."),
    ("Conscientiousness", "These individuals excel in structured environments requiring organization."),
    ("Extraversion", "Extraverts are energized by social interactions and enjoy engaging with people."),
    ("Extraversion", "Extraverts thrive in leadership and social settings."),
    ("Agreeableness", "Agreeable people are empathetic, cooperative, and focus on maintaining harmony."),
    ("Agreeableness", "Highly agreeable individuals prioritize social bonds and kindness."),
    ("Neuroticism", "Neurotic individuals experience higher stress and emotional instability."),
    ("Neuroticism", "These individuals are more prone to anxiety and mood swings."),
]

# SQL query for insertion
insert_sql = f"""
    INSERT INTO {table_name} (Trait, Description, Embedding)
    VALUES (?, ?, TO_VECTOR(?))
"""

# Prepare data for batch insert
start_time = time.time()
batch_data = [
    (trait, description, str(embedding_model.encode(description).tolist()))
    for trait, description in personality_data
]

# Insert data into IRIS
cursor.executemany(insert_sql, batch_data)

end_time = time.time()
print(f"Time taken to add {len(personality_data)} entries: {end_time - start_time} seconds")


from sklearn.metrics.pairwise import cosine_similarity

# Function to find similar personality traits
def retrieve_relevant_personality(user_input, top_k=3):
    # Convert user input to embedding
    user_embedding = embedding_model.encode([user_input])

    # Fetch stored embeddings
    cursor.execute(f"SELECT ID, Trait, Description, Embedding FROM {table_name}")
    stored_data = cursor.fetchall()

    # Extract embeddings for similarity comparison
    stored_embeddings = [np.array(eval(row[3])) for row in stored_data]  # Convert from string to array
    similarities = cosine_similarity(user_embedding, stored_embeddings)[0]

    # Retrieve top-K most relevant traits
    top_indices = np.argsort(similarities)[-top_k:][::-1]
    top_traits = [(stored_data[i][1], stored_data[i][2]) for i in top_indices]

    return top_traits


user_response = "I enjoy exploring new cultures and challenging traditional ideas."
print(retrieve_relevant_personality(user_response))


def store_user_response(user_id, scenario, response, trait_scores):
    sql = f"""
        INSERT INTO Psychology.UserPersonalityScores 
        (UserID, Scenario, Response, Openness, Conscientiousness, Extraversion, Agreeableness, Neuroticism)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """
    cursor.execute(sql, (user_id, scenario, response, *trait_scores.values()))