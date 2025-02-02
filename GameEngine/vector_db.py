import pandas as pd
import numpy as np
import json
import time
import intersystems_iris.dbapi._DBAPI as dbapi

config = {
    "hostname": "localhost",
    "port": 1972,
    "namespace": "USER",
    "username": "demo",
    "password": "demo",
}

def store_user_response(cursor,user_id, scenario, response, trait_scores):
    cursor.execute("""
        INSERT INTO UserResponses (UserID, Scenario, Response, Openness, Conscientiousness, Extraversion, Agreeableness, Neuroticism)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (user_id, scenario, response, *trait_scores.values()))



def create_table(cursor):
    """Create the ActionVectors table if it doesn't exist."""
    try:
        cursor.execute(f"DROP TABLE Actions")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Actions (
                ActionID INT PRIMARY KEY,
                ActionDescription VARCHAR(1000),
                ActionVector VECTOR(DOUBLE, 384),
                OpennessLevel DOUBLE,
                Consciousness FLOAT,
                Extraversion FLOAT,
                Agreeableness FLOAT,
                Neuroticism FLOAT
            )
        """)
        print("Table 'Actions' created or already exists.")
    except Exception as ex:
        print(f"Error creating table: {ex}")
        return False
    return True


def insert_data(cursor, df):
    """Insert data into the Actions table."""
    try:
        data = [
            (
                row['ActionID'],
                row['ActionDescription'],
                str(row['ActionVector']),  # Convert list to string for TO_VECTOR()
                row['OpennessLevel'],
                row['Consciousness'],
                row['Extraversion'],
                row['Agreeableness'],
                row['Neuroticism']
            )
            for index, row in df.iterrows()
        ]

        sql = """
            INSERT INTO Actions
            (ActionID, ActionDescription, ActionVector, OpennessLevel, Consciousness, Extraversion, Agreeableness, Neuroticism)
            VALUES (?, ?, TO_VECTOR(?), ?, ?, ?, ?, ?)
        """
        start_time = time.time()
        cursor.executemany(sql, data)
        end_time = time.time()
        print(f"time taken to add {len(df)} entries: {end_time - start_time} seconds")
    except Exception as ex:
        print(f"Error inserting data: {ex}")


def print_all_tables(cursor):
    """Fetch and print all table names from the database."""
    try:
        # Query to fetch all table names
        query = """
            SELECT TABLE_NAME 
            FROM SYSINFO.TABLES
        """
        cursor.execute(query)
        results = cursor.fetchall()

        # If no tables are found
        if not results:
            print("No tables found in the database.")
            return

        # Print table names
        print(f"\n{'='*80}")
        print(f"{'Table Name'}")
        print(f"{'='*80}")

        for result in results:
            print(result[0])

        print(f"{'='*80}")
    except Exception as ex:
        print(f"Error querying tables: {ex}")


def print_database_items(cursor):
    """Fetch and print all rows from the Actions table."""
    try:
        query = "SELECT * FROM Action"
        cursor.execute(query)

        results = cursor.fetchall()

        if not results:
            print("No data found in the Action table.")
            return

        print(f"\n{'='*80}\n{'ID':<8}{'Description':<30}{'Openness':<12}{'Consciousness':<15}{'Extraversion':<15}{'Agreeableness':<15}{'Neuroticism':<15}{'Vector'}")
        print(f"{'='*80}")

        for result in results:
            action_id, action_description, action_vector, openness_level, consciousness, extraversion, agreeableness, neuroticism = result

            # Check if action_vector is a string and attempt to deserialize it
            if isinstance(action_vector, str):
                try:
                    print(action_vector)
                    action_vector = json.loads(action_vector)
                except json.JSONDecodeError:
                    print(f"Error decoding vector for ActionID {action_id}. Skipping...")
                    continue

            # Ensure action_vector is a list and has expected length
            if isinstance(action_vector, list) and len(action_vector) == 384:
                vector_head = action_vector[:10]
            else:
                vector_head = "Invalid vector format"

            print(f"{action_id:<8}{action_description:<30}{openness_level:<12}{consciousness:<15}{extraversion:<15}{agreeableness:<15}{neuroticism:<15}{vector_head}")

    except Exception as ex:
        print(f"Error querying data: {ex}")


def main():
    with dbapi.connect(**config) as conn:
        with conn.cursor() as cursor:
            # Step 1: Create the table
            if not create_table(cursor):
                print("no table")
                return  # Exit if table creation fails

            # Step 2: Prepare and insert data
            num_rows = 3  # Example number of rows to insert
            action_ids = range(5, num_rows + 5)
            action_descriptions = [
                "Explore new work opportunity",
                "Learn a new language",
                "Take a long vacation"
            ]
            action_vectors = [np.random.rand(384).tolist() for _ in range(num_rows)]  # 3 sample vectors
            openness_levels = np.random.rand(num_rows).tolist()
            consciousness = np.random.rand(num_rows).tolist()
            extraversion = np.random.rand(num_rows).tolist()
            agreeableness = np.random.rand(num_rows).tolist()
            neuroticism = np.random.rand(num_rows).tolist()

            df = pd.DataFrame({
                'ActionID': action_ids,
                'ActionDescription': action_descriptions,
                'ActionVector': action_vectors,
                'OpennessLevel': openness_levels,
                'Consciousness': consciousness,
                'Extraversion': extraversion,
                'Agreeableness': agreeableness,
                'Neuroticism': neuroticism
            })

            # insert_data(cursor, df)

            # Step 3: Print tables and content of the Actions table
            print_all_tables(cursor)
            print_database_items(cursor)

if __name__ == "__main__":
    main()
