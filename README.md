# Proyek Tengah Semester C02 - PBP Gasal 2024/2025
- [Nama Aplikasi](#nama-aplikasi-jaket)
- [Profil Kelompok](#-kelompok-c02---jaket-)
- [Cerita dan Manfaat Aplikasi](#cerita-dan-manfaat-aplikasi)
- [Modul Aplikasi](#️-modul-aplikasi-️)
- [Sumber Initial Dataset](#sumber-initial-dataset)
- [Persona](#-persona-)
- [Deployment](#-tautan-deployment-aplikasi-)

# Nama Aplikasi: JakEt

### 👋 Kelompok C02 - JakEt 👋
| Nama | NPM |
| :--------------: | :--------: |
| Anthony Edbert Feriyanto | 2306165654 |
| Abraham Jordy Ollen | 2306275102 |
| Eva Yunia Aliyanshah | 2306165515 |
| Ida Made Revindra Dikta Mahendra | 2306275954 |
| Bertrand Gwynfory Iskandar | 2306152121 |

## Cerita dan Manfaat Aplikasi
Kota Jakarta Selatan telah lama menjadi ikon kehidupan metropolitan di Indonesia. Kehidupan yang dinamis dan modern ini tentu tidak bisa lepas dari penggunaan gadget, terutama handphone, yang telah menjadi kebutuhan primer bagi setiap individu, khususnya warga Jakarta Selatan. Dalam rangka mempermudah kehidupan digital mereka, kami memperkenalkan **JakEt** (Jakarta Gadget), sebuah platform yang dirancang khusus untuk memenuhi kebutuhan warga Jakarta Selatan akan gadget yang terpercaya dan berkualitas.

**JakEt** akan menjadi pusat jual beli gadget yang dapat diandalkan, dengan harga terjangkau dan menyediakan berbagai jenis produk, baik baru (brand new) maupun bekas (used). Selain itu, JakEt juga berfungsi sebagai platform perencanaan yang membantu pengguna memilih gadget yang sesuai dengan anggaran mereka, sekaligus memberikan spesifikasi terbaik yang dapat mereka peroleh dalam kisaran harga tersebut. 

Tak hanya berfokus pada transaksi jual beli, JakEt juga memberikan informasi mengenai toko-toko offline terpercaya bagi pelanggan yang lebih nyaman berbelanja langsung. Ini menjadi solusi bagi mereka yang ragu melakukan pembelian secara online.

Lebih dari itu, JakEt berperan sebagai penghubung antara pengguna dan penyedia layanan servis gadget. Dengan fitur ini, pengguna tidak perlu bingung lagi dalam mencari tempat servis yang profesional dan terpercaya untuk memperbaiki atau merawat gadget mereka.

Dengan **JakEt**, kami berharap dapat memberikan pengalaman digital yang lebih mudah, terjangkau, dan aman bagi warga Jakarta Selatan, serta mendukung gaya hidup modern yang semakin mengandalkan teknologi. 



## 🖥️ Modul Aplikasi 🖥️
1. Autentikasi pengguna (apakah pengguna yang login merupakan admin atau user)
    - Dikerjakan oleh: Anthony Edbert Feriyanto
1. Homepage (Aplikasi Django ini berfungsi untuk menampilkan halaman utama antarmuka dataset product dalam web ini. pada antarmuka tersebut juga disediakan fitur sorting, filter, dan search. Fitur filter berupa pemfilteran berdasarkan kategori product.)
    - Dikerjakan oleh: Anthony Edbert Feriyanto
1. Dashboard App
    - Dikerjakan oleh: Anthony Edbert Feriyanto & Ida Made Revindra Dikta Mahendra
1. User Discussion Forum (User yang login dapat memulai dan mengikuti diskusi mengenai produk atau topik)
    - Dikerjakan oleh: Ida Made Revindra Dikta Mahendra
1. Detail Product App (Memuat informasi detail mengenai suatu product dan memberikan link untuk melakukan pembelanjaan)
    - Dikerjakan oleh: Anthony Edbert Feriyanto
1. Service Center App (Aplikasi Django ini berisi informasi mengenai service center yang tersedia)
    - Dikerjakan oleh: Bertrand Gwynfory Iskandar
1. Tiket App (Aplikasi yang digunakan untuk generate sebuah tiket melalui _appointment_ untuk service center)
    - Dikerjakan oleh: Bertrand Gwynfory Iskandar
1. Article About Gadget (Memuat artikel yang membahas informasi update terbaru seputar gadget)
	- Dikerjakan oleh : Eva Yunia Aliyanshah
1. User Profile (Memuat halaman yang menampilkan informasi detail mengenai user seperti, nama, email, no telepon, dan lainnya)
	- Dikerjakan oleh : Eva Yunia Aliyanshah
1. Wishlist & Favorites (Memuat fitur yang memungkinkan pengguna dapat menambahkan gadget ke daftar wishlist atau favorit mereka untuk melacak gadget yang menarik dan bisa dibandingkan dengan produk yang punya kategori sama)
    - Dikerjakan oleh : Anthony Edbert Feriyanto
1. Comparison Tool (Memuat fitur yang memungkinkan pengguna untuk membandingkan spesifikasi dan harga beberapa gadget dari dataset yang sudah diambil (tergantung kategorinya, misal : laptop, mobiles, headphones, dan dataset lainnya) secara berdampingan. Ini sangat membantu pengguna dalam membuat keputusan berdasarkan perbandingan yang objektif.)
    - Dikerjakan oleh : Abraham Jordy Ollen
1. Customer Service Chat (Chat antara User yang login dengan admin)
    - Dikerjakan oleh : Ida Made Revindra Dikta Mahendra

## 📈 Sumber Initial Dataset 📈
[https://www.kaggle.com/code/kerneler/starter-gadgets360-electronics-dataset-095343b9-a/input?select=mobiles.csv](https://www.kaggle.com/code/kerneler/starter-gadgets360-electronics-dataset-095343b9-a/input?select=mobiles.csv)
[https://www.google.co.id/maps/search/service+center+jakarta+selatan/@-6.2833046,106.7772294,13z/data=!3m1!4b1?entry=ttu&g_ep=EgoyMDI0MTAwMi4xIKXMDSoASAFQAw%3D%3D](https://www.google.co.id/maps/search/service+center+jakarta+selatan/@-6.2833046,106.7772294,13z/data=!3m1!4b1?entry=ttu&g_ep=EgoyMDI0MTAwMi4xIKXMDSoASAFQAw%3D%3D)

## 🧑🏻 Persona 🧑🏻

**1. User yang tidak login**
- Meninjau halaman web dan produk-produk di dalamnya.
- Memanfaatkan fitur search and filter untuk menemukan produk yang diinginkan.
- Meninjau artikel terbaru mengenai gadget yang tersedia di platform.

**2. User yang sudah login**
- Menambahkan produk ke dalam wishlist.
- Meninjau detail produk dan informasi lengkapnya, termasuk spesifikasi dan ulasan pengguna lain.
- Memanfaatkan fitur Comparison Tool untuk membandingkan spesifikasi dan harga beberapa produk secara berdampingan.
- Membuat appointment dengan service center melalui Tiket App untuk perbaikan atau konsultasi.
- Meninjau, memulai, dan berkontribusi dalam forum diskusi mengenai produk atau topik terkait, berbagi pengalaman dan mendapatkan saran dari pengguna lain.
- Berkomunikasi dengan Customer Service melalui fitur chat untuk mendapatkan bantuan atau informasi lebih lanjut.
- Mengakses dan mengelola profil pengguna.

**3. Admin**
- Mengakses Dashboard untuk insert, edit, dan delete produk dalam database
- Menanggapi chat user dalam bagian Customer Service
- Menambahkan artikel terbaru mengenai gadget dalam aplikasi
- Memantau appointment yang dibuat oleh user
- Mengelola informasi service center yang tersedia
- Mengelola dan memperbarui dataset produk yang digunakan dalam aplikasi

## 🌐 Tautan Deployment Aplikasi 🌐
Tautan aplikasi PWS: [http://anthony-edbert-jaket.pbp.cs.ui.ac.id](http://anthony-edbert-jaket.pbp.cs.ui.ac.id)


