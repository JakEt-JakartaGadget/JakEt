import csv
from django.core.management.base import BaseCommand
from Homepage.models import Phone
from Article.models import Artikel
from django.core.exceptions import ValidationError
from decimal import Decimal, InvalidOperation
from datetime import datetime
import logging


logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Load smartphone and article data from CSV files into the database'

    def handle(self, *args, **kwargs):
        product_file_path = 'dataset/product/cleaned_dataset.csv'
        logger.info(f"Loading data from {product_file_path} into Phone model.")
        self.load_csv_to_database(product_file_path, Phone, self.process_phone_row)

        articles_file_path = 'dataset/article/articles.csv'
        logger.info(f"Loading data from {articles_file_path} into Article model.")
        self.load_csv_to_database(articles_file_path, Artikel, self.process_article_row)

    def clean_price(self, price_str):
        """
        Cleans and converts price from USD to INR.
        """
        if not price_str or price_str.strip() == "":
            logger.warning("Price is empty or None.")
            return None
        try:
            price_cleaned = price_str.strip().replace(',', '').replace('$', '')
            logger.debug(f"Original price: '{price_str}' -> Cleaned price: '{price_cleaned}'")
            price_usd = Decimal(price_cleaned)

            price_inr = price_usd * Decimal('15600')
            logger.debug(f"Converted INR price: {price_inr}")
            return price_inr
        except (InvalidOperation, ValueError) as e:
            logger.error(f"Invalid price format: '{price_str}' ({e})")
            return None

    def clean_integer_field(self, value, field_name):
        """
        Cleans and converts fields that should be integers.
        """
        if not value or value.strip() == "":
            logger.warning(f"{field_name} is empty or None.")
            return None
        try:
            value_cleaned = value.strip().replace(',', '')
            integer_value = int(value_cleaned)
            logger.debug(f"Converted {field_name}: {integer_value}")
            return integer_value
        except ValueError as e:
            logger.error(f"Invalid {field_name} format: '{value}' ({e})")
            return None

    def load_csv_to_database(self, file_path, model_class, process_row_func):
        """
        Loads data from CSV into the specified model, handling BOM and saving correctly.
        """
        try:
            with open(file_path, newline='', encoding='utf-8-sig') as csvfile:
                reader = csv.DictReader(csvfile)
                logger.info(f"CSV Headers: {reader.fieldnames}")
                for row_number, row in enumerate(reader, start=1):
                    logger.info(f"\nProcessing row {row_number}: {row}")
                    processed_data = process_row_func(row, row_number)
                    if processed_data:
                        model_instance = model_class(**processed_data)
                        try:
                            model_instance.save()
                            logger.info(f"Saved: {model_instance}")
                        except ValidationError as e:
                            logger.error(f"ValidationError saving {model_instance}: {e}")
                        except Exception as e:
                            logger.error(f"Unexpected error saving {model_instance}: {e}")
        except FileNotFoundError:
            logger.error(f"File not found: {file_path}")
        except Exception as e:
            logger.error(f"Error processing file {file_path}: {e}")

    def process_phone_row(self, row, row_number):
        """
        Processes a row from the Phone CSV and returns a dictionary of cleaned data.
        Returns None if the row should be skipped.
        """
        price_str = row.get('Price ($)', '').strip()
        price_inr = self.clean_price(price_str)
        if price_inr is None:
            logger.warning(f"Skipping row {row_number} due to invalid price: '{price_str}'")
            return None

        battery_str = row.get('Battery Capacity (mAh)', '').strip()
        battery_capacity = self.clean_integer_field(battery_str, 'battery_capacity_mAh')
        if battery_capacity is None:
            logger.warning(f"Skipping row {row_number} due to invalid battery capacity.")
            return None

        screen_size_str = row.get('Screen Size (inches)', '').strip()
        try:
            screen_size = float(screen_size_str) if screen_size_str else 0.0
        except ValueError:
            logger.error(f"Invalid screen size: '{screen_size_str}', setting to 0.0")
            screen_size = 0.0

        one_star = self.clean_integer_field(row.get('1 Star', '').strip(), '1 Star')
        two_star = self.clean_integer_field(row.get('2 Star', '').strip(), '2 Star')
        three_star = self.clean_integer_field(row.get('3 Star', '').strip(), '3 Star')
        four_star = self.clean_integer_field(row.get('4 Star', '').strip(), '4 Star')
        five_star = self.clean_integer_field(row.get('5 Star', '').strip(), '5 Star')

        brand = row.get('Brand', '').strip()
        model = row.get('Model', '').strip()
        storage = row.get('Storage ', '').strip()
        ram = row.get('RAM ', '').strip()
        camera_mp = row.get('Camera (MP)', '').strip()
        image_url = row.get('ImageURL', '').strip()

        model_data = {
            'brand': brand,
            'model': model,
            'storage': storage,
            'ram': ram,
            'screen_size_inches': screen_size,
            'camera_mp': camera_mp,
            'battery_capacity_mAh': battery_capacity,
            'price_usd': Decimal(price_str.replace('$', '').replace(',', '')),
            'price_inr': price_inr,
            'image_url': image_url,
            'one_star': one_star or 0,
            'two_star': two_star or 0,
            'three_star': three_star or 0,
            'four_star': four_star or 0,
            'five_star': five_star or 0,
        }

        logger.debug(f"Phone model data prepared for saving: {model_data}")
        return model_data

    def process_article_row(self, row, row_number):
        """
        Processes a row from the Article CSV and returns a dictionary of cleaned data.
        Returns None if the row should be skipped.
        """
        title = row.get('title', '').strip()
        content = row.get('content', '').strip()
        image_url = row.get('image_url', '').strip()
        source = row.get('source', '').strip()

        if not title or not content or not source:
            logger.warning(f"Skipping row {row_number} due to missing mandatory fields.")
            return None

        if Artikel.objects.filter(title=title).exists():
            logger.warning(f"Skipping row {row_number} as Article with title '{title}' already exists.")
            return None

        model_data = {
            'title': title,
            'content': content,
            'image_url': image_url or None,  
            'source': source,
        }

        logger.debug(f"Article model data prepared for saving: {model_data}")
        return model_data
