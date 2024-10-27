from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import mock_open, patch
import json
import csv
from Comparison.views import load_devices_from_csv, convert_inr_to_idr

# Definisikan mock_csv_data sebagai variabel global
mock_csv_data = """Model,Brand,Product Name,Picture URL,Price in India,Battery capacity (mAh),RAM,Rear camera,Processor,Screen size (inches),url
V11 Pro,Vivo,"Vivo V11 Pro (6GB RAM, 64GB) - Supernova Red",https://i.gadgets360cdn.com/products/large/1536222480_635_vivo_v11_pro.jpg,"₹ 28,990",3400,6GB,"12-megapixel (f/1.8) + 5-megapixel (f/2.4)","Qualcomm Snapdragon 660",6.41,https://gadgets.ndtv.com/vivo-v11-pro-5632
Redmi Note 5 Pro,Xiaomi,"Redmi Note 5 Pro (4GB RAM, 64GB) - Red",https://i.gadgets360cdn.com/products/large/1518591378_635_xiaomi_redmi_note_5_pro.jpg,"₹ 11,290",4000,4GB,"12-megapixel (f/2.2) + 5-megapixel (f/2.0)","Qualcomm Snapdragon 636",5.99,https://gadgets.ndtv.com/redmi-note-5-pro-4607
"""

class ComparisonTests(TestCase):

    def setUp(self):
        self.client = Client()
        # Tidak perlu mendefinisikan self.mock_csv_data di sini karena sudah ada di variabel global

    @patch('builtins.open', new_callable=mock_open, read_data=mock_csv_data)
    def test_load_devices_from_csv(self, mock_file):
        devices = load_devices_from_csv()
        # print("Devices loaded:", devices)  # Debugging untuk melihat perangkat yang dimuat
        self.assertTrue(isinstance(devices, list))
        self.assertEqual(len(devices), 2)  # Pastikan jumlah perangkat yang dimuat sesuai dengan mock data
        self.assertEqual(devices[0]['model'], 'V11 Pro')
        self.assertEqual(devices[1]['brand'], 'Xiaomi')

    def test_convert_inr_to_idr(self):
        # Test INR to IDR conversion dengan pembulatan
        self.assertEqual(convert_inr_to_idr('₹ 28,990'), 'Rp 5,379,384')  # Hasil pembulatan
        self.assertEqual(convert_inr_to_idr('₹ 11,290'), 'Rp 2,094,972')  # Sesuaikan hasil
        self.assertEqual(convert_inr_to_idr(None), 'Price not available')  # Test jika nilai None
        self.assertEqual(convert_inr_to_idr('₹ not a number'), 'Price not available')

    @patch('builtins.open', new_callable=mock_open, read_data=mock_csv_data)
    def test_comparison_view_get(self, mock_file):
        response = self.client.get(reverse('Comparison:comparison'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'comparison/comparison.html')
        self.assertIn('devices', response.context)

    @patch('builtins.open', new_callable=mock_open, read_data=mock_csv_data)
    def test_comparison_view_post_success(self, mock_file):
        response = self.client.post(reverse('Comparison:comparison'), {
            'model1': 'V11 Pro',
            'model2': 'Redmi Note 5 Pro'
        })
        #print("POST response status:", response.status_code)  # Debugging untuk status code
        #print("POST response content:", response.content)     # Debugging untuk melihat konten respons

        self.assertEqual(response.status_code, 200)  # Pastikan status respons adalah 200 OK
        data = json.loads(response.content)
        self.assertIn('device1', data)
        self.assertIn('device2', data)
        self.assertEqual(data['device1']['model'], 'V11 Pro')
        self.assertEqual(data['device2']['model'], 'Redmi Note 5 Pro')

    @patch('builtins.open', new_callable=mock_open, read_data=mock_csv_data)
    def test_comparison_view_post_device_not_found(self, mock_file):
        response = self.client.post(reverse('Comparison:comparison'), {
            'model1': 'InvalidModel',
            'model2': 'Redmi Note 5 Pro'
        })
        #print("POST response status (Invalid):", response.status_code)  # Debugging untuk status code

        self.assertEqual(response.status_code, 404)  # Pastikan status respons adalah 404
        data = json.loads(response.content)
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Device not found')
