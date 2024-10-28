# database.py
from sqlalchemy import create_engine, Column, Integer, String, Float, MetaData, Table
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Replace with your database connection string
DATABASE_URL = "postgresql://username:password@localhost:5432/predictions_db"

engine = create_engine(DATABASE_URL)
metadata = MetaData()

# Define predictions table
predictions_table = Table(
    "predictions", metadata,
    Column("id", Integer, primary_key=True),
    Column("model_name", String),
    Column("prediction", Float),
    Column("timestamp", String),
)

metadata.create_all(engine)
Session = sessionmaker(bind=engine)

def store_prediction_in_db(model_name, prediction):
    session = Session()
    try:
        prediction_entry = {
            "model_name": model_name,
            "prediction": prediction,
            "timestamp": datetime.utcnow().isoformat()
        }
        session.execute(predictions_table.insert().values(prediction_entry))
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Error storing prediction in database: {e}")
    finally:
        session.close()
