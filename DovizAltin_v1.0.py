import customtkinter as ctk
import requests
import datetime
import threading

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# --- Verileri Çekme ---
def fetch_data():
    try:
        r = requests.get("https://finans.truncgil.com/today.json", timeout=8)
        data = r.json()
        return data
    except Exception:
        return {}

# --- Arayüz ---
class DovizAltinApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("💱 Döviz & Altın Takipçisi v1.0")
        self.geometry("580x500")
        self.resizable(False, False)

        title = ctk.CTkLabel(self, text="💱 Döviz & Altın Takipçisi", font=("Segoe UI", 22, "bold"))
        title.pack(pady=(10,5))

        self.status = ctk.CTkLabel(self, text="Veriler yükleniyor...", font=("Segoe UI", 12))
        self.status.pack(pady=5)

        # Döviz kartları
        self.doviz_cards = {}
        doviz_frame = ctk.CTkFrame(self)
        doviz_frame.pack(fill="x", padx=10, pady=5)

        for key, name in [
            ("USD", "Amerikan Doları (USD)"),
            ("EUR", "Euro (EUR)"),
            ("GBP", "İngiliz Sterlini (GBP)"),
        ]:
            frame = ctk.CTkFrame(doviz_frame, corner_radius=10)
            frame.pack(side="left", expand=True, fill="both", padx=5, pady=5)
            lbl = ctk.CTkLabel(frame, text=name, font=("Segoe UI", 13, "bold"))
            lbl.pack(pady=(8,0))
            val = ctk.CTkLabel(frame, text="— ₺", font=("Segoe UI", 20, "bold"))
            val.pack(pady=8)
            self.doviz_cards[key] = val

        # Altın kısmı
        gold_frame = ctk.CTkFrame(self)
        gold_frame.pack(fill="x", padx=10, pady=10)

        self.gold_labels = {}
        for key, name in [
            ("gram-altin", "Gram Altın"),
            ("ceyrek-altin", "Çeyrek Altın"),
            ("yarim-altin", "Yarım Altın"),
            ("tam-altin", "Tam Altın"),
            ("cumhuriyet-altini", "Cumhuriyet Altını"),
        ]:
            lbl = ctk.CTkLabel(gold_frame, text=f"{name}: — ₺", font=("Segoe UI", 14))
            lbl.pack(anchor="w", padx=8, pady=3)
            self.gold_labels[key] = lbl

        # Zaman etiketi
        self.time_label = ctk.CTkLabel(self, text="Son güncelleme: —", font=("Segoe UI", 11))
        self.time_label.pack(pady=5)

        # Yenile butonu (büyük)
        self.refresh_button = ctk.CTkButton(
            self, text="🔄 Yenile", command=self.refresh,
            width=200, height=40, font=("Segoe UI", 14, "bold")
        )
        self.refresh_button.pack(pady=(10,15))

        # Alt yazı
        footer = ctk.CTkLabel(self, text="Powered by Ferit Oflaz", font=("Segoe UI", 10))
        footer.pack(side="bottom", pady=(0,5))

        threading.Thread(target=self.refresh, daemon=True).start()

    def refresh(self):
        self.status.configure(text="Veriler alınıyor...")
        data = fetch_data()
        self.update_ui(data)

    def update_ui(self, data):
        # Döviz kısmı
        for k in ("USD", "EUR", "GBP"):
            if k in data:
                fiyat = data[k]["Satış"]
                self.doviz_cards[k].configure(text=f"{fiyat} ₺")
            else:
                self.doviz_cards[k].configure(text="— ₺")

        # Altın kısmı
        for k in self.gold_labels.keys():
            if k in data:
                fiyat = data[k]["Satış"]
                self.gold_labels[k].configure(text=f"{self.gold_labels[k].cget('text').split(':')[0]}: {fiyat} ₺")
            else:
                self.gold_labels[k].configure(text=f"{self.gold_labels[k].cget('text').split(':')[0]}: — ₺")

        now = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        self.time_label.configure(text=f"Son güncelleme: {now}")
        self.status.configure(text="Veriler güncellendi ✅")


if __name__ == "__main__":
    app = DovizAltinApp()
    app.mainloop()
