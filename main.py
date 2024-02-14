import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import json


class To_Do_List:
    def __init__(self, pencere):
        self.pencere = pencere
        self.pencere.title("To-Do List")

        self.görevler = []
        self.tamamlanmıs_görevler = []

        self.ana_pencere()

    def pencere1_olustur(self):
        self.ekle_buton = tk.Button(self.pencere, text="Görev Ekle", command=self.ekleme_sayfası)
        self.ekle_buton.grid(row=0, column=0, columnspan=2, pady=10)

        self.tablo = ttk.Treeview(self.pencere, columns=("Görev", "Ayrıntılar", "Öncelik Sırası"))
        self.tablo.grid(row=1, column=0, columnspan=2, pady=10)

        self.tamamlandı_buton = tk.Button(self.pencere, text="Tamamlandı", command=self.görev_tamamla)
        self.tamamlandı_buton.grid(row=2, column=0, pady=5)

        self.sil_butonu = tk.Button(self.pencere, text="Sil", command=self.görev_sil)
        self.sil_butonu.grid(row=2, column=1, pady=5)

        self.sıradaki_sayfa_butonu = tk.Button(self.pencere, text="Tamamlanmış Görevler", command=self.tamamlananları_goster)
        self.sıradaki_sayfa_butonu.grid(row=3, column=0, columnspan=2, pady=10)

        self.pencere.protocol("WM_DELETE_WINDOW", self.kapama)

        self.tablo.bind("<Button-1>", self.görevin_ayrıntıları)

        self.görev_gosterme()

    def kapama(self):
        self.kaydet()
        self.pencere.destroy()

    def ekleme_sayfası(self):
        pencere1 = tk.Toplevel(self.pencere)
        pencere1.title("Görev Ekle")

        görev_girme = tk.Label(pencere1, text="Görev İsmi:")
        görev_girme.grid(row=0, column=0, padx=5, pady=5)
        görev_gir = tk.Entry(pencere1)
        görev_gir.grid(row=0, column=1, padx=5, pady=5)

        ayrıntılar = tk.Label(pencere1, text="Ayrıntılar:")
        ayrıntılar.grid(row=1, column=0, padx=5, pady=5)
        ayrıntı_gir = tk.Entry(pencere1)
        ayrıntı_gir.grid(row=1, column=1, padx=5, pady=5)

        öncelikt = tk.Label(pencere1, text="Önem Sırası (1-10):")
        öncelikt.grid(row=2, column=0, padx=5, pady=5)
        öncelik_girme = tk.Spinbox(pencere1, from_=1, to=10)
        öncelik_girme.grid(row=2, column=1, padx=5, pady=5)

        ekle_buton = tk.Button(pencere1, text="Ekle", command=lambda: self.görev_ekle(pencere1, görev_gir, ayrıntı_gir, öncelik_girme))
        ekle_buton.grid(row=3, column=1, pady=10)

    def görev_ekle(self, pencere1, görev_gir, ayrıntı_gir, öncelik_gir):
        görev_ad = görev_gir.get()
        detay = ayrıntı_gir.get()
        öncelik = öncelik_gir.get()

        if görev_ad and detay and öncelik:
            try:
                öncelik = int(öncelik)
                if not any(gorev[2] == öncelik for gorev in self.görevler):
                    if 1 <= öncelik <= 10:
                        görev_bilgi = (görev_ad, detay, öncelik, False)
                        self.görevler.append(görev_bilgi)
                        self.görev_gosterme()
                        pencere1.destroy()
                    else:
                        messagebox.showwarning("Hata", "Önem sırası 1 ile 10 arasında olmalıdır.")
                else:
                    messagebox.showwarning("Hata", "Bu önceliğe sahip başka bir görev zaten var.")
            except ValueError:
                messagebox.showwarning("Hata", "Önem sırası bir sayı olmalıdır.")
        else:
            messagebox.showwarning("Hata", "Lütfen tüm alanları doldurun.")

    def görev_gosterme(self):
        for i in self.tablo.get_children():
            self.tablo.delete(i)

        self.görevler.sort(key=lambda x: x[2])

        for a, bilgi in enumerate(self.görevler, start=1):
            ad, ayrıntı, öncelik, tamamlama = bilgi
            task_label = tk.Label(self.tablo, text=f"{a}. {ad}")
            self.tablo.insert("", "end", values=(ad, ayrıntı, öncelik), iid=a)


    def görev_düzeni(self):
        seçilen = self.tablo.selection()
        if seçilen:
            a = int(seçilen[0])
            bilgi = self.görevler[a - 1]

            düzenle_pencere1 = tk.Toplevel(self.pencere)
            düzenle_pencere1.title("Görevi Düzenle")

            tk.Label(düzenle_pencere1, text="Görev İsmi:").grid(row=0, column=0, padx=5, pady=5)
            tk.Entry(düzenle_pencere1, textvariable=tk.StringVar(value=bilgi[0])).grid(row=0, column=1, padx=5,pady=5)

            tk.Label(düzenle_pencere1, text="Ayrıntılar:").grid(row=1, column=0, padx=5, pady=5)
            tk.Entry(düzenle_pencere1, textvariable=tk.StringVar(value=bilgi[1])).grid(row=1, column=1, padx=5,pady=5)

            tk.Label(düzenle_pencere1, text="Önem Sırası (1-10):").grid(row=2, column=0, padx=5, pady=5)
            tk.Entry(düzenle_pencere1, textvariable=tk.StringVar(value=bilgi[2])).grid(row=2, column=1, padx=5,pady=5)

            tk.Button(düzenle_pencere1, text="Kaydet", command=lambda: self.degistir(düzenle_pencere1, a)).grid(row=3, column=1, pady=10)

    def degistir(self, pencere2, idx):
        görev_adı = pencere2.children["!entry"].get()
        ayrıntılar = pencere2.children["!entry2"].get()
        öncelik = pencere2.children["!entry3"].get()

        if görev_adı and ayrıntılar and öncelik:
            try:
                öncelik = int(öncelik)
                if 1 <= öncelik <= 10:
                    self.görevler[idx - 1] = (görev_adı, ayrıntılar, öncelik, False)
                    self.görev_gosterme()
                    pencere2.destroy()
                else:
                    messagebox.showwarning("Hata", "Önem sırası 1 ile 10 arasında olmalıdır.")
            except ValueError:
                messagebox.showwarning("Hata", "Önem sırası bir sayı olmalıdır.")
        else:
            messagebox.showwarning("Hata", "Lütfen tüm alanları doldurun.")

    def görev_tamamla(self):
        secilen = self.tablo.selection()
        if secilen:
            a = int(secilen[0])
            görev_bilgi = self.görevler[a - 1]
            gorevad, detay, oncelik, tamamlama = görev_bilgi
            if not tamamlama:
                self.görevler[a - 1] = (gorevad, detay, oncelik, True)
                self.tamamlanmıs_görevler.append(görev_bilgi)
                del self.görevler[a - 1]
                self.görev_gosterme()
            else:
                messagebox.showwarning("Hata", "Bu görev zaten tamamlandı.")
        else:
            messagebox.showwarning("Hata", "Lütfen tamamlamak istediğiniz görevi seçin.")

    def görev_sil(self):
        secilen = self.tablo.selection()
        if secilen:
            a = int(secilen[0])
            del self.görevler[a - 1]
            self.görev_gosterme()
        else:
            messagebox.showwarning("Hata", "Lütfen silmek istediğiniz görevi seçin.")

    def tamamlananları_goster(self):
        diger_sayfa = tk.Toplevel(self.pencere)
        diger_sayfa.title("Tamamlanan Görevler")

        completed_label = tk.Label(diger_sayfa, text="Tamamlanan Görevler")
        completed_label.grid(row=0, column=0, pady=10)

        tam_tablo = ttk.Treeview(diger_sayfa, columns=("Task", "Details", "Priority"), show="headings")
        tam_tablo.heading("Task", text="Görev")
        tam_tablo.heading("Details", text="Ayrıntılar")
        tam_tablo.heading("Priority", text="Önem Sırası")
        tam_tablo.grid(row=1, column=0, pady=10)

        for a, bilgi in enumerate(self.tamamlanmıs_görevler, start=1):
            task_name, details, priority, completed = bilgi
            tam_tablo.insert("", "end", values=(task_name, details, priority), iid=a)

        self.kaydet_tamamlananları()

    def ana_pencere(self):
        self.ekle_buton = tk.Button(self.pencere, text="Görev Ekle", command=self.ekleme_sayfası, foreground="red",
                                    background="light blue", width=10, height=4)
        self.ekle_buton.grid(row=0, column=0, columnspan=2, pady=10)

        self.tablo = ttk.Treeview(self.pencere, columns=("Görev", "Ayrıntılar", "Önem Sırası"), show="headings")
        self.tablo.heading("Görev", text="Görev")
        self.tablo.heading("Ayrıntılar", text="Ayrıntılar")
        self.tablo.heading("Önem Sırası", text="Önem Sırası")
        self.tablo.grid(row=1, column=0, columnspan=2, pady=10)

        self.tamamlandı_buton = tk.Button(self.pencere, text="Tamamlandı", command=self.görev_tamamla)
        self.tamamlandı_buton.grid(row=2, column=0, pady=5)

        self.sil_butonu = tk.Button(self.pencere, text="Sil", command=self.görev_sil)
        self.sil_butonu.grid(row=2, column=1, pady=5)

        self.duzen_butonu = tk.Button(self.pencere, text="Düzenle", command=self.görev_düzeni)
        self.duzen_butonu.grid(row=3, column=0, columnspan=2, pady=10)

        self.sıradaki_sayfa_butonu = tk.Button(self.pencere, text="Tamamlanmış Görevler",
                                               command=self.tamamlananları_goster)
        self.sıradaki_sayfa_butonu.grid(row=4, column=0, columnspan=2, pady=10)

        self.pencere.protocol("WM_DELETE_WINDOW", self.kapama)

        self.tablo.bind("<Button-1>", self.görevin_ayrıntıları)

        self.görev_gosterme()
    def kaydet(self):
        with open("gorevler.json", "w") as f:
            json.dump(self.görevler, f)

    def kaydet_tamamlananları(self):
        with open("tamamlanmıslar.json", "w") as f:
            json.dump(self.tamamlanmıs_görevler, f)

    def yükle(self):
        try:
            with open("gorevler.json", "r") as f:
                self.görevler.extend(json.load(f))
            self.görev_gosterme()
            messagebox.showinfo("Bilgi", "Görevler başarıyla yüklendi.")
        except FileNotFoundError:
            messagebox.showwarning("Hata", "Kaydedilmiş görev bulunamadı.")

    def yükle_tamamlananları(self):
        try:
            with open("tamamlanmıslar.json", "r") as f:
                self.tamamlanmıs_görevler.extend(json.load(f))
        except FileNotFoundError:
            pass

    def görevin_ayrıntıları(self, event):
        basılan = self.tablo.selection()
        if basılan:
            a = int(basılan[0])
            bilgi = self.görevler[a - 1]
            ad, ayrıntı, öncelik, tamamlanmıs = bilgi
            messagebox.showinfo("Görev Detayları", f"Görev: {ad}\nAyrıntılar: {ayrıntı}\nÖnem Sırası: {öncelik}\n")

pencere = tk.Tk()
proje = To_Do_List(pencere)
proje.yükle()
proje.yükle_tamamlananları()
pencere.mainloop()
