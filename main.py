import numpy as np
import pyautogui
import time
import random
import cv2
from io import BytesIO
from PIL import Image
from ultralytics import YOLO
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# KENDİ BİLGİSAYARIN İÇİN BULDUĞUN O KUSURSUZ PAYI BURAYA YAZ (Örn: 90, 100, 130)
TARAYICI_PAYI = 100 

# --- 1. BEYİN VE KÖK SÖZLÜĞÜ ---
print("Yapay zeka modeli yükleniyor...")
model = YOLO("best.pt")

HEDEF_SOZLUK = {
    "yaya": "Crosswalk",
    "lamba": "Traffic Light",
    "otobüs": "Bus",
    "bisiklet": "Bicycle",
    "motosiklet": "Motorcycle",
    "yangın": "Hydrant",
    "musluk": "Hydrant",
    "araba": "Car",
    "araç": "Car",
    "köprü": "Bridge",
    "merdiven": "Stair",
    "baca": "Chimney",
    "palmiye": "Palm"
}

# --- 2. İNSANSI FARE HAREKETİ ---
def human_like_mouse_move(start_x, start_y, end_x, end_y):
    cp1_x = start_x + random.randint(-80, 80)
    cp1_y = start_y + random.randint(-80, 80)
    cp2_x = end_x + random.randint(-80, 80)
    cp2_y = end_y + random.randint(-80, 80)
    
    steps = random.randint(35, 55)
    for t in range(steps + 1):
        t /= steps
        x = (1-t)**3 * start_x + 3*(1-t)**2 * t * cp1_x + 3*(1-t) * t**2 * cp2_x + t**3 * end_x
        y = (1-t)**3 * start_y + 3*(1-t)**2 * t * cp1_y + 3*(1-t) * t**2 * cp2_y + t**3 * end_y
        pyautogui.moveTo(x, y)
        time.sleep(random.uniform(0.001, 0.004)) 

# --- 3. ANA OTONOM SİSTEM ---
def main():
    chrome_options = Options()
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument("--disable-blink-features=AutomationControlled") 
    
    driver = webdriver.Chrome(options=chrome_options)
    driver.maximize_window()
    driver.get("https://www.google.com/recaptcha/api2/demo")
    time.sleep(3) 
    driver.execute_script("window.scrollBy(0, 300);")
    time.sleep(1)
    
    try:
        # KUTUYA TIKLAMA AŞAMASI
        iframe = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//iframe[contains(@src, 'recaptcha/api2/anchor')]"))
        )
        location = iframe.location
        size = iframe.size
        hedef_x = location['x'] + (size['width'] / 2)
        hedef_y = location['y'] + (size['height'] / 2) + TARAYICI_PAYI 
        
        human_like_mouse_move(pyautogui.position()[0], pyautogui.position()[1], hedef_x, hedef_y)
        time.sleep(random.uniform(0.2, 0.4))
        pyautogui.click()
        time.sleep(3) 
        
        print("\n[BİLGİ] Master Loop (Ana Görev Döngüsü) Başlıyor...")
        
        basari_onayi = False
        for gorev_turu in range(1, 6): 
            
            driver.switch_to.default_content() 
            try:
                challenge_iframe = WebDriverWait(driver, 3).until(
                    EC.presence_of_element_located((By.XPATH, "//iframe[contains(@src, 'recaptcha/api2/bframe')]"))
                )
                if not challenge_iframe.is_displayed():
                    basari_onayi = True
                    break
            except:
                basari_onayi = True
                break

            iframe_x = challenge_iframe.location['x']
            iframe_y = challenge_iframe.location['y']
            driver.switch_to.frame(challenge_iframe)
            
            # --- İÇ DÖNGÜ: OKUMA VE IZGARA TARAMASI ---
            tur_sayisi = 1
            while True:
                # 1. HER TURDA GÖREVİ YENİDEN OKU
                talimat_elementi = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'rc-imageselect-instructions')]"))
                )
                talimat_metni = talimat_elementi.text.lower()
                
                hedef_metin_elementi = driver.find_element(By.XPATH, "//div[contains(@class, 'rc-imageselect-desc')]//strong")
                istenen_tam_cumle = hedef_metin_elementi.text.lower()
                
                # --- YENİ ÇAKAL ALGORİTMA: TEK RESİMSE ATLA ---
                if "parça" in talimat_metni or "parça" in istenen_tam_cumle:
                    print(f"\n[ATLA] Gıcık tek resimli test algılandı! Çözmekle uğraşmıyoruz, Yenile (Reload) butonuna basılıyor...")
                    reload_button = driver.find_element(By.ID, "recaptcha-reload-button")
                    rect = reload_button.rect
                    btn_x = iframe_x + rect['x'] + (rect['width'] / 2)
                    btn_y = iframe_y + rect['y'] + (rect['height'] / 2) + TARAYICI_PAYI
                    
                    human_like_mouse_move(pyautogui.position()[0], pyautogui.position()[1], btn_x, btn_y)
                    time.sleep(random.uniform(0.2, 0.4))
                    pyautogui.click()
                    time.sleep(3) # Yeni resmin ve sorunun gelmesini bekle
                    continue # Döngüyü başa sar, yeni soruyu oku!
                
                # Tek resim değilse normal akışa devam et
                istenen_sinif_en = "Unknown"
                for tr_kok, en_sinif in HEDEF_SOZLUK.items():
                    if tr_kok in istenen_tam_cumle:
                        istenen_sinif_en = en_sinif
                        break
                
                is_dinamik = any(kelime in talimat_metni for kelime in ["kalmayana", "yeni", "kaybol", "değiş"])
                
                print(f"\n--- GÖREV ANALİZİ (TUR {tur_sayisi}) ---")
                if is_dinamik:
                    print(f"[TİP] DİNAMİK GÖREV! (Solan resimler)")
                else:
                    print(f"[TİP] STATİK GÖREV! (Tek seferlik)")
                    
                print(f"[HEDEF] Aranan Kelime Kökü: '{istenen_tam_cumle}' -> YOLO Sınıfı: {istenen_sinif_en}")

                # 2. IZGARAYI PARÇALA VE YOLO'YA SOR
                grid_element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//table[contains(@class, 'rc-imageselect-table')]")) 
                )
                kare_elementleri = driver.find_elements(By.XPATH, "//td[@role='button']")
                
                png_bytes = grid_element.screenshot_as_png
                image = Image.open(BytesIO(png_bytes))
                img_cv2 = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
                
                kare_h = img_cv2.shape[0] // 3
                kare_w = img_cv2.shape[1] // 3
                
                tiklanacak_kare_indexleri = []
                
                kare_no = 0
                for satir in range(3):
                    for sutun in range(3):
                        y1, y2 = satir * kare_h, (satir + 1) * kare_h
                        x1, x2 = sutun * kare_w, (sutun + 1) * kare_w
                        kucuk_kare = img_cv2[y1:y2, x1:x2]
                        
                        results = model(kucuk_kare, verbose=False) 
                        predicted_class = results[0].names[results[0].probs.top1]
                        confidence = results[0].probs.top1conf.item()
                        
                        if predicted_class == istenen_sinif_en and confidence > 0.25:
                            tiklanacak_kare_indexleri.append(kare_no)
                        kare_no += 1
                
                # EĞER HEDEF KALMADIYSA DÖNGÜDEN ÇIK (BUTONA BASMAYA GİT)
                if len(tiklanacak_kare_indexleri) == 0:
                    print(f"[BİLGİ] Ekranda hedef kalmadı. Butona basılacak...")
                    break 
                    
                # HEDEFLERE TIKLA
                print(f"[HAREKET] Bulunan {len(tiklanacak_kare_indexleri)} hedefe tıklanıyor...")
                for index in tiklanacak_kare_indexleri:
                    hedef_element = kare_elementleri[index]
                    rect = hedef_element.rect
                    kare_hedef_x = iframe_x + rect['x'] + (rect['width'] / 2)
                    kare_hedef_y = iframe_y + rect['y'] + (rect['height'] / 2) + TARAYICI_PAYI
                    
                    human_like_mouse_move(pyautogui.position()[0], pyautogui.position()[1], kare_hedef_x, kare_hedef_y)
                    time.sleep(random.uniform(0.2, 0.4))
                    pyautogui.click()
                    time.sleep(random.uniform(0.3, 0.5))
                
                if not is_dinamik:
                    break 
                    
                print("[BEKLEME] Dinamik görev: 3 saniye bekleniyor...")
                time.sleep(3) 
                tur_sayisi += 1
                
            # SAYFA BİTTİ -> BUTONA BAS (Doğrula veya Atla)
            print(f"[HAREKET] Sayfa bitti. Onay butonuna basılıyor...")
            verify_button = driver.find_element(By.ID, "recaptcha-verify-button")
            rect = verify_button.rect
            btn_x = iframe_x + rect['x'] + (rect['width'] / 2)
            btn_y = iframe_y + rect['y'] + (rect['height'] / 2) + TARAYICI_PAYI
            
            human_like_mouse_move(pyautogui.position()[0], pyautogui.position()[1], btn_x, btn_y)
            time.sleep(random.uniform(0.2, 0.5))
            pyautogui.click()
            time.sleep(3) 
            
        if basari_onayi:
            print("\n*** GÖREV BAŞARIYLA TAMAMLANDI! (YEŞİL TİK ALINDI) ***")
        else:
            print("\n[SİSTEM] Çok fazla sayfa geldiği için güvenlik nedeniyle işlem durduruldu.")
            
        time.sleep(10)
        
    except Exception as e:
        print(f"\nSİSTEM HATASI: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()