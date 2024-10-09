# roso-jogja

## Nama Anggota Kelompok PBP-D11:
1. Akhdan Taufiq Syofyan (2306152475)
2. Fadhli Raihan Ardiansyah (2306207594)
3. Makarim Zufar Prambudyo (2306241751)
4. Nadia Rahmadina Aristawati (2306207972)
5. Yudayana Arif Prasojo (2306215160)

## Deskripsi Aplikasi
Baru tiba di Jogja dan perut mulai keroncongan, tapi Anda bingung harus mulai dari mana untuk menemukan kuliner terbaik di kota ini. Dengan banyaknya pilihan makanan dari yang tradisional hingga kekinian, memilih tempat yang tepat bisa jadi memusingkan, apalagi jika waktu terbatas. RosoJogja hadir untuk memudahkan Anda menemukan kuliner yang sesuai dengan kebutuhan dan keinginan Anda di Jogja. Fokus aplikasi ini adalah memberikan rekomendasi makanan terdekat dengan cepat dan praktis.

Fitur yang disediakan:
- **Pencarian Berbasis Lokasi**
Aplikasi secara otomatis memberikan rekomendasi kuliner terdekat dari lokasi Anda, membantu Anda menemukan makanan dengan cepat dan mudah.
- **Kategori Makanan**
Pengguna dapat memilih kategori makanan yang diinginkan, seperti makanan tradisional, makanan kekinian, jajanan pasar, atau minuman khas Jogja, sehingga pencarian menjadi lebih terarah.
- **Informasi Jam Buka**
Setiap tempat yang direkomendasikan menampilkan informasi jam buka secara real-time, memastikan Anda hanya melihat tempat yang siap melayani.
- **Ulasan Singkat dan Rating**
Setiap rekomendasi dilengkapi dengan ulasan singkat dan rating dari pengguna lain, sehingga Anda bisa membuat keputusan yang lebih informasional sebelum mencoba.
- **Filter Harga**
Sesuaikan pilihan Anda dengan anggaran yang dimiliki melalui fitur filter harga, agar kuliner yang direkomendasikan sesuai dengan dompet Anda.
Dengan fokus pada fitur yang sederhana namun esensial, RosoJogja dirancang untuk memudahkan siapa pun yang baru datang ke Jogja agar bisa menemukan makanan dengan cepat, tepat, dan tanpa kebingungan.

## Daftar Modul yang Diimplementasikan
1. Restoran dan Makanan

Yang mengerjakan: Yuda

Pembeli|Penjual|Admin Aplikasi
-|-|-
Pembeli dapat melihat berbagai restoran yang ada dan memesan makanan yang terdapat pada restoran tersebut (Memasukkan ke dalam cart dan membuat order) | Penjual dapat memodifikasi atau menambahkan informasi makanan yang terdapat pada restoran yang ia miliki | Memiliki wewenang administratif terhadap restoran yang ada di aplikasi (membuat, memodifikasi, dan menghapus restoran yang ada)

2. Cart dan Order

Yang mengerjakan: Akhdan

Pembeli|Penjual|Admin Aplikasi
-|-|-
Pembeli dapat memasukkan makanan yang terdapat pada suatu restoran ke dalam cart dan melakukan checkout (membuat order)|Penjual tidak memiliki fitur ini|Admin tidak memiliki fitur ini

3. Promo

Yang mengerjakan: Nadia

Pembeli|Penjual|Admin Aplikasi
-|-|-
Menggunakan voucher yang telah ditambahkan oleh admin dengan memasukkan sebuah kode untuk meng-claim voucher tersebut|Penjual tidak memiliki fitur ini|Menambahkan voucher dengan harga tertentu dan minimal transaksi tertentu yang kemudian dapat digunakan oleh pembeli

4. Wishlist

Yang mengerjakan: Zufar

Pembeli|Penjual|Admin Aplikasi
-|-|-
Menambahkan makanan yang ingin dibeli kepada wishlist (list makanan yang ingin dicoba)|Penjual tidak memiliki fitur ini|Admin tidak memiliki fitur ini

5. Review

Yang mengerjakan: Fadhli

Pembeli|Penjual|Admin Aplikasi
-|-|-
Menambahkan review kepada restoran yang sebelumnya sudah pernah dipesan|Penjual tidak memiliki fitur ini|Admin dapat menghapus suatu review dari sebuah restoran

## Sumber dataset kuliner Jogja

[Kaggle](https://www.kaggle.com/datasets/yudhaislamisulistya/places-to-eat-in-the-jogja-region)

## Role atau Peran
1. Pembeli

Peran utama di aplikasi, pembeli dapat membeli makanan dari sebuah restoran, menambahkan makanan kepada wishlist, dan menulis review terhadap suatu restoran.

2. Penjual

Penjual dapat memodifikasi makanan yang terdapat di restoran yang dimilikinya.

3. Admin Aplikasi

Admin dapat menambahkan, memodifikasi, dan menghapus restoran yang terdapat dalam aplikasi, menambahkan promo untuk digunakan oleh pembeli, dan menghapus review yang ditujukan kepada suatu restoran.

