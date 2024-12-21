import snowflake.connector as snowflake  # Snowflake connector
from dotenv import load_dotenv
import os
import pydantic as pd

# Load environment variables
load_dotenv()

PASSWORD = os.getenv('SNOWSQL_PWD')
WAREHOUSE = os.getenv('WAREHOUSE')
ACCOUNT = os.getenv('SNOWSQL_ACCOUNT')
USER = os.getenv('SNOWSQL_USER')
DATABASE = os.getenv('SNOWSQL_DATABASE')
ROLE = os.getenv('SNOWSQL_ROLE')

# Define the Game model
class Game(pd.BaseModel):
    id: int
    name: str
    document: str
    keywords: str
    cover: str
    rating: float
    websites: str

# Decorator to handle SnowSQL connection
def requires_SnowSQL(function):
    """
    Decorator to handle SnowSQL connection.
    This decorator establishes a connection to a Snowflake database using the provided
    credentials and configuration. It then executes the decorated function with a cursor
    object as its first argument, allowing the function to interact with the database.
    
    Args:
        function (callable): The function to be decorated. This function should accept a
                             cursor object as its first argument.
    Returns:
        callable: The wrapped function with an active Snowflake connection.

    """
    def wrapper(*args, **kwargs):
        with snowflake.connect(
            user=USER,  # required
            password=PASSWORD,  # required
            account=ACCOUNT,  # required
            warehouse=WAREHOUSE,
            database=DATABASE,
            schema='PUBLIC',
            role=ROLE
        ) as conn:
            with conn.cursor() as cur:
                return function(cur, *args, **kwargs)
            conn.commit()
    return wrapper

# CRUD operations
@requires_SnowSQL
def search_games(cursor, query, limit):
    """
    Searches for games in the Snowflake database using cortex search with the query as context and a limit.

    Args:
        cursor (object): The database cursor used to execute the query.
        query (str): The search query string that will be embedded and used for context search.
        limit (int): The maximum number of results to return.

    Returns:
        list: A list of Game objects that match the search criteria.
    """
    query = f""" SELECT SNOWFLAKE.CORTEX.SEARCH_PREVIEW (
        'CORTEXPLAY_DB.PUBLIC.GAME_DOCS_SVC',
        '{
            "query": "{query}",
            "columns": ["DOCUMENT", "KEYWORDS"],
            "limit": {limit}
        }' 
    ); 
    """
    cursor.execute(query)
    results = cursor.fetchall()
    return [Game(**result) for result in results]

@requires_SnowSQL
def retrieve_game_by_id(cursor, game_id):
    """
    Retrieve a game record from the database by its ID.

    Args:
        cursor (object): The database cursor to execute the query.
        game_id (int): The ID of the game to retrieve.

    Returns:
        Game: An instance of the Game class populated with the retrieved data if found, otherwise None.
    """
    query = f""" SELECT * FROM GAME_DOCS_SVC WHERE ID = {game_id}; """
    cursor.execute(query)
    result = cursor.fetchone()
    return Game(**result) if result else None

@requires_SnowSQL
def retrieve_game_by_name(cursor, game_name):
    query = f""" SELECT * FROM GAME_DOCS_SVC WHERE NAME = '{game_name}'; """
    cursor.execute(query)
    result = cursor.fetchone()
    return Game(**result) if result else None

@requires_SnowSQL
def insert_game(cursor, game):
    data = Game(**game)
    query = f""" INSERT INTO GAME_DOCS_SVC (ID, NAME, DOCUMENT, KEYWORDS, COVER, RATING, WEBSITES)
                 VALUES ({data.id}, '{data.name}', '{data.document}', '{data.keywords}', '{data.cover}', {data.rating}, '{data.websites}'); """
    cursor.execute(query)

@requires_SnowSQL
def delete_game(cursor, game_id):
    """
    Deletes a game record from the GAME_DOCS_SVC table based on the provided game ID.

    Args:
        cursor (object): The database cursor object used to execute the SQL query.
        game_id (int): The ID of the game to be deleted.

    Returns:
        None
    """
    query = f""" DELETE FROM GAME_DOCS_SVC WHERE ID = {game_id}; """
    cursor.execute(query)

# Test function
def run_tests():
    pass
