import os
import base64
from flask import request, jsonify
from marshmallow import fields, ValidationError
from app.settings import ma
from . import api_upload_csv
from .Product import  Product   # Assuming Product is in product_model.py
import tempfile

class RequestBodySchema(ma.Schema):
    file_data = fields.Str(required=True, error_messages={"required": "Base64-encoded CSV data is required."})

request_body_schema = RequestBodySchema()

@api_upload_csv.route("/api/upload", methods=["POST"])
def upload_csv():
    try:
        # Validate input data using RequestBodySchema (includes ProductSchema validation)
        data = request_body_schema.load(request.get_json())

        # Decode Base64 file data
        file_data = base64.b64decode(data["file_data"])
        file_name = data["file_name"]

        # Save decoded file temporarily
        temp_dir = tempfile.gettempdir()
        file_path = os.path.join(temp_dir, file_name)

        with open(file_path, "wb") as f:
            f.write(file_data)

        # Process CSV file
        product = Product()
        product.read_csv_file(file_path)

        return jsonify({"message": "CSV processed successfully"}), 200

    except ValidationError as err:
        return jsonify({"error": err.messages}), 400  # Return validation errors

    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Return any other errors
