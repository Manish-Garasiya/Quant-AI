from .db import db_engine 
from .models import Feature, Stock, Prediction, StrategyRun, TradeModel, Base

def init_database():
    print("Creating database tables...")
    Base.metadata.create_all(bind=db_engine)
    print("Tables created successfully!")

if __name__ == "__main__":
    init_database()
