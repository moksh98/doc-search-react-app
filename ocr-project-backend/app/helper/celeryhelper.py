import io
import os
import json
from PIL import Image, ImageDraw, ImageFont
from google.oauth2 import service_account
from google.cloud import vision
from google.protobuf.json_format import MessageToJson
from bidi.algorithm import get_display
import arabic_reshaper
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from app.core.settings import settings


class PdfCreator:
    def __init__(self, image_path, font_path, font_size=32, output_path=None, dpi=300):
        self.image_path = image_path
        self.font_path = font_path
        self.font_size = font_size
        self.output_path = output_path
        self.text_annotations = []
        self.dpi = dpi

    def get_font_size(self, word_vertices, text):
        # Get coordinates of the four vertices
        x1, y1 = word_vertices[0]
        x2, y2 = word_vertices[1]
        x3, y3 = word_vertices[2]
        x4, y4 = word_vertices[3]

        # Define the font style
        font = ImageFont.truetype(self.font_path, size=1)

        # Calculate the appropriate font size
        font_size = 1
        while font.getsize(text)[0] < 0.8 * (x2 - x1):
            font_size += 1
            font = ImageFont.truetype(self.font_path, size=font_size)

        return font_size

    def is_arabic_or_english(self, text: str) -> str:
        arabic_range = range(0x0600, 0x06FF + 1)
        english_range = range(0x0041, 0x007A + 1)
        for char in text:
            char_code = ord(char)
            if char_code in arabic_range:
                return "Arabic"
            elif char_code in english_range:
                return "English"
        return "Unknown"

    def recognize_text(self):
        """Recognizes text from an image using Google Cloud Vision API."""
        credentials = service_account.Credentials.from_service_account_file(
            settings.GCV_CRED)
        client = vision.ImageAnnotatorClient(credentials=credentials)

        with open(self.image_path, 'rb') as image_file:
            content = image_file.read()
        image = vision.Image(content=content)
        response = client.text_detection(image=image)
        serialized = MessageToJson(response._pb)
        string = '{"responses": [\n' + serialized + '\n]}'
        self.text_annotations = json.loads(string)
        return str(response.text_annotations[0].description)

    def create_pdf(self):
        """Creates a PDF file with the recognized text and image."""
        if not self.text_annotations:
            raise ValueError('No text annotations available. Please run recognize_text() first.')
        if not os.path.exists(self.font_path):
            raise FileNotFoundError(f'Font file not found: {self.font_path}')

        unknown_chars = 0

        # Register Arial Font
        pdfmetrics.registerFont(TTFont('Arial', self.font_path))

        # Load font and image
        img = Image.open(self.image_path)

        # Create a PDF document
        self.output_path = self.output_path or os.path.splitext(self.image_path)[0] + '.pdf'
        pdf_canvas = canvas.Canvas(self.output_path)

        # Set PDF page size equal to the image size
        width, height = img.size
        pdf_canvas.setPageSize((width, height))

        # Add the image to the PDF document
        pdf_canvas.drawImage(self.image_path, 0, 0, width, height)

        self.text_annotations["responses"][0]["textAnnotations"].pop()
        # Loop through the text annotations and add the text to the PDF document
        for text in self.text_annotations["responses"][0]["textAnnotations"]:
            # Get the coordinates of the bounding box for the text
            vertices = [(vertex["x"], vertex["y"]) for vertex in text["boundingPoly"]["vertices"]]
            x_min, y_min = vertices[0]
            x_max, y_max = vertices[2]
            string = text["description"]

            # Set the fill color to be transparent
            pdf_canvas.setFillColorRGB(0, 0, 0, 0)

            # Reshape the Arabic text and add it to the PDF document
            if self.is_arabic_or_english(string) == "Arabic":
                arabic_text = arabic_reshaper.reshape(text["description"])
                arabic_text = get_display(arabic_text)
                font_size = self.get_font_size(vertices, arabic_text)
                pdf_canvas.setFont("Arial", font_size)
                if font_size <= 10:
                    # pdf_canvas.rect(x_min, height - y_min - 30, x_max-x_min, y_max-y_min, stroke=1, fill=0)
                    pdf_canvas.drawString(x_min, height - y_min - 20, arabic_text)
                else:
                    pdf_canvas.drawString(x_min, height - y_min - 35, arabic_text)
            elif self.is_arabic_or_english(string) == "English":
                font_size = self.get_font_size(vertices, text["description"])
                pdf_canvas.setFont("Arial", font_size)
                # pdf_canvas.rect(x_min, height - y_min - 25, x_max-x_min, y_max-y_min, stroke=1, fill=0)
                if font_size <= 10:
                    pdf_canvas.drawString(x_min, height - y_min - 20, text["description"])
                else:
                    pdf_canvas.drawString(x_min, height - y_min - 35, text["description"])
            else:
                unknown_chars += 1

        print("{:d} unknown characters found! \n Skipping it".format(unknown_chars))
        # Save the PDF document
        pdf_canvas.save()
