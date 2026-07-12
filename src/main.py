import os
import sys
from scanner import CodeScanner
from evaluator import SecurityEvaluator

def main():
    print("=" * 60)
    print("🛡️  Fable 5 Otonom Siber Güvenlik ve Kod Denetim Ajanı")
    print("=" * 60)

    # 1. Taranacak Hedef Dizin
    target_directory = os.path.join("..", "tests", "vulnerable_app")
    
    if not os.path.exists(target_directory):
        print(f"[!] Hata: Target dizin bulunamadı: {target_directory}")
        return

    # 2. Kod Tarayıcıyı Çalıştır
    print(f"\n[*] Hedef dizin taranıyor: '{target_directory}'...")
    scanner = CodeScanner(target_directory)
    scanned_files = scanner.scan()

    if not scanned_files:
        print("[!] Taranacak uyumlu kod dosyası bulunamadı.")
        return

    print(f"[✓] Toplam {len(scanned_files)} dosya analize hazır.\n")

    # 3. Claude Fable 5 Evaluator'ı Başlat
    try:
        evaluator = SecurityEvaluator()
    except Exception as e:
        print(f"[!] Evaluator başlatılamadı (.env dosyanızı ve API key'i kontrol edin): {e}")
        return

    # 4. Her Dosya İçin Otonom Güvenlik Analizi
    for file_info in scanned_files:
        file_path = file_info["file_path"]
        print(f"🔍 [{file_path}] üzerinde Fable 5 derin analizi yürütülüyor...")
        
        try:
            result = evaluator.evaluate_code(file_path, file_info["content"])
            
            # Sonuçları Terminale Yazdır
            print("\n" + "-" * 40)
            print(f"📌 Zafiyet Durumu : {result.get('vulnerability_found')}")
            print(f"⚠️  Riske Seviyesi   : {result.get('severity')}")
            print(f"🐛 Açık Türü        : {result.get('vulnerability_type')}")
            print(f"📝 Açıklama         : {result.get('explanation')}")
            print("-" * 40)

            # Eğer Zafiyet Bulunduysa Yamayı (Patch) Otomatik Uygula
            if result.get("vulnerability_found") and result.get("patched_code"):
                patched_file_path = file_path.replace(".py", "_patched.py")
                
                with open(patched_file_path, "w", encoding="utf-8") as f:
                    f.write(result.get("patched_code"))
                    
                print(f"🛠️  [Otonom Düzeltme] Yamalanmış güvenli kod yazıldı: {patched_file_path}\n")
                
        except Exception as e:
            print(f"[!] {file_path} analiz edilirken hata oluştu: {e}\n")

if __name__ == "__main__":
    main()