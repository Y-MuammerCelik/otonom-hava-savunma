# Bulanık Mantık Dersi – Dönem Projesi Raporu
**Proje Adı:** Otonom Hava Savunma ve Tehdit Skorlama Sistemi
**Hazırlayan:** Muammer Çelik

---

## 1. Giriş ve Problem Tanımı

### 1.a. Gerçek Dünya Probleminin Sunulması
Günümüz asimetrik harp sahasında, sınır güvenliği ve hava savunma sistemleri, hedefleri tespit ve teşhis ederken yüksek belirsizlik içeren sensör ve radar verileriyle çalışmak zorundadır. Radarlardan alınan mesafe, hız ve irtifa gibi parametreler; sensör gürültüleri, sinyal bozucular (jamming) ve özellikle kamikaze İHA'lar gibi düşük radar kesit alanına (RCS) sahip hedeflerin öngörülemez hareketleri nedeniyle her zaman kesin ($0$ veya $1$) değerler ifade etmez. 

### 1.b. Problemdeki İlgili Giriş ve Çıkış Değişkenleri
Bu belirsizlik ortamında karar verici sistemin değerlendirmesi gereken 3 ana giriş değişkeni bulunmaktadır:
- **Giriş 1:** Hedefin Bataryaya Mesafesi (km)
- **Giriş 2:** Hedefin Yaklaşma Hızı (km/h)
- **Giriş 3:** Hedefin Uçuş İrtifası (m)

Sistemin üretmesi beklenen çıkış değişkeni:
- **Çıkış:** Angajman Tavsiyesi ve Tehdit Skoru (%)

### 1.c. Sistemin Bulanık Mantıkla Çözülmesinin Gerekçelendirilmesi
Klasik kontrol (Boolean) sistemleri keskin eşik değerleriyle çalışır. Örneğin kural "EĞER Hız > 500 İSE Tehdit Yüksek" şeklinde belirlendiğinde, hızın 499 km/h olduğu bir durumda sistem hedefi tamamen göz ardı edebilir. Bu durum hava savunması gibi ölümcül sonuçları olabilecek bir alanda kabul edilemez bir zafiyettir. Bulanık mantık (Fuzzy Logic), "oldukça yakın", "biraz hızlı" veya "çok alçaktan uçan" gibi insan kararına ve mantığına yakın esnek dilsel değişkenleri işleyebildiği için bu problemin çözümünde kullanılabilecek en ideal matematiksel modeldir.

---

## 2. Sistem Tasarımı

### 2.a. Giriş Çıkış Değişkenlerinin Tanımlanması
Projede tanımlanan değişkenler ve evren (universe) aralıkları şu şekildedir:
- **Mesafe:** $0$ ile $100$ km aralığında tanımlanmıştır.
- **Hız:** $0$ ile $1200$ km/h aralığında tanımlanmıştır.
- **İrtifa:** $0$ ile $10000$ metre aralığında tanımlanmıştır.
- **Tehdit Skoru (Çıkış):** $0$ ile $100$ (%) aralığında tanımlanmıştır.

### 2.b. Üyelik Fonksiyonları
Hesaplama maliyetini düşük tutmak ve sistemi hızlı çalıştırmak amacıyla tüm değişkenler için **Üçgensel Üyelik Fonksiyonları (trimf)** tercih edilmiştir.

1. **Mesafe:**
   - Yakın: $[0, 0, 50]$
   - Orta: $[20, 50, 80]$
   - Uzak: $[50, 100, 100]$
2. **Hız:**
   - Yavaş: $[0, 0, 500]$
   - Normal: $[300, 600, 900]$
   - Hızlı: $[700, 1200, 1200]$
3. **İrtifa:**
   - Düşük: $[0, 0, 4000]$
   - Orta: $[2000, 5000, 8000]$
   - Yüksek: $[6000, 10000, 10000]$
4. **Tehdit Skoru (Çıkış):**
   - Düşük: $[0, 0, 50]$
   - Orta: $[25, 50, 75]$
   - Yüksek: $[50, 100, 100]$

### 2.c. Kural Tabanı (Rule Base)
Sistem için hava savunma doktrinlerine (örneğin alçaktan ve hızlı gelen cisimlerin yüksek tehdit olması) uygun olarak $15$ adet IF-THEN kuralı oluşturulmuştur:

1. IF (Mesafe Yakın) AND (Hız Hızlı) AND (İrtifa Düşük) THEN (Tehdit Yüksek)
2. IF (Mesafe Yakın) AND (Hız Yavaş) AND (İrtifa Düşük) THEN (Tehdit Yüksek)
3. IF (Mesafe Yakın) AND (Hız Hızlı) AND (İrtifa Yüksek) THEN (Tehdit Yüksek)
4. IF (Mesafe Yakın) AND (Hız Normal) AND (İrtifa Orta) THEN (Tehdit Yüksek)
5. IF (Mesafe Yakın) AND (Hız Yavaş) AND (İrtifa Yüksek) THEN (Tehdit Orta)
6. IF (Mesafe Orta) AND (Hız Hızlı) AND (İrtifa Düşük) THEN (Tehdit Yüksek)
7. IF (Mesafe Orta) AND (Hız Normal) AND (İrtifa Orta) THEN (Tehdit Orta)
8. IF (Mesafe Orta) AND (Hız Yavaş) AND (İrtifa Düşük) THEN (Tehdit Orta)
9. IF (Mesafe Orta) AND (Hız Hızlı) AND (İrtifa Yüksek) THEN (Tehdit Yüksek)
10. IF (Mesafe Uzak) AND (Hız Normal) AND (İrtifa Orta) THEN (Tehdit Düşük)
11. IF (Mesafe Uzak) AND (Hız Yavaş) AND (İrtifa Düşük) THEN (Tehdit Düşük)
12. IF (Mesafe Uzak) AND (Hız Hızlı) AND (İrtifa Yüksek) THEN (Tehdit Düşük)
13. IF (Mesafe Uzak) AND (Hız Yavaş) AND (İrtifa Yüksek) THEN (Tehdit Düşük)
14. IF (Mesafe Uzak) AND (Hız Hızlı) AND (İrtifa Düşük) THEN (Tehdit Orta)
15. IF (Mesafe Orta) AND (Hız Yavaş) AND (İrtifa Yüksek) THEN (Tehdit Düşük)

### 2.d. Çıkarım Motoru
Bulanık çıkarım mekanizması olarak **Mamdani Çıkarım Motoru** kullanılmıştır. Kural öncülleri (antecedent) birleştirilirken mantıksal AND operatörü (minimum alma yöntemi) tercih edilmiştir.

### 2.e. Durulaştırma (Defuzzification)
Mamdani motoru sonucunda elde edilen bulanık küme (birleştirilmiş çıkış alanı), **Ağırlık Merkezi (Centroid)** metodu kullanılarak kesin (crisp) bir sayısal tehdit skoruna (% olarak) dönüştürülmektedir.

---

## 3. Python Uygulamasının Detayları

### 3.a. Kullanılan Kütüphaneler ve Araçlar
Proje Python tabanlı olarak geliştirilmiştir. Bulanık mantık hesaplamaları için `scikit-fuzzy` ve `numpy`; verilerin görselleştirilmesi için `matplotlib`; dinamik ve modern bir web kullanıcı arayüzü sunmak için ise `streamlit` kütüphanesi tercih edilmiştir.

### 3.b. Arayüz Dinamikleri
Kullanıcı, arayüzdeki "Slider (Kaydırıcı)" veya "Metin Kutusu" yardımıyla hedefin mesafe, hız ve irtifa bilgilerini manuel olarak değiştirebilmektedir. "Sistemi Çalıştır" butonuna basıldığında, bu girişler alınarak bulanık çıkarım motoruna sokulmakta ve sayısal sonuç anlık olarak (% olarak) görsel bir skor kartında sunulmaktadır. Ayrıca, sisteme tek tıkla test edilebilecek hazır senaryo şablonları da entegre edilmiştir.

### 3.c. Grafiksel Gösterim ve XAI (Açıklanabilir Yapay Zeka)
- Giriş değişkenlerinin üyelik fonksiyonları Matplotlib ile çizdirilmekte ve kullanıcının girdiği o anki değerler fonksiyon grafiği üzerinde dik bir çizgi olarak gösterilmektedir.
- Durulaştırma grafiğinde, sistem çıkışında oluşan "Aggregate" (birleşik) alan boyalı olarak gösterilmekte ve ağırlık merkezi (centroid) bir ok ile işaretlenmektedir.
- Arayüzde "Kural Aktivasyon Analizi" paneli yer almaktadır. Hangi kuralın yüzde kaçlık bir aktivasyonla (min değeriyle) tetiklendiği açıkça listelenmekte, sistemin verdiği kararın nedeni şeffaf bir biçimde ispatlanmaktadır.

---

## 4. Sonuç, Değerlendirme ve Test Analizi

### 4.a. Test Senaryoları
Sistemin farklı profillerdeki doğruluğunu test etmek için 2 farklı uç senaryo uygulanmıştır:

**Senaryo 1: Düşük İrtifa Kamikaze İHA Beklentisi**
- *Girişler:* Mesafe: 15 km | Hız: 200 km/h | İrtifa: 500 m
- *Sonuç:* Sistem %81.4 Tehdit Skoru üreterek durumu **YÜKSEK TEHDİT** olarak belirlemiştir. Hedef yavaş olmasına rağmen; "Yakın" ve "Düşük İrtifa" kümelerine yüksek derecede üye olduğu için ilgili kurallar (Kural 2 vb.) baskın gelmiş ve doğru asimetrik tehdit kararı alınmıştır.

**Senaryo 2: Ticari Uçuş Geçişi**
- *Girişler:* Mesafe: 80 km | Hız: 800 km/h | İrtifa: 9000 m
- *Sonuç:* Sistem %22.6 Tehdit Skoru üreterek durumu **DÜŞÜK TEHDİT** olarak belirlemiştir. Hedef yüksek hızlı olmasına rağmen "Uzak" ve "Yüksek İrtifa" profili bir sivil yolcu uçağını andırdığından sistem gereksiz angajmanı önlemiştir.

### 4.b. Sistem Değerlendirmesi
**Güçlü Yönleri:** 
Sistemin en büyük avantajı, karar alma sürecinin %100 "Açıklanabilir" olmasıdır. Derin Öğrenme modelleri gibi bir kara kutu (black-box) değildir; verilen bir vur/vurma kararının matematiksel alt yapısı, hangi kuralların aktive olduğu arayüzde kanıtlanabilir. Ayrıca hesaplama maliyeti son derece düşüktür.

**Zayıf Yönleri ve Güncel Yaklaşımlar:** 
Sistemin zayıf yönü, değişen çevre koşullarına veya yeni geliştirilen düşman hava araçlarının profillerine karşı kendi kendine öğrenme yeteneği olmamasıdır. Kurallar uzman bilgisiyle (heuristically) oluşturulmuştur. Güncel yaklaşımlarda bu problemi çözmek için Yapay Sinir Ağlarının (ANN) öğrenme kapasitesi ile Bulanık Mantığın açıklanabilirliğini birleştiren **ANFIS (Adaptif Sinirsel Bulanık Çıkarım Sistemleri)** hibrit modelleri kullanılmaktadır. Ancak proje sınırları içerisinde kurgulanan Mamdani modeli görevini son derece başarılı ve tutarlı bir biçimde yerine getirmiştir.
