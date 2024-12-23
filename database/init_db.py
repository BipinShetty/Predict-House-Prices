import sqlite3
import pandas as pd

class DatabaseHandler:
    def __init__(self, db_name="real_estate.db"):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name, check_same_thread=False)

    def initialize_database(self, data_path):
            data = pd.read_csv(data_path)

            # Normalize column names
            data.columns = [col.strip().replace(' ', '').replace('/', '').lower() for col in data.columns]

            # Required columns
            required_columns = [
                'lotarea', 'overallqual', 'overallcond', 'centralair',
                'fullbath', 'bedroomabvgr', 'garagecars', 'saleprice'
            ]

            missing_columns = set(required_columns) - set(data.columns)
            if missing_columns:
                raise KeyError(f"Dataset is missing one or more required columns: {missing_columns}")

            # Convert Central Air to numeric (Y -> 1, N -> 0)
            data['centralair'] = data['centralair'].map({'Y': 1, 'N': 0}).fillna(0)

            # Ensure all required columns are numeric
            for col in required_columns:
                data[col] = pd.to_numeric(data[col], errors='coerce').fillna(0)

            data['datasource'] = 1  # Add datasource column
            data.to_sql("properties", self.conn, if_exists="replace", index=False)
            print(f"Database initialized at {self.db_name}")

            # Create additional tables if they don't exist
            self.conn.execute("""
                   CREATE TABLE IF NOT EXISTS listings (
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       description TEXT NOT NULL
                   )
               """)
            self.conn.execute("DROP TABLE IF EXISTS feedback")
            self.conn.execute("""
                    CREATE TABLE IF NOT EXISTS feedback (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        listing TEXT,
                        feedback TEXT
                    );
                    """)
            print(f"Database initialized at {self.db_name}")


    def add_verified_price(self, price, lot_area, overall_quality, overall_condition, central_air, full_bath, bedrooms,
                           garage_cars):
        """
        Save a verified sale price and its associated features to the database.
        """
        query = """
        INSERT INTO properties (SalePrice, LotArea, OverallQual, OverallCond, CentralAir, FullBath, BedroomAbvGr, GarageCars, datasource)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        with self.conn as conn:
            conn.execute(query, (
            price, lot_area, overall_quality, overall_condition, central_air, full_bath, bedrooms, garage_cars, 2))
            conn.commit()
            print("Verified sale price added successfully!")

    def record_listing(self, listing):
        self.conn.execute("INSERT INTO listings (description) VALUES (?)", (listing,))
        self.conn.commit()

    def record_feedback(self, listing, feedback):
        self.conn.execute("INSERT INTO feedback (listing, feedback) VALUES (?, ?)", (listing, feedback))
        self.conn.commit()

    def get_full_data_for_features(self, features):
        query = """
        SELECT * FROM properties 
        WHERE lotarea = ? OR overallqual = ? OR overallcond = ? OR centralair = ?
        OR fullbath = ? OR bedroomabvgr = ? OR garagecars = ?
        ORDER BY yrsold DESC LIMIT 1
        """
        cursor = self.conn.execute(query, features)
        return cursor.fetchone()

    def get_closest_match(self, inputs):
        """
        Retrieve the closest match from the database for the given input features.
        :param inputs: A tuple of input values in the order:
                       (lot_area, overall_quality, overall_condition, central_air, full_bath, bedrooms, garage_cars)
        :return: A dictionary containing the closest match property details or None if no match is found.
        """
        query = """
        SELECT *, 
       ABS(LotArea - ?) / MAX(LotArea) AS lot_area_diff,
       ABS(OverallQual - ?) / MAX(OverallQual) AS overall_quality_diff,
       ABS(OverallCond - ?) / MAX(OverallCond) AS overall_condition_diff,
       ABS(CentralAir - ?) AS central_air_diff,
       ABS(FullBath - ?) / MAX(FullBath) AS full_bath_diff,
       ABS(BedroomAbvGr - ?) / MAX(BedroomAbvGr) AS bedrooms_diff,
       ABS(GarageCars - ?) / MAX(GarageCars) AS garage_cars_diff,
       (ABS(LotArea - ?) / MAX(LotArea) +
        ABS(OverallQual - ?) / MAX(OverallQual) +
        ABS(OverallCond - ?) / MAX(OverallCond) +
        ABS(CentralAir - ?) +
        ABS(FullBath - ?) / MAX(FullBath) +
        ABS(BedroomAbvGr - ?) / MAX(BedroomAbvGr) +
        ABS(GarageCars - ?) / MAX(GarageCars)) AS total_diff
FROM properties
ORDER BY total_diff ASC, YrSold DESC
LIMIT 1
        """

        # The inputs are repeated for each difference calculation and total_diff
        params = inputs * 2

        cursor = self.conn.execute(query, params)
        result = cursor.fetchone()

        if result:
            # Map the result to a dictionary
            columns = [col[0] for col in cursor.description]
            closest_match = dict(zip(columns, result))
            return closest_match
        else:
            return None

