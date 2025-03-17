from marshmallow import Schema, fields, post_load
import csv
from PIL import Image
import requests
from io import BytesIO
import os
from app.settings import db


class ProductSchema(Schema):
    id = fields.Int(required=True)
    product_name = fields.Str(required=True)
    input_image_urls = fields.List(fields.Str(), required=True)
    output_image_urls = fields.List(fields.Str(), required=False)

    @post_load
    def make_product(self, data, **kwargs):
        return Product(**data)



class Product:
    def __init__(self, id, product_name, input_image_urls, output_image_urls=None):
        self.id = id
        self.product_name = product_name
        self.input_image_urls = input_image_urls
        self.output_image_urls = output_image_urls or []


    def reduce_50_percent(self, image_url):
        """Fetch image from URL, resize to 50% and return the processed image."""
        response = requests.get(image_url)
        if response.status_code == 200:
            img = Image.open(BytesIO(response.content))
            new_size = (img.width // 2, img.height // 2)
            img = img.resize(new_size, Image.ANTIALIAS)
            return img
        else:
            raise Exception(f"Failed to fetch image from {image_url}")



    def save_image(self, image, file_name):
        """Save the processed image and return the saved file path."""
        save_dir = "processed_images"
        os.makedirs(save_dir, exist_ok=True)
        save_path = os.path.join(save_dir, file_name)
        image.save(save_path)
        return save_path


    def read_csv_file(self, file_path):
        """Read CSV file, validate values, resize images, and update the database."""
        processed_products = []
        with open(file_path, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                input_urls = row["input_image_urls"].split(",")  # Convert CSV string to list
                output_urls = []

                for url in input_urls:
                    try:
                        image = self.reduce_50_percent(url)
                        file_name = os.path.basename(url)  # Use original filename
                        saved_path = self.save_image(image, file_name)
                        output_urls.append(saved_path)
                    except Exception as e:
                        print(f"Error processing {url}: {e}")
                        continue

                row["output_image_urls"] = ",".join(output_urls)  # Store as CSV string
                processed_products.append(Product(row["id"], row["product_name"], input_urls, output_urls))

        # Insert into database
        for product in processed_products:
            db.session.add(product)
        db.session.commit()
