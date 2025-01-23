import tkinter as tk
import qrcode
from PIL import Image, ImageDraw
from tkinter import filedialog
from tkinter import messagebox

class QRDings:
    def __init__(self, master):
        self.master = master
        self.Programm_Name = "QR-Code Generator"
        self.Version = "0.0.1"
        print(f"[-VERSION-] {self.Version}")
        self.Zeit = "Die Zeit ist eine Illusion."
        master.title(self.Programm_Name + " " + self.Version)

        self.output_path = None
        self.data = None

        self.Inhalt_eingabe = tk.Entry(root, width=50)
        self.Inhalt_eingabe.place(x=10,y=100)

        self.Erstellen_mit_Bild = tk.Button(root, text="Mit Bild erstellen", command=self.Daten_vorbereiten)
        self.Erstellen_mit_Bild.place(x=100,y=190)

    def Daten_vorbereiten(self):
        self.data = None
        self.data = self.Inhalt_eingabe.get()
        if self.data == "" or None:
            messagebox.showerror(title=self.Programm_Name, message="Bitte geben Sie zuerst einen Inhalt an!")
            return
        else:
            self.data.strip()
        self.output_path = filedialog.asksaveasfilename(title="QR-Code speichern unter...", defaultextension=".png",filetypes=[("Bild", "*.png"), ("Alle Dateien", "*.*"),])
        if self.output_path:
            self.code_erstellen_mit_bild()
        else:
            messagebox.showinfo(title=self.Programm_Name, message="Vorgang wurde abgebrochen.")


    def code_erstellen_mit_bild(self):
        empty_center_ratio = 0.3
        qr_size = 500
        data = self.data
        output_path = self.output_path
        # QR-Code generieren
        qr = qrcode.QRCode(
            error_correction=qrcode.constants.ERROR_CORRECT_H  # Hoher Fehlerkorrekturgrad für das Bild in der Mitte
        )
        qr.add_data(data)
        qr.make(fit=True)

        # QR-Code als Bild erstellen
        hauptfarbe = 57, 147, 133, 255 # #399385
        qr_img = qr.make_image(fill=hauptfarbe, back_color="white").convert("RGBA")
        qr_img = qr_img.resize((qr_size, qr_size), Image.LANCZOS)  


        empty_center_size = int(qr_size * empty_center_ratio)
        center_x, center_y = (qr_size - empty_center_size) // 2, (qr_size - empty_center_size) // 2
        draw = ImageDraw.Draw(qr_img)
        draw.rectangle(
            [center_x, center_y, center_x + empty_center_size, center_y + empty_center_size],
            fill="white"
        )


        qr_img.save(output_path)
        print(f"QR-Code mit leerem Bereich in der Mitte erfolgreich als '{output_path}' gespeichert.")
        output_path = None
        self.data = None

if __name__ == "__main__":
    root = tk.Tk()
    width = 420
    height = 690
    def mittig_fenster(root, width, height):
        root.update_idletasks()
        fenster_breite = root.winfo_screenwidth()
        fenster_höhe = root.winfo_screenheight()
        x = (fenster_breite - width) // 2
        y = (fenster_höhe - height) // 2
        root.geometry(f"{width}x{height}+{x}+{y}") # Das ist da um das Fenster mittig aufm Hauptmonitor zu spawnen, funktioniert in 30% der Fälle..
    mittig_fenster(root, width, height)
    QRDings = QRDings(root)
    root.mainloop()