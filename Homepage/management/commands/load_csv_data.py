import csv
from django.core.management.base import BaseCommand
from Homepage.models import Phone
from django.core.exceptions import ValidationError
from decimal import Decimal, InvalidOperation

class Command(BaseCommand):
    help = 'Load smartphone data from CSV files into the database'

    def handle(self, *args, **kwargs):
        file_path = 'dataset/product/mobile_phone_price.csv' 
        self.load_csv_to_database(file_path, Phone)

    def clean_price(self, price_str):
        """
        Membersihkan dan mengonversi harga dari USD ke INR.
        """
        if not price_str or price_str.strip() == "":
            print(f"Price is empty or None.")
            return None
        try:
            price_cleaned = price_str.strip().replace(',', '').replace('$', '')
            print(f"Original price: '{price_str}' -> Cleaned price: '{price_cleaned}'")
            price_usd = Decimal(price_cleaned)

            price_inr = price_usd * Decimal('15600')
            print(f"Converted INR price: {price_inr}")
            return price_inr
        except (InvalidOperation, ValueError) as e:
            print(f"Invalid price format: '{price_str}' ({e})")
            return None

    def clean_integer_field(self, value, field_name):
        """
        Membersihkan dan mengonversi field yang harus berupa integer.
        """
        if not value or value.strip() == "":
            print(f"{field_name} is empty or None.")
            return None
        try:
            value_cleaned = value.strip().replace(',', '')
            integer_value = int(value_cleaned)
            print(f"Converted {field_name}: {integer_value}")
            return integer_value
        except ValueError as e:
            print(f"Invalid {field_name} format: '{value}' ({e})")
            return None

    def load_csv_to_database(self, file_path, model_class):
        """
        Memuat data dari CSV ke database, menangani BOM, dan menyimpan secara benar.
        """
        with open(file_path, newline='', encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)
            print(f"CSV Headers: {reader.fieldnames}")
            for row_number, row in enumerate(reader, start=1):
                print(f"\nProcessing row {row_number}: {row}")
                
                price_str = row.get('Price ($)', '').strip()
                price_inr = self.clean_price(price_str)
                if price_inr is None:
                    print(f"Skipping row {row_number} due to invalid price: '{price_str}'")
                    continue


                battery_str = row.get('Battery Capacity (mAh)', '').strip()
                battery_capacity = self.clean_integer_field(battery_str, 'battery_capacity_mAh')
                if battery_capacity is None:
                    print(f"Skipping row {row_number} due to invalid battery capacity.")
                    continue

                screen_size_str = row.get('Screen Size (inches)', '').strip()
                try:
                    screen_size = float(screen_size_str) if screen_size_str else 0.0
                except ValueError:
                    print(f"Invalid screen size: '{screen_size_str}', setting to 0.0")
                    screen_size = 0.0

                brand = row.get('Brand', '').strip()  # Ensure brand is properly read
                model = row.get('Model', '').strip()
                storage = row.get('Storage ', '').strip()  
                ram = row.get('RAM ', '').strip()         
                camera_mp = row.get('Camera (MP)', '').strip()

                model_data = {
                    'brand': brand,
                    'model': model,
                    'storage': storage,
                    'ram': ram,
                    'screen_size_inches': screen_size,
                    'camera_mp': camera_mp,
                    'battery_capacity_mAh': battery_capacity,
                    'price_usd': Decimal(price_str.replace('$', '').replace(',', '')),  # Simpan USD jika diperlukan
                    'price_inr': price_inr,
                }

                print(f"Model data prepared for saving: {model_data}")
                model_instance = model_class(**model_data)
                try:
                    model_instance.save()
                    print(f"Saved: {model}")
                except ValidationError as e:
                    print(f"ValidationError saving {model}: {e}")
                except Exception as e:
                    print(f"Unexpected error saving {model}: {e}")

