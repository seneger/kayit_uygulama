from PyQt5.QtWidgets import QApplication, QMainWindow, QHeaderView, QTableWidgetItem, QMessageBox
from panel import Ui_MainWindow  # panel.py dosyasındaki Ui_MainWindow sınıfını içe aktar
import sys
import pymysql

# Arayüz işlemleri
uygulama = QApplication(sys.argv)
pencere = QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(pencere)
pencere.show()

# Veritabanı bağlantı işlemleri
baglanti = pymysql.connect(
    host="localhost",
    user="root",
    password="Sngr2516.",
    db="deneme",
    charset="utf8mb4",
    cursorclass=pymysql.cursors.DictCursor
)

islem = baglanti.cursor()

# Eğer tablo zaten yoksa oluştur
islem.execute("CREATE TABLE IF NOT EXISTS kayit (Ad TEXT, Soyad TEXT, Sirket TEXT)")
baglanti.commit()

# Tablo başlıklarını ayarlama
ui.tbl1.setHorizontalHeaderLabels(("İSİM", "SOYAD", "SİRKET"))

def kayit_ekle():
    AD = ui.lne1.text()
    SOYAD = ui.lne2.text()
    SIRKET = ui.cmb1.currentText()

    try:
        ekle = "INSERT INTO kayit (Ad, Soyad, Sirket) VALUES (%s, %s, %s)"
        islem.execute(ekle, (AD, SOYAD, SIRKET))
        baglanti.commit()
        ui.statusbar.showMessage("Kayıt eklendi.", 1000)
        kayit_listele()
    except Exception as e:
        ui.statusbar.showMessage(f"Kayıt eklenemedi: {str(e)}", 1000)

def kayit_listele():
    ui.tbl1.clearContents()
    ui.tbl1.setRowCount(0)
    ui.tbl1.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    ui.tbl1.setHorizontalHeaderLabels(("İSİM", "SOYAD", "SİRKET"))
    sorgu = "SELECT * FROM kayit"
    islem.execute(sorgu)
    row = 0
    for deger in islem.fetchall():
        print(deger)  # Terminalde veri olup olmadığını kontrol edin
        ui.tbl1.insertRow(row)  # Her satır için tabloya yeni bir satır ekle
        ui.tbl1.setItem(row, 0, QTableWidgetItem(deger["AD"]))
        ui.tbl1.setItem(row, 1, QTableWidgetItem(deger["SOYAD"]))
        ui.tbl1.setItem(row, 2, QTableWidgetItem(deger["SIRKET"]))
        row += 1

def kayit_sil():
    sil_mesaj = QMessageBox.question(pencere, "Silme Onayı", "Silmek istediğinize emin misiniz?",
                                     QMessageBox.Yes | QMessageBox.No)

    if sil_mesaj == QMessageBox.Yes:
        secilen_kayit = ui.tbl1.selectedItems()

        if secilen_kayit:
            silinecek_kayit = secilen_kayit[0].text()

            sorgu = "DELETE FROM kayit WHERE Ad = %s"
            try:
                islem.execute(sorgu, (silinecek_kayit,))
                baglanti.commit()
                ui.statusbar.showMessage("Kayıt silindi", 1000)
                kayit_listele()
            except Exception as e:
                ui.statusbar.showMessage(f"Kayıt silinemedi: {str(e)}", 1000)
        else:
            ui.statusbar.showMessage("Silinecek kayıt seçilmedi.", 1000)
    else:
        ui.statusbar.showMessage("İşlem iptal edildi", 1000)

def sirkete_gore_sirala():
    listelenecek_sirket = ui.cmb2.currentText()
    sorgu = "SELECT * FROM kayit WHERE Sirket = %s"
    islem.execute(sorgu, (listelenecek_sirket,))
    ui.tbl1.clearContents()
    ui.tbl1.setRowCount(0)
    ui.tbl1.setHorizontalHeaderLabels(("İSİM", "SOYAD", "SİRKET"))
    for IndexSatir, kayit_numarasi in enumerate(islem.fetchall()):
        ui.tbl1.insertRow(IndexSatir)
        ui.tbl1.setItem(IndexSatir, 0, QTableWidgetItem(kayit_numarasi["AD"]))
        ui.tbl1.setItem(IndexSatir, 1, QTableWidgetItem(kayit_numarasi["SOYAD"]))
        ui.tbl1.setItem(IndexSatir, 2, QTableWidgetItem(kayit_numarasi["SIRKET"]))

ui.btn1.clicked.connect(kayit_ekle)
ui.btn2.clicked.connect(kayit_sil)
ui.btn3.clicked.connect(sirkete_gore_sirala)
kayit_listele()

# Uygulamayı çalıştır
sys.exit(uygulama.exec_())
