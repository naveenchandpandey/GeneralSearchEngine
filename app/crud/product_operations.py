from ..models.products import Products
from sqlalchemy.orm import Session
from ..exceptions import InvalidInput


class ProductOperations:

    def __init__(self):
        """
        Handler for all the database operations
        """
        pass

    @staticmethod
    def get_product_by_id(db: Session, product_id: int):
        """
        Fetches a particular row from the DB based on ID
        :param db: DB connection object
        :param product_id: Primary key for the products table
        :return: DB row object
        """
        results = db.query(Products).filter(Products.id == product_id).first()
        if results:
            return results
        raise InvalidInput(data=product_id, message='Invalid product ID: ')

    @staticmethod
    def get_all_products(db: Session):
        """
        Fetches all the rows present in the DB
        :param db: DB connection object
        :return: DB rows as objects
        """
        # NOTE: Could be a very heavy in case the no. of rows in the table is large.
        # should implement chunking of records in that case
        return db.query(Products).all()
