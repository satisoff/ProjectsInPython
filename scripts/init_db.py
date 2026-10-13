from dotenv import load_dotenv

from web_portal.config import load_settings
from web_portal.db import init_database


if __name__ == "__main__":
    load_dotenv()
    init_database(load_settings())
    print("Database initialized successfully.")
