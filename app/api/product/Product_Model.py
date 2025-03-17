from app.settings import db
from sqlalchemy.dialects.postgresql import ARRAY

class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_name = db.Column(db.String(255), nullable=False)
    input_image_urls = db.Column(ARRAY(db.String), nullable=False)  # Stores multiple URLs
    output_image_urls = db.Column(ARRAY(db.String), nullable=False)  # Stores multiple URLs

    def __init__(self, product_name, input_image_urls, output_image_urls):
        self.product_name = product_name
        self.input_image_urls = input_image_urls
        self.output_image_urls = output_image_urls

    def __repr__(self):
        return f"<Product {self.product_name}>"
