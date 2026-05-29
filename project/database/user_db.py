from sqlalchemy import text
from project.database.db_config import get_db_engine
from project.utils.logger import get_logger

logger = get_logger(__name__)

def add_user(username, password_hash):
    """Adds a new user to the database."""
    engine = get_db_engine()
    try:
        with engine.begin() as connection:  # Use begin() for transaction
            # Check if user already exists
            result = connection.execute(
                text("SELECT username FROM users WHERE username = :username"),
                {"username": username}
            ).fetchone()
            if result:
                logger.warning(f"User '{username}' already exists.")
                return False, "User already exists"

            # Insert new user
            connection.execute(
                text("INSERT INTO users (username, password_hash) VALUES (:username, :password_hash)"),
                {"username": username, "password_hash": password_hash}
            )
        logger.info(f"User '{username}' created successfully.")
        return True, "User created successfully"
    except Exception as e:
        logger.error(f"Error adding user '{username}': {e}")
        return False, f"An error occurred: {e}"


def get_user(username):
    """Retrieves a user from the database by username."""
    engine = get_db_engine()
    try:
        with engine.connect() as connection:
            result = connection.execute(
                text("SELECT username, password_hash FROM users WHERE username = :username"),
                {"username": username}
            ).fetchone()
            return result
    except Exception as e:
        logger.error(f"Error retrieving user '{username}': {e}")
        return None
