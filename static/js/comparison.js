// Fungsi untuk menambahkan gambar ke dalam dropdown options
window.onload = function() {
    // Ambil semua dropdown dengan kelas 'device-dropdown'
    const dropdowns = document.querySelectorAll('.device-dropdown');

    // Iterasi melalui setiap dropdown
    dropdowns.forEach(dropdown => {
        const options = dropdown.querySelectorAll('option');

        // Iterasi melalui setiap option di dalam dropdown
        options.forEach(option => {
            const imageUrl = option.getAttribute('data-image');
            
            // Jika option memiliki atribut 'data-image', tambahkan gambar
            if (imageUrl) {
                // Buat elemen gambar baru
                const image = document.createElement('img');
                image.src = imageUrl;
                image.style.width = '40px'; // Ukuran gambar
                image.style.height = '40px';
                image.style.marginRight = '10px';

                // Kosongkan teks asli dalam option
                option.textContent = ''; 
                
                // Tambahkan gambar di awal option
                option.appendChild(image);
                
                // Tambahkan teks setelah gambar (berdasarkan Product Name)
                const textNode = document.createTextNode(option.getAttribute('value'));
                option.appendChild(textNode); 
            }
        });
    });
};

// Fungsi untuk menangani event submit pada tombol Compare menggunakan AJAX
document.getElementById('comparisonForm').addEventListener('submit', function(event) {
    event.preventDefault();  // Mencegah halaman di-reload

    let model1 = document.getElementById('device1').value;
    let model2 = document.getElementById('device2').value;
    let url = document.getElementById('comparisonForm').getAttribute('data-url');
    
    // Buat objek FormData untuk mengirim data ke server
    const formData = new FormData();
    formData.append('model1', model1);
    formData.append('model2', model2);

    // AJAX Request menggunakan Fetch API
    fetch(url, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),  // Ambil CSRF token untuk keamanan
        },
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();  // Ambil respons dalam format JSON
    })
    .then(data => {
        if (data.device1 && data.device2) {
            // Update HTML untuk menampilkan hasil perbandingan
            document.getElementById('comparisonResults').innerHTML = `
                <div class="device-card">
                    <h2>${data.device1.product_name}</h2>
                    <img src="${data.device1.picture_url}" alt="${data.device1.model}">
                    <h3>Specification</h3>
                    <p>Brand: ${data.device1.brand}</p>
                    <p>Battery: ${data.device1.battery_capacity_mAh} mAh</p>
                    <p>Harga Rilis (IDR): ${data.device1.price_idr}</p> <!-- Tambahkan harga dalam IDR -->
                    <p>Camera: ${data.device1.camera}</p>
                    <p>Processor: ${data.device1.processor}</p>
                    <p>Display: ${data.device1.screen_size}"</p>
                    <button class="view-button">
                        <a href="${data.device1.url}" target="_blank">View product page</a>
                    </button>
                    <a href="" class="wishlist-button">
                        <img src="${heartIconPath}" alt="Wishlist">
                    </a>
                </div>
                <div class="device-card">
                    <h2>${data.device2.product_name}</h2>
                    <img src="${data.device2.picture_url}" alt="${data.device2.model}">
                    <h3>Specification</h3>
                    <p>Brand: ${data.device2.brand}</p>
                    <p>Battery: ${data.device2.battery_capacity_mAh} mAh</p>
                    <p>Harga Rilis (IDR): ${data.device2.price_idr}</p> <!-- Tambahkan harga dalam IDR -->
                    <p>Camera: ${data.device2.camera}</p>
                    <p>Processor: ${data.device2.processor}</p>
                    <p>Display: ${data.device2.screen_size}"</p>
                    <button class="view-button">
                        <a href="${data.device2.url}" target="_blank">View product page</a>
                    </button>
                    <a href="" class="wishlist-button">
                        <img src="${heartIconPath}" alt="Wishlist">
                    </a>
                </div>
            `;
        } else {
            alert('Data for one or both devices not found');
        }
    })
    .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
    });
});

// Fungsi untuk mendapatkan nilai CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        let cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
