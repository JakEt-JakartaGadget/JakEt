from django.shortcuts import render
import csv
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

# Fungsi untuk memuat data device dari file CSV
def load_devices_from_csv():
    devices = []
    try:
        with open('dataset/product/mobiles.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                devices.append({
                    'model': row['Model'],
                    'brand': row['Brand'],
                    'product_name': row['Product Name'],
                    'picture_url': row['Picture URL'],
                    'battery_capacity_mAh': row['Battery capacity (mAh)'],
                    'price_inr': row['Price in India'],
                    'ram': row['RAM'],
                    'camera': row['Rear camera'],
                    'processor': row['Processor'],  
                    'screen_size': row['Screen size (inches)'],  
                    'url': row['url'], 
                })
    except FileNotFoundError as e:
        print(f"Error loading CSV file: {e}")
    return devices

@csrf_exempt
def comparison_view(request):
    if request.method == 'GET':
        devices = load_devices_from_csv()
        return render(request, 'comparison/comparison.html', {'devices': devices})

    if request.method == 'POST':
        model1 = request.POST.get('model1')
        model2 = request.POST.get('model2')
        devices = load_devices_from_csv()

        device1 = next((device for device in devices if device['model'] == model1), None)
        device2 = next((device for device in devices if device['model'] == model2), None)

        if device1 and device2:
            return JsonResponse({'device1': device1, 'device2': device2})
        else:
            return JsonResponse({'error': 'Device not found'}, status=404)

    return HttpResponse(status=405)
