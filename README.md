# roso-jogja

## Nama Anggota Kelompok PBP-D11:
1. Akhdan Taufiq Syofyan (2306152475)
2. Fadhli Raihan Ardiansyah (2306207594)
3. Makarim Zufar Prambudyo (2306241751)
4. Nadia Rahmadina Aristawati (2306207972)
5. Yudayana Arif Prasojo (2306215160)

## Deskripsi Aplikasi
RosoJogja adalah aplikasi kuliner yang dirancang khusus untuk membantu Anda menemukan dan memesan makanan atau minuman dari berbagai restoran dan tempat makan di Yogyakarta. Dengan antarmuka yang intuitif, RosoJogja memberikan kemudahan dalam mencari restoran, melihat menu, hingga memesan makanan atau minuman.

Aplikasi ini menghadirkan beragam pilihan kuliner, mulai dari makanan tradisional (termasuk angkringan), makanan kekinian dan kuliner modern, oleh-oleh khas Yogyakarta, jajanan pasar/kudapan tradisional, minuman khas Yogyakarta, dan minuman modern. RosoJogja hadir untuk memudahkan Anda menemukan kuliner yang sesuai dengan kebutuhan dan keinginan Anda di Jogja. Fokus aplikasi ini adalah memberikan rekomendasi kuliner terdekat dengan cepat dan praktis.

## Fitur yang disediakan:
- **Kategori Kuliner** <br>
Pengguna dapat memilih kategori kuliner yang diinginkan, seperti makanan tradisional, makanan kekinian, jajanan pasar, atau minuman khas Jogja, sehingga pencarian menjadi lebih terarah.
- **Informasi Jam Buka** <br>
Setiap tempat yang direkomendasikan menampilkan informasi jam buka secara real-time, memastikan Anda hanya melihat tempat yang siap melayani.
- **Ulasan Singkat dan Rating** <br>
Setiap rekomendasi dilengkapi dengan ulasan singkat dan rating dari pengguna lain, sehingga Anda bisa membuat keputusan yang lebih informasional sebelum mencoba.
- **Whislist** <br>
Pengguna dapat menambahkan restoran yang ingin dikunjungi/dilihat ke dalam wishlist mereka.
- **Order Makanan** <br>
Pengguna dapat dengan mudah memesan makanan atau minuman langsung dari aplikasi. Pilih makanan favorit Anda, tentukan jumlah yang diinginkan.
- **Klaim Promo** <br>
 Pengguna dapat mengklaim promo dengan memasukkan kode voucher yang tersedia.

Dengan fokus pada fitur yang sederhana namun esensial, RosoJogja dirancang untuk memudahkan siapa pun yang baru datang ke Jogja agar bisa menemukan makanan dengan cepat, tepat, dan tanpa kebingungan.

## Daftar Modul yang Diimplementasikan

Berikut ini adalah daftar modul dan fitur yang diimplementasikan dalam aplikasi restoran, beserta tanggung jawab masing-masing anggota tim.

### 1. Restoran dan Makanan
**Yang mengerjakan**: Yudayana Arif Prasojo

| Peran       | Fitur                                                                                           |
|-------------|-------------------------------------------------------------------------------------------------|
| **Pembeli** | Melihat daftar restoran dan memesan makanan dari restoran (memasukkan ke dalam cart dan membuat order). |
| **Penjual** | Memodifikasi atau menambahkan informasi makanan di restoran yang dimiliki.                       |
| **Admin**   | Memiliki wewenang administratif terhadap restoran yang ada di aplikasi (membuat, memodifikasi, dan menghapus restoran).                    |

### 2. Cart dan Order
**Yang mengerjakan**: Akhdan Taufiq Syofyan

| Peran       | Fitur                                                                                           |
|-------------|-------------------------------------------------------------------------------------------------|
| **Pembeli** | Memasukkan makanan ke dalam cart dan melakukan checkout untuk membuat order.                    |
| **Penjual** | Tidak memiliki akses ke fitur ini.                                                              |
| **Admin**   | Tidak memiliki akses ke fitur ini.                                                              |

### 3. Promo
**Yang mengerjakan**: Nadia Rahmadina Aristawati

| Peran       | Fitur                                                                                           |
|-------------|-------------------------------------------------------------------------------------------------|
| **Pembeli** | Menggunakan voucher yang telah ditambahkan oleh admin dengan memasukkan sebuah kode untuk meng-claim voucher tersebut. |
| **Penjual** | Tidak memiliki fitur ini.                                                                      |
| **Admin**   | Menambahkan voucher dengan harga tertentu dan minimal transaksi tertentu yang kemudian dapat digunakan oleh pembeli. |

### 4. Wishlist
**Yang mengerjakan**: Makarim Zufar Prambudyo

| Peran       | Fitur                                                                                           |
|-------------|-------------------------------------------------------------------------------------------------|
| **Pembeli** | Menambahkan makanan yang ingin dibeli kepada wishlist (list makanan yang ingin dicoba).        |
| **Penjual** | Tidak memiliki fitur ini.                                                                      |
| **Admin**   | Tidak memiliki fitur ini.                                                                      |

### 5. Review
**Yang mengerjakan**: Fadhli Raihan Ardiansyah

| Peran       | Fitur                                                                                           |
|-------------|-------------------------------------------------------------------------------------------------|
| **Pembeli** | Menambahkan review kepada restoran yang sebelumnya sudah pernah dipesan.                        |
| **Penjual** | Tidak memiliki fitur ini.                                                                      |
| **Admin**   | Admin dapat menghapus suatu review dari sebuah restoran.

## Sumber dataset kuliner Jogja

[Kaggle](https://www.kaggle.com/datasets/yudhaislamisulistya/places-to-eat-in-the-jogja-region)

## Role atau Peran
**1. Pembeli**

Peran utama di aplikasi, pembeli dapat membeli makanan dari sebuah restoran, menambahkan makanan kepada wishlist, dan menulis review terhadap suatu restoran.

**2. Penjual**

Penjual dapat memodifikasi makanan yang terdapat di restoran yang dimilikinya.

**3. Admin Aplikasi**

Admin dapat menambahkan, memodifikasi, dan menghapus restoran yang terdapat dalam aplikasi, menambahkan promo untuk digunakan oleh pembeli, dan menghapus review yang ditujukan kepada suatu restoran.

