from PIL import Image
import io
import requests
import uuid


class ImageProcessor:

    # Check if the image format is supported.
    def is_valid_format(self, image_data):
        supported_formats = [".jpeg", ".jpg", ".png", ".gif"]
        extension = image_data.filename[image_data.filename.rfind("."):]
        return extension in supported_formats

    # Process the image based on the provided arguments.
    def process_image(self, args):
        # Check if the image data is provided as a file
        image_data = args.get("image_file")

        if image_data is None:
            # If image data is not provided as a file, fetch it from the URL
            image_url = args.get("image_url")
            response = requests.get(image_url)

            # Check if the URL request was successful
            if response.status_code != 200:
                return {"error": "Invalid URL or unable to download image"}
            
            # Check if the image format from the URL is supported
            if not self.is_valid_format(response.headers["Content-Type"]):
                return {"error": "Unsupported image format from URL"}
            
            # Use the content of the response as the image data
            image_data = response.content

        # Generate a unique ID for the processed image
        image_id = str(uuid.uuid1().hex)

        modifier = args.get("modifier")
        # Check if a specific modifier is requested (e.g., "grayScale")
        if modifier == "grayScale":
            # Convert the image to grayscale
            return {"id": image_id, "new_file": self.convert_to_gray_scale(image_data)}

    # Convert the image data to grayscale.
    def convert_to_gray_scale(self, image_data):
        # Open the image data and convert it to grayscale
        img = Image.open(io.BytesIO(image_data)).convert("LA")
        
        # Save the grayscale image data to a new BytesIO object
        new_image_data = io.BytesIO()
        img.save(new_image_data, "PNG")
        new_image_data.seek(0)
        return new_image_data
