# Deep Learning and Bezier Curve-Based Autonomous Web Bot

Bu proje, YOLOv8 nesne tespiti mimarisini ve Bezier eğrilerini (Bezier Curves) kullanarak dinamik reCAPTCHA doğrulamalarını otonom bir şekilde aşan entegre bir yapay zeka otomasyonudur.

## 🚀 Mimarinin Öne Çıkan Özellikleri
* **YOLOv8 ile Hassas Tespit:** reCAPTCHA görsellerindeki istenen nesneler (örneğin; trafik lambası, yaya geçidi) YOLOv8 derin öğrenme modeli (`best.pt`) ile yüksek doğrulukla tespit edilir.
* **İnsansı Fare Hareketleri (Bezier Curves):** Botun bot olduğunun anlaşılmaması için fare imleci doğrusal (düz bir çizgi) gitmez. Bezier eğrileri kullanılarak insansı, kavisli ve rastgele hızlarda hareketler simüle edilir.
* **Stealth Otomasyon:** Web etkileşimleri Selenium tabanlı gizlilik (stealth) modülleriyle entegre edilmiştir.
* **Karar Döngüsü (Finite State-Machine):** Sistemin karşılaşabileceği farklı reCAPTCHA senaryolarına karşı mantıksal bir durum makinesi tasarlanmıştır.

## 📁 Proje Dosyaları
* `main.py`: Otonom botu başlatan, görüntü işleme ve tarayıcı otomasyonunu yöneten ana betik.
* `best.pt`: reCAPTCHA veri setleri üzerinde eğitilmiş YOLOv8 model ağırlığı.

## 🛠️ Kullanılan Teknolojiler
* Python
* YOLOv8 (Ultralytics)
* Selenium (Stealth Automation)
* OpenCV & NumPy

## 💻 Nasıl Çalıştırılır?
**Not:** Bu projeyi çalıştırmak için sanal ortam (venv) kullanmanız tavsiye edilir.

1. Depoyu bilgisayarınıza klonlayın.
2. Gerekli kütüphaneleri yükleyin:
```bash
pip install ultralytics selenium opencv-python numpy
python main.py
