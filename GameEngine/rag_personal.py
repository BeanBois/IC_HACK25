import os
import anthropic
import getpass
import time
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage



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
    # Openness
    ("Openness", "People high in Openness enjoy creativity, abstract thinking, and exploring new ideas."),
    ("Openness", "Individuals with high Openness scores embrace novelty and diverse perspectives."),
    ("Openness", "Open individuals often seek out intellectual challenges and artistic experiences."),
    ("Openness", "People with high Openness enjoy philosophical discussions and abstract thinking."),
    ("Openness", "Openness is associated with curiosity, imagination, and appreciation of beauty."),
    ("Openness", "Those high in Openness are willing to experiment with new ways of thinking and living."),
    ("Openness", "Open-minded individuals often enjoy literature, music, and innovative technologies."),
    
    # Conscientiousness
    ("Conscientiousness", "Conscientious individuals are detail-oriented, highly disciplined, and reliable."),
    ("Conscientiousness", "These individuals excel in structured environments requiring organization."),
    ("Conscientiousness", "Conscientious people set long-term goals and work diligently to achieve them."),
    ("Conscientiousness", "People high in Conscientiousness tend to be punctual, careful, and self-disciplined."),
    ("Conscientiousness", "A strong work ethic and responsibility are key traits of highly conscientious people."),
    ("Conscientiousness", "Highly conscientious individuals are good at planning and avoiding impulsive actions."),
    ("Conscientiousness", "Conscientious people follow rules carefully and strive for excellence in their work."),

    # Extraversion
    ("Extraversion", "Extraverts are energized by social interactions and enjoy engaging with people."),
    ("Extraversion", "Extraverts thrive in leadership and social settings."),
    ("Extraversion", "People high in Extraversion tend to be outgoing, talkative, and sociable."),
    ("Extraversion", "Extraverted individuals are often enthusiastic and seek excitement."),
    ("Extraversion", "Those who score high in Extraversion enjoy group activities and team projects."),
    ("Extraversion", "Extraverts prefer stimulating environments and are comfortable in large gatherings."),
    ("Extraversion", "Highly extraverted individuals are assertive and often take the initiative in conversations."),

    # Agreeableness
    ("Agreeableness", "Agreeable people are empathetic, cooperative, and focus on maintaining harmony."),
    ("Agreeableness", "Highly agreeable individuals prioritize social bonds and kindness."),
    ("Agreeableness", "Agreeable people tend to be trusting, generous, and compassionate."),
    ("Agreeableness", "Individuals high in Agreeableness enjoy helping others and working in teams."),
    ("Agreeableness", "People with high Agreeableness value relationships and strive to avoid conflicts."),
    ("Agreeableness", "Agreeable individuals tend to be forgiving and supportive in difficult situations."),
    ("Agreeableness", "Highly agreeable people are good listeners and show genuine concern for others."),

    # Neuroticism
    ("Neuroticism", "Neurotic individuals experience higher stress and emotional instability."),
    ("Neuroticism", "These individuals are more prone to anxiety and mood swings."),
    ("Neuroticism", "High Neuroticism is associated with sensitivity to stress and negative emotions."),
    ("Neuroticism", "People with high Neuroticism may overthink situations and experience frequent worry."),
    ("Neuroticism", "Those scoring high in Neuroticism often react strongly to criticism or setbacks."),
    ("Neuroticism", "Neurotic individuals may struggle with self-doubt and feelings of insecurity."),
    ("Neuroticism", "People with high Neuroticism are more likely to feel overwhelmed by daily challenges."),
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


# Precomputed trait embeddings for each of the Big Five traits
trait_embeddings = {
    "Openness": embedding_model.encode("People high in Openness enjoy creativity, abstract thinking, and exploring new ideas."),
    "Conscientiousness": embedding_model.encode("Conscientious individuals are detail-oriented, highly disciplined, and reliable."),
    "Extraversion": embedding_model.encode("Extraverts are energized by social interactions and enjoy engaging with people."),
    "Agreeableness": embedding_model.encode("Agreeable people are empathetic, cooperative, and focus on maintaining harmony."),
    "Neuroticism": embedding_model.encode("Neurotic individuals experience higher stress and emotional instability."),
}

def compute_personality_affinity(user_response):
    response_embedding = embedding_model.encode([user_response])  # Embed the user's response

    # Calculate cosine similarity between response and personality traits
    trait_scores = {
        trait: float(cosine_similarity([response_embedding], [trait_vec])[0][0])
        for trait, trait_vec in trait_embeddings.items()
    }
    
    return trait_scores


def store_user_response(user_id, scenario, response, trait_scores):
    sql = f"""
        INSERT INTO Psychology.UserPersonalityScores 
        (UserID, Scenario, Response, Openness, Conscientiousness, Extraversion, Agreeableness, Neuroticism)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """
    cursor.execute(sql, (user_id, scenario, response, *trait_scores.values()))



def query_model(model,user_responses):
    rt = retrieve_relevant_personality(user_responses)
    score = compute_personality_affinity(user_responses)

    context = [
            SystemMessage(f"This is the relavent context given the user input to a disaster scenrio {rt} and there 5 scores {score}"),
            HumanMessage("Give me a summary of the user strenghs and weakness and adivce giving their 5 behaviour traits")]

    response = model.invoke(context).content

    return response
