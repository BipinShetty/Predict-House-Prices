import logging
import sqlite3
import pandas as pd

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class DatabaseHandler:
    def __init__(self, db_name="real_estate.db"):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name, check_same_thread=False)
        logging.info(f"Connected to database: {self.db_name}")

    def initialize_database(self, data_path):
        try:
            data = pd.read_csv(data_path)
            data.columns = [col.strip().replace(' ', '').replace('/', '').lower() for col in data.columns]

            required_columns = [
                'lotarea', 'overallqual', 'overallcond', 'centralair',
                'fullbath', 'bedroomabvgr', 'garagecars', 'saleprice'
            ]
            missing_columns = set(required_columns) - set(data.columns)
            if missing_columns:
                raise KeyError(f"Missing required columns: {missing_columns}")

            data['centralair'] = data['centralair'].map({'Y': 1, 'N': 0}).fillna(0)
            for col in required_columns:
                data[col] = pd.to_numeric(data[col], errors='coerce').fillna(0)

            data['datasource'] = 1
            data.to_sql("properties", self.conn, if_exists="replace", index=False)
            logging.info("Database initialized with Ames Housing data.")

            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS listings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    description TEXT NOT NULL
                )
            """)
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS feedback (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    listing TEXT,
                    feedback TEXT
                )
            """)
            logging.info("Tables created successfully.")
        except Exception as e:
            logging.error(f"Error initializing database: {e}")
            raise

    def add_verified_price(self, *inputs):
        try:
            query = """
            INSERT INTO properties (SalePrice, LotArea, OverallQual, OverallCond, CentralAir, FullBath, BedroomAbvGr, GarageCars, datasource)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            self.conn.execute(query, (*inputs, 2))
            self.conn.commit()
            logging.info("Verified sale price added successfully!")
        except Exception as e:
            logging.error(f"Error adding verified price: {e}")
            raise
