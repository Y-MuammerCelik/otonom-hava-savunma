# Otonom Hava Savunma ve Tehdit Skorlama Sistemi 🚀

Bu proje, asimetrik harp ortamlarındaki hava savunma operasyonlarında karşılaşılan radar belirsizliklerini yönetmek üzere tasarlanmış **Bulanık Mantık (Fuzzy Logic)** tabanlı modern bir karar destek sistemidir.

Klasik savunma sistemlerinin keskin eşik değerlerine dayalı katı kararlarının aksine, bu sistem radar verilerini insan mantığına yakın esnek dilsel terimlerle işler. "Oldukça yakın", "çok hızlı" veya "alçaktan uçan" gibi belirsizlik içeren durumları hassasiyetle modelleyerek, hedeflerin tehdit skorunu hesaplar ve operatöre angajman tavsiyesi sunar.

---

## 🌟 Sistemin Öne Çıkan Özellikleri

- **Mamdani Bulanık Çıkarım Motoru**: Mesafe, hız ve irtifa girişlerini işleyerek tehdit skoru üreten, `scikit-fuzzy` kullanılarak geliştirilmiş 15 kuraldan oluşan güçlü bir kural tabanı.
- **Dinamik ve Modern Arayüz**: Streamlit ile askeri radar teması çerçevesinde tasarlanmış, akıcı ve kullanıcı dostu bir kontrol paneli.
- **Açıklanabilir Yapay Zeka (XAI)**: Sistemin hangi kararı neden verdiğini şeffaf bir şekilde gösteren Kural Aktivasyon Analizi. Hangi kuralın yüzde kaç aktivasyon ile tetiklendiğini anlık olarak görebilirsiniz.
- **Anlık Görsel Analizler**: Matplotlib entegrasyonu ile üyelik fonksiyonlarının ve durulaştırma (defuzzification) grafiklerinin anlık olarak çizilmesi.
- **PDF Sonuç Raporu**: Yapılan analiz sonucunu hızlı bir şekilde tek sayfalık akademik/profesyonel bir PDF raporuna dönüştürebilme özelliği.

---

## 📂 Dosya Yapısı

- `app.py`: Bulanık çıkarım motorunu, matematiksel modeli ve Streamlit arayüzünü barındıran projenin kalbi.
- `generate_pdf.py`: Yapılan analiz sonucuna göre ReportLab kullanarak otomatik PDF raporu üreten destekleyici betik.
- `requirements.txt`: Projenin sorunsuz çalışması için gereken Python kütüphaneleri.

---

## ⚙️ Kurulum ve Çalıştırma Rehberi

Sistemi kendi bilgisayarınızda çalıştırmak oldukça basittir. Python 3.8 veya üzeri bir sürümün yüklü olduğundan emin olduktan sonra aşağıdaki adımları izleyin:

### 1. Bağımlılıkların Yüklenmesi
Öncelikle gerekli Python kütüphanelerini kurmak için proje dizininde bir terminal veya PowerShell penceresi açın ve şu komutu çalıştırın:

```bash
pip install -r requirements.txt
```

### 2. Sistemin Başlatılması
Kurulum tamamlandıktan sonra, Streamlit sunucusunu başlatmak için şu komutu girin:

```bash
streamlit run app.py
```
Komutu çalıştırdığınızda varsayılan web tarayıcınız otomatik olarak açılacak ve **http://localhost:8501** adresinden sisteme erişebileceksiniz.

---

## 🎯 Test Senaryoları

Sistem, çeşitli tehdit profillerini analiz etmek için varsayılan senaryolarla birlikte gelir. Arayüzün sol panelinden bu şablonları anında sisteme yükleyebilirsiniz:

1. **Kamikaze İHA Yaklaşması** 
   *(Çok yakın mesafe, yavaş hız, çok düşük irtifa)*
   Sistem bu profili asimetrik bir tehdit olarak algılar ve yüksek tehdit skoru üretir.

2. **Ticari Uçuş Geçişi** 
   *(Uzak mesafe, yüksek hız, çok yüksek irtifa)*
   Sistem bu durumu sivil havacılık profili ile eşleştirir ve düşük tehdit uyarısı verir.

3. **Seyir Füzesi (Cruise Missile) ve Balistik Füze Geçişleri**
   Farklı hız ve irtifa kombinasyonlarıyla daha dinamik tehdit algılama analizleri.

---

*Geliştiren:* Muammer Çelik
