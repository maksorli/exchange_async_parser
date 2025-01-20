from repository.models import Spimex
from sqlalchemy.orm import Session


class Repository:
    def __init__(self, db: Session):
        self.db = db

    def save_product(self, product_data):
        product = Spimex(**product_data)
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)

    def get_all_products(self):
        return self.db.query(Spimex).all()

    def count(self):
        return self.db.query(Spimex).count()
