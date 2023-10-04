from PyQt5.QtWidgets import *
from anapencere_python import Ui_MainWindow
from anapencere_python import *
import itertools
from PyQt5.QtCore import QEvent, QTimer, QSettings
from PyQt5.QtGui import QColor,QIcon
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QTableWidgetItem, QInputDialog, QFileDialog, QApplication, QWidget, QComboBox
import sqlite3
import pandas as pd
import shutil
import sys
import json
class AnapencerePage(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.anapencereform = Ui_MainWindow()
        self.anapencereform.setupUi(self)
        self.setWindowTitle('Anapencere')
        self.anapencereform.urunlisteeklebuton.clicked.connect(self.kayit_ekle)
        self.anapencereform.secimleritemizlebuton.clicked.connect(self.sayfa_sifirla)
        self.anapencereform.pushButton_urunguncellebutton.clicked.connect(self.urun_guncelle)
        self.anapencereform.pushButton_urunsilbutton_2.clicked.connect(self.kayit_sil)
        self.anapencereform.pushButton_listeyisifirlabutton.clicked.connect(self.tablo_temizle)
        self.anapencereform.pushButton_urunkopyalabutton.clicked.connect(self.urun_kopyala)
        self.anapencereform.pushButton_listeyiexcelecevirbutton.clicked.connect(self.excel_cevir)
        self.anapencereform.listekaydet.clicked.connect(self.dosya_kaydet)
        self.anapencereform.dosyaac.clicked.connect(self.dosya_ac)
        self.anapencereform.veritabanekle_1.clicked.connect(self.veriekle1)
        self.anapencereform.veritabanekle_1.clicked.connect(self.verilistele1)
        self.anapencereform.verisil_1.clicked.connect(self.verisil1)
        self.anapencereform.veritabanekle_2.clicked.connect(self.veriekle2)
        self.anapencereform.veritabanekle_2.clicked.connect(self.verilistele2)
        self.anapencereform.verisil_2.clicked.connect(self.verisil2)
        self.anapencereform.veritabanekle_3.clicked.connect(self.veriekle3)
        self.anapencereform.veritabanekle_3.clicked.connect(self.verilistele3)
        self.anapencereform.verisil_3.clicked.connect(self.verisil3)
        self.anapencereform.veritabanekle_4.clicked.connect(self.veriekle4)
        self.anapencereform.veritabanekle_4.clicked.connect(self.verilistele4)
        self.anapencereform.verisil_4.clicked.connect(self.verisil4)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_input_sayisi)
        self.timer.start(1000)  
        self.timer2 = QTimer(self) 
        self.timer2.timeout.connect(self.update_output_sayisi)
        self.timer2.start(1000)
        self.anapencereform.sensoradres.installEventFilter(self)
        self.current_database_path = None
        self.showMaximized()
        self.setWindowIcon(QIcon('f_logo-150x150.ico'))
        self.baglanti = sqlite3.connect("urunler.db")
        self.islem = self.baglanti.cursor()
        self.baglanti.commit()
        self.islem.execute("create table if not exists urun (ref text, makineAdi text, motorGucu text, yolVerme text, sigorta text, markas text, mks text, markaMks text, surucuKod text, markaSurucu text, surucuFaz text, surucuGucu text, kontaktorKod1 text, markaKontaktor text, kontaktorKod2 text, kontaktorKod3 text, kontaktorGeri text, panoNo text, kabloCapi text, kabloUzunlugu text, mksInput text, hataInput text, ileriAdres text, geriAdres text, ileriRole text, geriRole text, digerSensor int, endSensor int, kapSensor int, motorSensor int, sensorAdres text, baglantiNoktasi text, inputSay text, outputSay text)")
        self.islem.execute("create table if not exists veri1 (motorGucu_veri text, yolVerme_veri text, markasurucu_veri text, surucufaz_veri text, surucuGucu_veri text, surucuKodu_veri text)")
        self.islem.execute("create table if not exists veri2 (motorGucu_veri text, yolVerme_veri text, markasigorta_veri text, sigorta_veri text)")
        self.islem.execute("create table if not exists veri3 (motorGucu_veri text, yolVerme_veri text, markamks_veri text, mks_veri text)")
        self.islem.execute("create table if not exists veri4 (motorGucu_veri text, yolVerme_veri text, markakontaktor_veri text, kontaktorKod1_veri text, kontaktorKod2_veri text, kontaktorKod3_veri text)")
        self.baglanti.commit()
        self.kayit_listele()
        self.kayit_listele_veri()
        self.setTabOrder(self.anapencereform.ref, self.anapencereform.makineadi)
        self.setTabOrder(self.anapencereform.makineadi, self.anapencereform.motorgucu)
        self.setTabOrder(self.anapencereform.motorgucu, self.anapencereform.yolverme)
        self.setTabOrder(self.anapencereform.yolverme, self.anapencereform.sigorta)
        self.setTabOrder(self.anapencereform.sigorta, self.anapencereform.mks)
        self.setTabOrder(self.anapencereform.mks, self.anapencereform.surucukodu)
        self.setTabOrder(self.anapencereform.surucukodu, self.anapencereform.surucugucu)
        self.setTabOrder(self.anapencereform.surucugucu, self.anapencereform.kontaktorkodu_1)
        self.setTabOrder(self.anapencereform.kontaktorkodu_1, self.anapencereform.kontaktorkodu_2)
        self.setTabOrder(self.anapencereform.kontaktorkodu_2, self.anapencereform.kontaktorkodu_3)
        self.setTabOrder(self.anapencereform.kontaktorkodu_3, self.anapencereform.kontaktorgeri)
        self.setTabOrder(self.anapencereform.kontaktorgeri, self.anapencereform.panono)
        self.setTabOrder(self.anapencereform.panono, self.anapencereform.Kablocapi)
        self.setTabOrder(self.anapencereform.Kablocapi, self.anapencereform.kablouzunlugu)
        self.setTabOrder(self.anapencereform.kablouzunlugu, self.anapencereform.MKSinput)
        self.setTabOrder(self.anapencereform.MKSinput, self.anapencereform.hatainputadres)
        self.setTabOrder(self.anapencereform.hatainputadres, self.anapencereform.ileriadres)
        self.setTabOrder(self.anapencereform.ileriadres, self.anapencereform.geriadres)
        self.setTabOrder(self.anapencereform.geriadres, self.anapencereform.ilerirole)
        self.setTabOrder(self.anapencereform.ilerirole, self.anapencereform.gerirole)
        self.setTabOrder(self.anapencereform.gerirole, self.anapencereform.digersensor)
        self.setTabOrder(self.anapencereform.digersensor, self.anapencereform.endsensor)
        self.setTabOrder(self.anapencereform.endsensor, self.anapencereform.kapsensor)
        self.setTabOrder(self.anapencereform.kapsensor, self.anapencereform.motorsensor)
        self.setTabOrder(self.anapencereform.motorsensor, self.anapencereform.sensoradres)
        self.setTabOrder(self.anapencereform.sensoradres, self.anapencereform.baglantinoktasi)
        self.setTabOrder(self.anapencereform.baglantinoktasi, self.anapencereform.inputsayisi)
        self.setTabOrder(self.anapencereform.inputsayisi, self.anapencereform.outputsayisi)
        self.setTabOrder(self.anapencereform.outputsayisi, self.anapencereform.urunlisteeklebuton)     
        self.previous_input_toplam = None
        self.previous_output_toplam = None
        self.anapencereform.otomatikdoldur.clicked.connect(self.karsilastir)  
        self.layout = QVBoxLayout()  
        self.setLayout(self.layout)  
        self.comboboxlar = [
            self.anapencereform.marka, self.anapencereform.motorgucu, self.anapencereform.yolverme,
            self.anapencereform.Marka_sigorta, self.anapencereform.Marka_mks,
            self.anapencereform.Marka_surucu, self.anapencereform.fazsurucu,
            self.anapencereform.Marka_kontaktor, self.anapencereform.Kablocapi,
            self.anapencereform.motorgucu_veri, self.anapencereform.yolverme_veri,
            self.anapencereform.Markasurucu_veri, self.anapencereform.fazsurucu_veri,
            self.anapencereform.Markasigorta_veri, self.anapencereform.Markamks_veri,
            self.anapencereform.Markakontaktor_veri
        ]
        self.load_settings()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_json)
        self.timer.start(1000)   
        self.anapencereform.Marka_surucu.currentIndexChanged.connect(self.veridoldur1)
        self.anapencereform.Marka_sigorta.currentIndexChanged.connect(self.veridoldur2)
        self.anapencereform.Marka_mks.currentIndexChanged.connect(self.veridoldur3)
        self.anapencereform.Marka_kontaktor.currentIndexChanged.connect(self.veridoldur4)
        self.anapencereform.marka.currentIndexChanged.connect(self.marka_selected)
        self.anapencereform.motorgucu.currentIndexChanged.connect(self.motorgucu_selected)
        self.anapencereform.motorgucu.setEnabled(False)
        self.anapencereform.yolverme.setEnabled(False)
        self.anapencereform.yolverme.currentIndexChanged.connect(self.veridoldur_marka1)
        self.anapencereform.yolverme.currentIndexChanged.connect(self.veridoldur_marka2)
        self.anapencereform.yolverme.currentIndexChanged.connect(self.veridoldur_marka3)
        self.anapencereform.yolverme.currentIndexChanged.connect(self.veridoldur_marka4)
    def urun_guncelle(self):
        try:
            table_urun_list = []
            for row in range(self.anapencereform.tableWidge_urunlistesi_2.rowCount()):
                row_data = [self.anapencereform.tableWidge_urunlistesi_2.item(row, col).text() for col in range(self.anapencereform.tableWidge_urunlistesi_2.columnCount())]
                table_urun_list.append(tuple(row_data))

            self.islem.execute("DELETE FROM urun")  
            for urun in table_urun_list:
                self.islem.execute("INSERT INTO urun VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", urun)
            
            self.baglanti.commit()
            self.anapencereform.statusbar.showMessage("Veriler güncellendi.", 5000)
            self.renklendir()

        except Exception as e:
            self.anapencereform.statusbar.showMessage("Bir hata oluştu: " + str(e), 5000)
    def kayit_ekle(self):
        Ref = self.anapencereform.ref.text()
        MakineAdi = self.anapencereform.makineadi.text()
        MotorGucu = self.anapencereform.motorgucu.currentText()
        Yolverme = self.anapencereform.yolverme.currentText()
        Sigorta = self.anapencereform.sigorta.text()
        MarkaSigorta = self.anapencereform.Marka_sigorta.currentText()
        Mks = self.anapencereform.mks.text()
        MarkaMks = self.anapencereform.Marka_mks.currentText()
        SurucuKod = self.anapencereform.surucukodu.text()
        MarkaSurucu = self.anapencereform.Marka_surucu.currentText()
        SurucuFaz = self.anapencereform.fazsurucu.currentText()
        SurucuGucu = self.anapencereform.surucugucu.text()
        KontaktorKod1 = self.anapencereform.kontaktorkodu_1.text()
        MarkaKontaktor = self.anapencereform.Marka_kontaktor.currentText()
        KontaktorKod2 = self.anapencereform.kontaktorkodu_2.text()
        KontaktorKod3 = self.anapencereform.kontaktorkodu_3.text()
        KontaktorGeri = self.anapencereform.kontaktorgeri.currentText()
        PanoNo = self.anapencereform.panono.currentText()
        KabloCapi = self.anapencereform.Kablocapi.currentText()
        KabloUzunlugu = self.anapencereform.kablouzunlugu.text()
        MksInput = self.anapencereform.MKSinput.text()
        HataInput = self.anapencereform.hatainputadres.text()
        IleriAdres = self.anapencereform.ileriadres.text()
        GeriAdres = self.anapencereform.geriadres.text()
        IleriRole = self.anapencereform.ilerirole.text()
        GeriRole = self.anapencereform.gerirole.text()
        DigerSensor = int(self.anapencereform.digersensor.value())
        EndSensor = int(self.anapencereform.endsensor.value())
        KapSensor = int(self.anapencereform.kapsensor.value())
        MotorSensor = int(self.anapencereform.motorsensor.value())
        SensorAdres = self.anapencereform.sensoradres.text()
        BaglantiNoktasi = self.anapencereform.baglantinoktasi.text()
        InputSay = self.anapencereform.inputsayisi.text()
        OutputSay = self.anapencereform.outputsayisi.text()

        MotorGucu = "" if MotorGucu == "Seciniz" else MotorGucu
        Yolverme = "" if Yolverme == "Seciniz" else Yolverme
        MarkaKontaktor = "" if MarkaKontaktor == "Seciniz" else MarkaKontaktor
        MarkaMks = "" if MarkaMks == "Seciniz" else MarkaMks
        MarkaSurucu = "" if MarkaSurucu == "Seciniz" else MarkaSurucu
        MarkaSigorta = "" if MarkaSigorta == "Seciniz" else MarkaSigorta
        SurucuFaz = "" if SurucuFaz == "Seciniz" else SurucuFaz
        KabloCapi = "" if KabloCapi == "Seciniz" else KabloCapi
        PanoNo = "" if PanoNo == "Seçiniz" else PanoNo
        try:
            ekle = "insert into urun (ref,makineAdi,motorGucu,yolVerme,sigorta,markas,mks,markaMks,surucuKod,markaSurucu,surucuFaz,surucuGucu,kontaktorKod1,markaKontaktor,kontaktorKod2,kontaktorKod3,kontaktorGeri,panoNo,kabloCapi,kabloUzunlugu,mksInput,hataInput,ileriAdres,geriAdres,ileriRole,geriRole,digerSensor,endSensor,kapSensor,motorSensor,sensorAdres,baglantiNoktasi,inputSay,outputSay) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
            self.islem.execute(
                ekle,
                (
                    Ref,
                    MakineAdi,
                    MotorGucu,
                    Yolverme,
                    Sigorta,
                    MarkaSigorta,
                    Mks,
                    MarkaMks,
                    SurucuKod,
                    MarkaSurucu,
                    SurucuFaz,
                    SurucuGucu,
                    KontaktorKod1,
                    MarkaKontaktor,
                    KontaktorKod2,
                    KontaktorKod3,
                    KontaktorGeri,
                    PanoNo,
                    KabloCapi,
                    KabloUzunlugu,
                    MksInput,
                    HataInput,
                    IleriAdres,
                    GeriAdres,
                    IleriRole,
                    GeriRole,
                    DigerSensor,
                    EndSensor,
                    KapSensor,
                    MotorSensor,
                    SensorAdres,
                    BaglantiNoktasi,
                    InputSay,
                    OutputSay,
                ),
            )
            self.baglanti.commit()
            self.anapencereform.statusbar.showMessage("Kayıt Ekleme İşlemi Başarılı", 10000)
        except Exception as error:
            self.anapencereform.statusbar.showMessage("Kayıt Eklenemedi. Hata Çıktı: " + str(error))
        self.renklendir()
        self.anapencereform.motorgucu.setEnabled(False)
        self.anapencereform.yolverme.setEnabled(False)
        self.kayit_listele()
    def sayfa_sifirla(self):
        try:
            reply = QMessageBox.question(self, "Sayfa Sıfırla", "Verileri silmek istediğinizden emin misiniz?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.anapencereform.ref.clear()
                self.anapencereform.makineadi.clear()
                self.anapencereform.marka.setCurrentText("Seciniz")
                self.anapencereform.motorgucu.setCurrentText("Seciniz")
                self.anapencereform.yolverme.setCurrentText("Seciniz")
                self.anapencereform.sigorta.clear()
                self.anapencereform.Marka_sigorta.setCurrentText("Seciniz")
                self.anapencereform.mks.clear()
                self.anapencereform.Marka_mks.setCurrentText("Seciniz")
                self.anapencereform.surucukodu.clear()
                self.anapencereform.fazsurucu.setCurrentText("Seciniz")
                self.anapencereform.surucugucu.clear()
                self.anapencereform.Marka_surucu.setCurrentText("Seciniz")
                self.anapencereform.Marka_kontaktor.setCurrentText("Seciniz")
                self.anapencereform.kontaktorkodu_1.clear()
                self.anapencereform.kontaktorkodu_2.clear()
                self.anapencereform.kontaktorkodu_3.clear()               
                self.anapencereform.kontaktorgeri.setCurrentText("Yok")
                self.anapencereform.panono.setCurrentText("Seçiniz")
                self.anapencereform.Kablocapi.setCurrentText("Seciniz")
                self.anapencereform.kablouzunlugu.clear()
                self.anapencereform.MKSinput.clear()
                self.anapencereform.hatainputadres.clear()
                self.anapencereform.ileriadres.clear()
                self.anapencereform.geriadres.clear()
                self.anapencereform.ilerirole.clear()
                self.anapencereform.gerirole.clear()
                self.anapencereform.digersensor.setValue(0)
                self.anapencereform.inputsayisi.clear()
                self.anapencereform.outputsayisi.clear()
                self.anapencereform.endsensor.setValue(0)
                self.anapencereform.kapsensor.setValue(0)
                self.anapencereform.motorsensor.setValue(0)
                self.anapencereform.sensoradres.clear()
                self.anapencereform.baglantinoktasi.clear()

                self.anapencereform.statusbar.showMessage("Sayfa sıfırlama işlemi başarılı.", 5000)
            else:
                self.anapencereform.statusbar.showMessage("Sayfa sıfırlama işlemi iptal edildi.", 5000)
        except Exception as e:
            self.anapencereform.statusbar.showMessage("Bir hata oluştu: " + str(e), 5000)
        self.anapencereform.motorgucu.setEnabled(False)
        self.anapencereform.yolverme.setEnabled(False)
        self.update_input_sayisi()
        self.update_output_sayisi()
        self.anapencereform.inputsayisi.setText("0")
        self.anapencereform.outputsayisi.setText("0")
    def kayit_listele(self):
        self.anapencereform.tableWidge_urunlistesi_2.clearContents()
        self.anapencereform.tableWidge_urunlistesi_2.setRowCount(0)
        self.anapencereform.tableWidge_urunlistesi_2.setHorizontalHeaderLabels(("REF", "MakineAdi","MotorGucu","Yol Verme", "Sigorta", "MarkaSigorta", "MKS", "MksMarka", "SurucuKodu", "Sur.Marka", "Sur.Faz", "SurucuGucu", "kontaktorKod1", "K.Marka", "kontaktorKod2", "kontaktorKod3",
                            "PanoNo", "kabloCapi", "kabl Uzunlugu", "kontaktorGeri",
                            "MKSInput", "HataInput", "IleriAdres",
                            "GeriAdres", "IleriRole", "GeriRole", "DigerSensor", "EndSensor", "KapSensor",
                            "MotorSensor", "SensorAdres", "BağlantıNoktası", "InputSay", "OutputSay"))
        sorgu = "select * from urun"
        self.islem.execute(sorgu)

        for indexSatir, kayitNumarasi in enumerate(self.islem):
            self.anapencereform.tableWidge_urunlistesi_2.insertRow(indexSatir)
            for indexSutun, kayitSutun in enumerate(kayitNumarasi):
                self.anapencereform.tableWidge_urunlistesi_2.setItem(indexSatir, indexSutun, QTableWidgetItem(str(kayitSutun)))
        self.renklendir()
    def kayit_sil(self):
        sil_mesaj = QMessageBox.question(self, "Silme Onayı", "Silmek İstediğinizden Emin Misiniz?", QMessageBox.Yes | QMessageBox.No)

        if sil_mesaj == QMessageBox.Yes:
            secilen_kayit = self.anapencereform.tableWidge_urunlistesi_2.selectedItems()
            if not secilen_kayit:
                self.anapencereform.statusbar.showMessage("Silinecek bir kayıt seçilmedi")
                return
            secilen_satir = secilen_kayit[0].row()

            try:
                self.islem.execute("DELETE FROM urun WHERE rowid = ?", (secilen_satir + 1,))
                self.baglanti.commit()

                self.guncelle_rowids()
                self.anapencereform.statusbar.showMessage("Kayıt Başarıyla Silindi")
                self.kayit_listele()
            except Exception as error:
                self.anapencereform.statusbar.showMessage("Kayıt Silinirken Hata Çıktı: " + str(error))
        else:
            self.anapencereform.statusbar.showMessage("Silme İşlemi İptal Edildi")
    def guncelle_rowids(self):
        self.islem.execute("SELECT rowid FROM urun")
        rowids = [kayit[0] for kayit in self.islem.fetchall()]
        new_rowids = itertools.count(start=1)

        for current_rowid, new_rowid in zip(rowids, new_rowids):
            if current_rowid != new_rowid:
                self.islem.execute("UPDATE urun SET rowid = ? WHERE rowid = ?", (new_rowid, current_rowid))

        self.baglanti.commit()
        self.anapencereform.statusbar.showMessage("Veritabanı güncellendi ve rowid'ler yeniden numaralandırıldı")
    def marka_selected(self):
        self.anapencereform.motorgucu.setEnabled(True)
    def motorgucu_selected(self):
        self.anapencereform.yolverme.setEnabled(True)
    def veridoldur_marka1(self):
            try:
                yolVerme = self.anapencereform.yolverme.currentText()
                motorGucu = self.anapencereform.motorgucu.currentText()
                marka = self.anapencereform.marka.currentText()
                if marka == "" or yolVerme == "" or motorGucu == "":
                    self.anapencereform.statusbar.showMessage("Lütfen geçerli bir marka, yol verme ve motor gücü seçin.")
                    return
                baglanti_veriler = sqlite3.connect("urunler.db")
                islem_veriler = baglanti_veriler.cursor()

                sorgu_veriler = "SELECT * FROM veri1 WHERE yolVerme_veri = ? AND motorGucu_veri = ? AND markasurucu_veri = ?"
                islem_veriler.execute(sorgu_veriler, (yolVerme, motorGucu, marka))
                veri_satiri = islem_veriler.fetchone()

                if not veri_satiri:
                    self.anapencereform.statusbar.showMessage("Girilen verilere uygun bir satır bulunamadı.")
                    baglanti_veriler.close()
                    return
                else:
                    self.anapencereform.Marka_surucu.setCurrentText(veri_satiri[2])
                    self.anapencereform.fazsurucu.setCurrentText(veri_satiri[3])
                    self.anapencereform.surucukodu.setText(veri_satiri[4])
                    self.anapencereform.surucugucu.setText(veri_satiri[5])
                    baglanti_veriler.close()
                    self.anapencereform.statusbar.showMessage("Veriler başarıyla dolduruldu.", 5000)
            except Exception as e:
                self.anapencereform.statusbar.showMessage("Otomatik doldurma işlemi sırasında bir hata oluştu: " + str(e), 5000)
    def veridoldur_marka2(self):
            try:
                marka = self.anapencereform.marka.currentText()
                yolVerme = self.anapencereform.yolverme.currentText()
                motorGucu = self.anapencereform.motorgucu.currentText()
                if marka == "" or yolVerme == "" or motorGucu == "":
                    self.anapencereform.statusbar.showMessage("Lütfen geçerli bir marka, yol verme ve motor gücü seçin.")
                    return
                baglanti_veriler = sqlite3.connect("urunler.db")
                islem_veriler = baglanti_veriler.cursor()

                sorgu_veriler = "SELECT * FROM veri2 WHERE yolVerme_veri = ? AND motorGucu_veri = ? AND markasigorta_veri = ?"
                islem_veriler.execute(sorgu_veriler, (yolVerme, motorGucu, marka))
                veri_satiri = islem_veriler.fetchone()

                if not veri_satiri:
                    self.anapencereform.statusbar.showMessage("Girilen verilere uygun bir satır bulunamadı.")
                    baglanti_veriler.close()
                    return
                else:
                    self.anapencereform.Marka_sigorta.setCurrentText(veri_satiri[2])
                    self.anapencereform.sigorta.setText(veri_satiri[3])
                    baglanti_veriler.close()
                    self.anapencereform.statusbar.showMessage("Veriler başarıyla dolduruldu.", 5000)
            except Exception as e:
                self.anapencereform.statusbar.showMessage("Otomatik doldurma işlemi sırasında bir hata oluştu: " + str(e), 5000)
    def veridoldur_marka3(self):
            try:
                marka = self.anapencereform.marka.currentText()
                yolVerme = self.anapencereform.yolverme.currentText()
                motorGucu = self.anapencereform.motorgucu.currentText()

                if marka == "" or yolVerme == "" or motorGucu == "":
                    self.anapencereform.statusbar.showMessage("Lütfen geçerli bir marka, yol verme ve motor gücü seçin.")
                    return

                baglanti_veriler = sqlite3.connect("urunler.db")
                islem_veriler = baglanti_veriler.cursor()

                sorgu_veriler = "SELECT * FROM veri3 WHERE yolVerme_veri = ? AND motorGucu_veri = ? AND markamks_veri = ?"
                islem_veriler.execute(sorgu_veriler, (yolVerme, motorGucu, marka))
                veri_satiri = islem_veriler.fetchone()

                if not veri_satiri:
                    self.anapencereform.statusbar.showMessage("Girilen verilere uygun bir satır bulunamadı.")
                    baglanti_veriler.close()
                    return
                else:
                    self.anapencereform.Marka_mks.setCurrentText(veri_satiri[2])
                    self.anapencereform.mks.setText(veri_satiri[3])
                    baglanti_veriler.close()
                    self.anapencereform.statusbar.showMessage("Veriler başarıyla dolduruldu.", 5000)

            except Exception as e:
                self.anapencereform.statusbar.showMessage("Otomatik doldurma işlemi sırasında bir hata oluştu: " + str(e), 5000)
    def veridoldur_marka4(self):
            try:
                marka = self.anapencereform.marka.currentText()
                yolVerme = self.anapencereform.yolverme.currentText()
                motorGucu = self.anapencereform.motorgucu.currentText()

                if marka == "" or yolVerme == "" or motorGucu == "":
                    self.anapencereform.statusbar.showMessage("Lütfen geçerli bir marka, yol verme ve motor gücü seçin.")
                    return

                baglanti_veriler = sqlite3.connect("urunler.db")
                islem_veriler = baglanti_veriler.cursor()

                sorgu_veriler = "SELECT * FROM veri4 WHERE yolVerme_veri = ? AND motorGucu_veri = ? AND markakontaktor_veri = ?"
                islem_veriler.execute(sorgu_veriler, (yolVerme, motorGucu, marka))
                veri_satiri = islem_veriler.fetchone()

                if not veri_satiri:
                    self.anapencereform.statusbar.showMessage("Girilen verilere uygun bir satır bulunamadı.")
                    baglanti_veriler.close()
                    return
                else:
                    self.anapencereform.Marka_kontaktor.setCurrentText(veri_satiri[2])
                    self.anapencereform.kontaktorkodu_1.setText(veri_satiri[3])
                    self.anapencereform.kontaktorkodu_2.setText(veri_satiri[4])
                    self.anapencereform.kontaktorkodu_3.setText(veri_satiri[5])
                    baglanti_veriler.close()
                    self.anapencereform.statusbar.showMessage("Veriler başarıyla dolduruldu.", 5000)

            except Exception as e:
                self.anapencereform.statusbar.showMessage("Otomatik doldurma işlemi sırasında bir hata oluştu: " + str(e), 5000)
    def veridoldur1(self):
        try:
            yolVerme = self.anapencereform.yolverme.currentText()
            motorGucu = self.anapencereform.motorgucu.currentText()
            marka = self.anapencereform.Marka_surucu.currentText()
            faz = self.anapencereform.fazsurucu.currentText()
            if marka == "" or yolVerme == "" or motorGucu == "" or faz == "":
                self.anapencereform.statusbar.showMessage("Lütfen geçerli bir marka, faz, yol verme ve motor gücü seçin.")
                return
            baglanti_veriler = sqlite3.connect("urunler.db")
            islem_veriler = baglanti_veriler.cursor()

            sorgu_veriler = "SELECT * FROM veri1 WHERE yolVerme_veri = ? AND motorGucu_veri = ? AND markasurucu_veri = ? AND surucufaz_veri = ?"
            islem_veriler.execute(sorgu_veriler, (yolVerme, motorGucu, marka, faz))
            veri_satiri = islem_veriler.fetchone()

            if not veri_satiri:
                self.anapencereform.statusbar.showMessage("Girilen verilere uygun bir satır bulunamadı.")
                baglanti_veriler.close()
                return
            else:
                self.anapencereform.surucukodu.setText(veri_satiri[5])
                self.anapencereform.surucugucu.setText(veri_satiri[4])
                baglanti_veriler.close()
                self.anapencereform.statusbar.showMessage("Veriler başarıyla dolduruldu.", 5000)


        except Exception as e:
            self.anapencereform.statusbar.showMessage("Otomatik doldurma işlemi sırasında bir hata oluştu: " + str(e), 5000)
    def veridoldur2(self):

        try:
            marka = self.anapencereform.Marka_sigorta.currentText()
            yolVerme = self.anapencereform.yolverme.currentText()
            motorGucu = self.anapencereform.motorgucu.currentText()
            if marka == "" or yolVerme == "" or motorGucu == "":
                self.anapencereform.statusbar.showMessage("Lütfen geçerli bir marka, yol verme ve motor gücü seçin.")
                return
            baglanti_veriler = sqlite3.connect("urunler.db")
            islem_veriler = baglanti_veriler.cursor()

            sorgu_veriler = "SELECT * FROM veri2 WHERE yolVerme_veri = ? AND motorGucu_veri = ? AND markasigorta_veri = ?"
            islem_veriler.execute(sorgu_veriler, (yolVerme, motorGucu, marka))
            veri_satiri = islem_veriler.fetchone()

            if not veri_satiri:
                self.anapencereform.statusbar.showMessage("Girilen verilere uygun bir satır bulunamadı.")
                baglanti_veriler.close()
                return
            else:
                self.anapencereform.sigorta.setText(veri_satiri[3])
                self.anapencereform.statusbar.showMessage("Veriler başarıyla dolduruldu.", 5000)
                self.zamanlayici7.stop()

        except Exception as e:
            self.anapencereform.statusbar.showMessage("Otomatik doldurma işlemi sırasında bir hata oluştu: " + str(e), 5000)
    def veridoldur3(self):

        try:
            marka = self.anapencereform.Marka_mks.currentText()
            yolVerme = self.anapencereform.yolverme.currentText()
            motorGucu = self.anapencereform.motorgucu.currentText()

            if marka == "" or yolVerme == "" or motorGucu == "":
                self.anapencereform.statusbar.showMessage("Lütfen geçerli bir marka, yol verme ve motor gücü seçin.")
                return

            baglanti_veriler = sqlite3.connect("urunler.db")
            islem_veriler = baglanti_veriler.cursor()

            sorgu_veriler = "SELECT * FROM veri3 WHERE yolVerme_veri = ? AND motorGucu_veri = ? AND markamks_veri = ?"
            islem_veriler.execute(sorgu_veriler, (yolVerme, motorGucu, marka))
            veri_satiri = islem_veriler.fetchone()

            if not veri_satiri:
                self.anapencereform.statusbar.showMessage("Girilen verilere uygun bir satır bulunamadı.")
                baglanti_veriler.close()
                return
            else:
                self.anapencereform.mks.setText(veri_satiri[3])

                baglanti_veriler.close()
                self.anapencereform.statusbar.showMessage("Veriler başarıyla dolduruldu.", 5000)


        except Exception as e:
            self.anapencereform.statusbar.showMessage("Otomatik doldurma işlemi sırasında bir hata oluştu: " + str(e), 5000)
    def veridoldur4(self):

        try:
            marka = self.anapencereform.Marka_kontaktor.currentText()
            yolVerme = self.anapencereform.yolverme.currentText()
            motorGucu = self.anapencereform.motorgucu.currentText()

            if marka == "" or yolVerme == "" or motorGucu == "":
                self.anapencereform.statusbar.showMessage("Lütfen geçerli bir marka, yol verme ve motor gücü seçin.")
                return

            baglanti_veriler = sqlite3.connect("urunler.db")
            islem_veriler = baglanti_veriler.cursor()

            sorgu_veriler = "SELECT * FROM veri4 WHERE yolVerme_veri = ? AND motorGucu_veri = ? AND markakontaktor_veri = ?"
            islem_veriler.execute(sorgu_veriler, (yolVerme, motorGucu, marka))
            veri_satiri = islem_veriler.fetchone()

            if not veri_satiri:
                self.anapencereform.statusbar.showMessage("Girilen verilere uygun bir satır bulunamadı.")
                baglanti_veriler.close()
                return
            else:
                self.anapencereform.kontaktorkodu_1.setText(veri_satiri[3])
                self.anapencereform.kontaktorkodu_2.setText(veri_satiri[4])
                self.anapencereform.kontaktorkodu_3.setText(veri_satiri[5])

                baglanti_veriler.close()
                self.anapencereform.statusbar.showMessage("Veriler başarıyla dolduruldu.", 5000)

        except Exception as e:
            self.anapencereform.statusbar.showMessage("Otomatik doldurma işlemi sırasında bir hata oluştu: " + str(e), 5000)
    def load_settings(self):
        try:
            with open('data.json', 'r') as json_file:
                data = json.load(json_file)

            for index, combo in enumerate(self.comboboxlar):
                cList = data.get(f'veri{index+1}', [])
                combo.addItems(cList)
                combo.setCurrentIndex(0)

        except FileNotFoundError:
            pass
    def update_json(self):
        try:
            with open('data.json', 'r') as json_file:
                data = json.load(json_file)
        except FileNotFoundError:
            data = {f'veri{i+1}': [] for i in range(len(self.comboboxlar))}

        for index, combo in enumerate(self.comboboxlar):
            data[f'veri{index+1}'] = [combo.itemText(i) for i in range(combo.count())]

        with open('data.json', 'w') as json_file:
            json.dump(data, json_file)
    def closeEvent(self, event):
        self.update_json()  # JSON dosyasını güncelle
        for index, combo in enumerate(self.comboboxlar):
            data = [combo.itemText(i) for i in range(combo.count())]
            settings = QSettings(QSettings.IniFormat, QSettings.UserScope, 'MyCompany', 'MyApp')
            settings.setValue(f'combo list{index}', data)
    def tablo_temizle(self):
        onay = QMessageBox.question(self, "Tabloyu Temizle", "Tüm kayıtları silmek istediğinizden emin misiniz?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if onay == QMessageBox.Yes:
            self.anapencereform.tableWidge_urunlistesi_2.clearContents()
            self.anapencereform.tableWidge_urunlistesi_2.setRowCount(0)
            sorgu = "delete from urun"
            try:
                self.islem.execute(sorgu)
                self.baglanti.commit()
                self.anapencereform.statusbar.showMessage("Tüm Kayıtlar Başarıyla Silindi")
            except Exception as error:
                self.anapencereform.statusbar.showMessage("Kayıtlar Silinirken Hata Çıktı === " + str(error))
        else:
            self.anapencereform.statusbar.showMessage("Tablo temizleme işlemi iptal edildi")
    def urun_kopyala(self):
        secilen_kayit = self.anapencereform.tableWidge_urunlistesi_2.selectedItems()
        if secilen_kayit:
            secilen_satir = secilen_kayit[0].row()
            veriler = []
            for sutun in range(self.anapencereform.tableWidge_urunlistesi_2.columnCount()):
                veriler.append(self.anapencereform.tableWidge_urunlistesi_2.item(secilen_satir, sutun).text())

            kopyalama_sayisi, ok = QInputDialog.getInt(self, "Kopyalama Sayısı", "Kaç kere kopyalamak istersiniz?", 1, 1)
            if ok:
                for _ in range(kopyalama_sayisi):
                    try:
                        self.islem.execute("INSERT INTO urun VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", tuple(veriler))
                        self.baglanti.commit()
                    except Exception as error:
                        self.anapencereform.statusbar.showMessage("Kayıt Kopyalanırken Hata Çıktı === " + str(error))
                self.anapencereform.statusbar.showMessage(f"{kopyalama_sayisi} adet kayıt başarıyla kopyalandı ve veritabanına eklendi.")
                self.kayit_listele()
        else:
            self.anapencereform.statusbar.showMessage("Kopyalanacak bir kayıt seçilmedi")
        self.renklendir()
    def excel_cevir(self):
        try:
            if self.current_database_path:
                sorgu = "SELECT * FROM urun"
                self.islem.execute(sorgu)
                veriler = self.islem.fetchall()
                columns = [description[0] for description in self.islem.description]
                df = pd.DataFrame(veriler, columns=columns)
                excel_dosya_adi, _ = QFileDialog.getSaveFileName(self, "Excel Dosyasına Kaydet", "", "Excel Dosyası (*.xlsx);;All Files (*)")

                if excel_dosya_adi:
                    df.to_excel(excel_dosya_adi, index=False)
                    self.anapencereform.statusbar.showMessage(f"Veriler başarıyla {excel_dosya_adi} dosyasına kaydedildi.")
            else:
                dosya_adi, _ = QFileDialog.getSaveFileName(self, "Excel Dosyası Kaydet", "", "Excel Dosyası (*.xlsx);;All Files (*)")
                if dosya_adi:
                    try:
                        sorgu = "SELECT * FROM urun"
                        df = pd.read_sql_query(sorgu, self.baglanti)
                        df.to_excel(dosya_adi, index=False)
                        self.anapencereform.statusbar.showMessage(f"Veriler başarıyla Excel dosyasına kaydedildi: {dosya_adi}", 10000)
                    except Exception as error:
                        self.anapencereform.statusbar.showMessage("Veriler Excel dosyasına kaydedilemedi. Hata Çıktı === " + str(error))
        except Exception as error:
            self.anapencereform.statusbar.showMessage(f"Veriler yazılırken hata oluştu: {error}")
    def karsilastir(self):
        limit = "SELECT * FROM urun ORDER BY rowid DESC LIMIT 10"
        self.islem.execute(limit)
        last_10_records = self.islem.fetchall()
        ref = self.anapencereform.ref.text()
        makine_adi = self.anapencereform.makineadi.text()
        for record in last_10_records:
            if record[0] == ref and record[1] == makine_adi:
                self.anapencereform.motorgucu.setCurrentText(record[2])
                self.anapencereform.yolverme.setCurrentText(record[3])
                self.anapencereform.sigorta.setText(record[4])
                self.anapencereform.Marka_sigorta.setCurrentText(record[5])
                self.anapencereform.mks.setText(record[6])
                self.anapencereform.Marka_mks.setCurrentText(record[7])
                self.anapencereform.surucukodu.setText(record[8])
                self.anapencereform.Marka_surucu.setCurrentText(record[9])
                self.anapencereform.fazsurucu.setCurrentText(record[10])
                self.anapencereform.surucugucu.setText(record[11])
                self.anapencereform.kontaktorkodu_1.setText(record[12])
                self.anapencereform.Marka_kontaktor.setCurrentText(record[13])
                self.anapencereform.kontaktorkodu_2.setText(record[14])
                self.anapencereform.kontaktorkodu_3.setText(record[15])
                self.anapencereform.kontaktorgeri.setCurrentText(record[16])
                self.anapencereform.panono.setCurrentText(record[17])
                self.anapencereform.Kablocapi.setCurrentText(record[18])
                self.anapencereform.kablouzunlugu.setText(record[19])
                self.anapencereform.MKSinput.setText(record[20])
                self.anapencereform.hatainputadres.setText(record[21])
                self.anapencereform.ileriadres.setText(record[22])
                self.anapencereform.geriadres.setText(record[23])
                self.anapencereform.ilerirole.setText(record[24])
                self.anapencereform.gerirole.setText(record[25])
                self.anapencereform.digersensor.setValue(record[26])
                self.anapencereform.endsensor.setValue(record[27])
                self.anapencereform.kapsensor.setValue(record[28])
                self.anapencereform.motorsensor.setValue(record[29])
                self.anapencereform.sensoradres.setText(record[30])
                self.anapencereform.baglantinoktasi.setText(record[31])
                self.anapencereform.inputsayisi.setText(record[32])
                self.anapencereform.outputsayisi.setText(record[33])
                break  
        else:
            self.anapencereform.statusbar.showMessage("Eşleşme bulunamadı.")
    def sensor_adres_sorgula(self):
        kapsensor_sayisi = int(self.anapencereform.kapsensor.value())
        motorsensor_sayisi = int(self.anapencereform.motorsensor.value())
        endsensor_sayisi = int(self.anapencereform.endsensor.value())

        adresler = []
        for i in range(1, endsensor_sayisi + 1):
            adres, ok = QInputDialog.getText(self, f"{i}. End Sensör Adresi", f"{i}. end sensör adresini giriniz:")
            if ok and adres.strip():
                adresler.append(adres.strip())
            else:
                QMessageBox.warning(self, "Uyarı", "Geçerli bir sensör adresi girmediniz. Lütfen tekrar deneyin.")
                return

        for i in range(1, kapsensor_sayisi + 1):
            adres, ok = QInputDialog.getText(self, f"{i}. Kap Sensör Adresi", f"{i}. kap sensör adresini giriniz:")
            if ok and adres.strip():
                adresler.append(adres.strip())
            else:
                QMessageBox.warning(self, "Uyarı", "Geçerli bir sensör adresi girmediniz. Lütfen tekrar deneyin.")
                return

        for i in range(1, motorsensor_sayisi + 1):
            adres, ok = QInputDialog.getText(self, f"{i}. Motor Sensör Adresi", f"{i}. motor sensör adresini giriniz:")
            if ok and adres.strip():
                adresler.append(adres.strip())
            else:
                QMessageBox.warning(self, "Uyarı", "Geçerli bir sensör adresi girmediniz. Lütfen tekrar deneyin.")
                return

        self.anapencereform.sensoradres.setText(" / ".join(adresler))
    def eventFilter(self, obj, event):
        if obj == self.anapencereform.sensoradres and event.type() == QEvent.MouseButtonPress:
            self.sensor_adres_sorgula()
            return True
        return super().eventFilter(obj, event)
    def renklendir(self):
        deger = "Diğer"
        for satir in range(self.anapencereform.tableWidge_urunlistesi_2.rowCount()):
            for sutun in range(self.anapencereform.tableWidge_urunlistesi_2.columnCount()):
                hucr_item = self.anapencereform.tableWidge_urunlistesi_2.item(satir, sutun)
                if hucr_item and hucr_item.text() == deger:
                    hucr_item.setForeground(QColor("red"))
                    hucr_item.setBackground(QColor("yellow"))
    def dosya_ac(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        dosya_adi, _ = QFileDialog.getOpenFileName(self, "Dosya Aç", "", "SQLite Veritabanı (*.db);;All Files (*)", options=options)
        if dosya_adi:
            try:
                self.baglanti.close()
                self.current_database_path = dosya_adi
                self.baglanti = sqlite3.connect(dosya_adi)
                self.islem = self.baglanti.cursor()
                self.baglanti.commit()
                self.kayit_listele()
                self.anapencereform.statusbar.showMessage(f"Dosya başarıyla açıldı: {dosya_adi}", 10000)
            except Exception as error:
                self.anapencereform.statusbar.showMessage("Dosya açılamadı Hata Çıktı === " + str(error))
    def dosya_kaydet(self):
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            dosya_adi, _ = QFileDialog.getSaveFileName(self, "Dosya Kaydet", ".db", "SQLite Veritabanı (*.db);;All Files (*)", options=options)
            if dosya_adi:
                try:
                    shutil.copyfile("urunler.db", dosya_adi)
                    self.anapencereform.statusbar.showMessage(f"Dosya başarıyla kaydedildi: {dosya_adi}", 10000)
                except Exception as error:
                    self.anapencereform.statusbar.showMessage("Dosya kaydedilemedi Hata Çıktı === " + str(error))
    def update_input_sayisi(self):
        sigorta = self.anapencereform.sigorta.text()
        mks = self.anapencereform.mks.text()
        diger_sensor = int(self.anapencereform.digersensor.value())
        end_sensor = int(self.anapencereform.endsensor.value())
        kap_sensor = int(self.anapencereform.kapsensor.value())
        motor_sensor = int(self.anapencereform.motorsensor.value())
        input_toplam = 0
        if sigorta:
            input_toplam += 1
        if mks:
            input_toplam += 1
        if diger_sensor:
            input_toplam += 1
        if end_sensor:
            input_toplam += 1
        if kap_sensor:
            input_toplam += 1
        if motor_sensor:
            input_toplam += 1
        if self.previous_input_toplam is None or input_toplam != self.previous_input_toplam:
            self.anapencereform.inputsayisi.setText(str(input_toplam))
            self.previous_input_toplam = input_toplam
    def update_output_sayisi(self):
        ileri_role = self.anapencereform.ilerirole.text()
        geri_role = self.anapencereform.gerirole.text()
        output_toplam = 0
        if ileri_role:
            output_toplam += 1
        if geri_role:
            output_toplam += 1
        if self.previous_output_toplam is None or output_toplam != self.previous_output_toplam :
            self.anapencereform.outputsayisi.setText(str(output_toplam))
            self.previous_output_toplam = output_toplam
    def veriekle1(self):
        MotorGucu_veri = self.anapencereform.motorgucu_veri.currentText()
        Yolverme_veri = self.anapencereform.yolverme_veri.currentText()
        MarkaSurucu_veri = self.anapencereform.Markasurucu_veri.currentText()
        SurucuFaz_veri = self.anapencereform.fazsurucu_veri.currentText()
        SurucuGucu_veri = self.anapencereform.surucugucu_veri.text()
        SurucuKod_veri = self.anapencereform.surucukodu_veri.text()

        if self.veri_var_mi1(MotorGucu_veri, Yolverme_veri, MarkaSurucu_veri, SurucuFaz_veri):
            QMessageBox.warning(self, "Uyarı", "Girilen marka, motor gücü ve yol verme kombinasyonuna sahip bir veri zaten mevcut!",
                                QMessageBox.Ok)
        else:
            try:
                kaydet = "insert into veri1(motorGucu_veri,yolVerme_veri,markasurucu_veri,surucufaz_veri,surucuGucu_veri,surucuKodu_veri) values (?,?,?,?,?,?)"
                self.islem.execute(kaydet,(MotorGucu_veri,Yolverme_veri,MarkaSurucu_veri,SurucuFaz_veri,SurucuGucu_veri,SurucuKod_veri))
                self.baglanti.commit()
                self.anapencereform.statusbar.showMessage("Kayıt Ekleme İşlemi Başarılı", 10000)
            except Exception as error:
                self.anapencereform.statusbar.showMessage("Kayıt Eklenemedi Hata Çıktı === " + str(error))


        self.anapencereform.Markasurucu_veri.setCurrentIndex(0)
        self.anapencereform.fazsurucu_veri.setCurrentIndex(0)
        self.anapencereform.surucugucu_veri.clear()
        self.anapencereform.surucukodu_veri.clear() 
    def veri_var_mi1(self, motor_gucu, yol_verme, marka_surucu, surucu_faz):
        sorgu = "SELECT COUNT(*) FROM veri1 WHERE motorgucu_veri = ? AND yolverme_veri = ? AND markasurucu_veri = ? AND surucufaz_veri = ?"
        self.islem.execute(sorgu, (motor_gucu, yol_verme, marka_surucu, surucu_faz))
        kayit_sayisi = self.islem.fetchone()[0]
        return kayit_sayisi > 0 
    def veriekle2(self):
        MotorGucu_veri = self.anapencereform.motorgucu_veri.currentText()
        Yolverme_veri = self.anapencereform.yolverme_veri.currentText()
        MarkaSigorta_veri = self.anapencereform.Markasigorta_veri.currentText()
        Sigorta_veri = self.anapencereform.sigorta_veri.text()

        if self.veri_var_mi2(MotorGucu_veri, Yolverme_veri, MarkaSigorta_veri):
            QMessageBox.warning(self, "Uyarı", "Girilen marka, motor gücü ve yol verme kombinasyonuna sahip bir veri zaten mevcut!",
                                QMessageBox.Ok)
        else:
            try:
                kaydet = "insert into veri2(motorGucu_veri,yolVerme_veri,markasigorta_veri,sigorta_veri)values (?,?,?,?)"
                self.islem.execute(kaydet,(MotorGucu_veri,Yolverme_veri,MarkaSigorta_veri,Sigorta_veri))
                self.baglanti.commit()
                self.anapencereform.statusbar.showMessage("Kayıt Ekleme İşlemi Başarılı", 10000)
            except Exception as error:
                self.anapencereform.statusbar.showMessage("Kayıt Eklenemedi Hata Çıktı === " + str(error))

        self.anapencereform.Markasigorta_veri.setCurrentIndex(0)
        self.anapencereform.sigorta_veri.clear()
    def veri_var_mi2(self, motor_gucu, yol_verme, marka_sigorta):
        sorgu = "SELECT COUNT(*) FROM veri2 WHERE motorgucu_veri = ? AND yolverme_veri = ? AND markasigorta_veri = ?"
        self.islem.execute(sorgu, (motor_gucu, yol_verme, marka_sigorta))
        kayit_sayisi = self.islem.fetchone()[0]
        return kayit_sayisi > 0
    def veriekle3(self):
        MotorGucu_veri = self.anapencereform.motorgucu_veri.currentText()
        Yolverme_veri = self.anapencereform.yolverme_veri.currentText()
        MarkaMks_veri = self.anapencereform.Markamks_veri.currentText()
        Mks_veri = self.anapencereform.mks_veri.text()

        if self.veri_var_mi3(MotorGucu_veri, Yolverme_veri, MarkaMks_veri):
            QMessageBox.warning(self, "Uyarı", "Girilen marka, motor gücü ve yol verme kombinasyonuna sahip bir veri zaten mevcut!",
                                QMessageBox.Ok)
        else:
            try:
                kaydet = "insert into veri3(motorGucu_veri,yolVerme_veri,markamks_veri,mks_veri) values (?,?,?,?)"
                self.islem.execute(kaydet,(MotorGucu_veri,Yolverme_veri,MarkaMks_veri,Mks_veri))
                self.baglanti.commit()
                self.anapencereform.statusbar.showMessage("Kayıt Ekleme İşlemi Başarılı", 10000)
            except Exception as error:
                self.anapencereform.statusbar.showMessage("Kayıt Eklenemedi Hata Çıktı === " + str(error))

        self.anapencereform.Markamks_veri.setCurrentIndex(0)
        self.anapencereform.mks_veri.clear()
    def veri_var_mi3(self, motor_gucu, yol_verme, marka_mks):
        sorgu = "SELECT COUNT(*) FROM veri3 WHERE motorGucu_veri = ? AND yolVerme_veri = ? AND markamks_veri = ?"
        self.islem.execute(sorgu, (motor_gucu, yol_verme, marka_mks))
        kayit_sayisi = self.islem.fetchone()[0]
        return kayit_sayisi > 0
    def veriekle4(self):
        MotorGucu_veri = self.anapencereform.motorgucu_veri.currentText()
        Yolverme_veri = self.anapencereform.yolverme_veri.currentText()
        MarkaKontaktor_veri = self.anapencereform.Markakontaktor_veri.currentText()
        KontaktorKod1_veri = self.anapencereform.kontaktor1_veri.text()
        KontaktorKod2_veri = self.anapencereform.kontaktor2_veri.text()
        KontaktorKod3_veri = self.anapencereform.kontaktor3_veri.text()
        
        if self.veri_var_mi4(MotorGucu_veri, Yolverme_veri,MarkaKontaktor_veri):
            QMessageBox.warning(self, "Uyarı", "Girilen marka, motor gücü ve yol verme kombinasyonuna sahip bir veri zaten mevcut!",
                                QMessageBox.Ok)
        else:
            try:
                kaydet = "insert into veri4(motorgucu_veri,yolverme_veri,markakontaktor_veri,kontaktorKod1_veri,kontaktorKod2_veri,kontaktorKod3_veri) values (?,?,?,?,?,?)"
                self.islem.execute(kaydet,(MotorGucu_veri,Yolverme_veri,MarkaKontaktor_veri,KontaktorKod1_veri,KontaktorKod2_veri,KontaktorKod3_veri))
                self.baglanti.commit()
                self.anapencereform.statusbar.showMessage("Kayıt Ekleme İşlemi Başarılı", 10000)
            except Exception as error:
                self.anapencereform.statusbar.showMessage("Kayıt Eklenemedi Hata Çıktı === " + str(error))


        self.anapencereform.Markakontaktor_veri.setCurrentIndex(0)
        self.anapencereform.kontaktor1_veri.clear()
        self.anapencereform.kontaktor2_veri.clear()
        self.anapencereform.kontaktor3_veri.clear()   
    def veri_var_mi4(self, motor_gucu, yol_verme, marka_kontaktor):
        sorgu = "SELECT COUNT(*) FROM veri4 WHERE motorgucu_veri = ? AND yolverme_veri = ? AND markakontaktor_veri = ?"
        self.islem.execute(sorgu, (motor_gucu, yol_verme, marka_kontaktor))
        kayit_sayisi = self.islem.fetchone()[0]
        return kayit_sayisi > 0
    def verilistele1(self):
        self.anapencereform.tableWidge_veritabani_1.clearContents()
        self.anapencereform.tableWidge_veritabani_1.setRowCount(0)
        self.anapencereform.tableWidge_veritabani_1.setHorizontalHeaderLabels(("Motor Gücü", "Yol Verme", "Marka Src", "Faz Src", "Sürücü Gücü", "Sürücü Kodu"))

        sorgu = "SELECT * FROM veri1"
        self.islem.execute(sorgu)

        for indexSatir, kayitNumarasi in enumerate(self.islem):
            self.anapencereform.tableWidge_veritabani_1.insertRow(indexSatir)
            for indexSutun, kayitSutun in enumerate(kayitNumarasi):
                self.anapencereform.tableWidge_veritabani_1.setItem(indexSatir, indexSutun, QTableWidgetItem(str(kayitSutun)))
    def verilistele2(self):
        self.anapencereform.tableWidge_veritabani_2.clearContents()
        self.anapencereform.tableWidge_veritabani_2.setRowCount(0)
        self.anapencereform.tableWidge_veritabani_2.setHorizontalHeaderLabels(("Motor Gücü", "Yol Verme", "Marka Sgrt", "Sigorta"))

        sorgu = "SELECT * FROM veri2"
        self.islem.execute(sorgu)
        for indexSatir, kayitNumarasi in enumerate(self.islem):
            self.anapencereform.tableWidge_veritabani_2.insertRow(indexSatir)
            for indexSutun, kayitSutun in enumerate(kayitNumarasi):
                self.anapencereform.tableWidge_veritabani_2.setItem(indexSatir, indexSutun, QTableWidgetItem(str(kayitSutun)))
    def verilistele3(self):
        self.anapencereform.tableWidge_veritabani_3.clearContents()
        self.anapencereform.tableWidge_veritabani_3.setRowCount(0)
        self.anapencereform.tableWidge_veritabani_3.setHorizontalHeaderLabels(("Motor Gücü", "Yol Verme", "Marka MKŞ", "MKŞ"))

        sorgu = "SELECT * FROM veri3"
        self.islem.execute(sorgu)
        for indexSatir, kayitNumarasi in enumerate(self.islem):
            self.anapencereform.tableWidge_veritabani_3.insertRow(indexSatir)
            for indexSutun, kayitSutun in enumerate(kayitNumarasi):
                self.anapencereform.tableWidge_veritabani_3.setItem(indexSatir, indexSutun, QTableWidgetItem(str(kayitSutun)))
    def verilistele4(self):
        self.anapencereform.tableWidge_veritabani_4.clearContents()
        self.anapencereform.tableWidge_veritabani_4.setRowCount(0)
        self.anapencereform.tableWidge_veritabani_4.setHorizontalHeaderLabels(("Motor Gücü", "Yol Verme", "Marka Kontaktör", "Kontaktör Kod1", "Kontaktör Kod2", "Kontaktör Kod3"))

        sorgu = "SELECT * FROM veri4"
        self.islem.execute(sorgu)

        for indexSatir, kayitNumarasi in enumerate(self.islem):
            self.anapencereform.tableWidge_veritabani_4.insertRow(indexSatir)
            for indexSutun, kayitSutun in enumerate(kayitNumarasi):
                self.anapencereform.tableWidge_veritabani_4.setItem(indexSatir, indexSutun, QTableWidgetItem(str(kayitSutun)))
    def guncelle_rowids1(self): 
        self.islem.execute("SELECT rowid FROM veri1")
        rowids = [kayit[0] for kayit in self.islem.fetchall()]
        new_rowids = itertools.count(start=1)

        for current_rowid, new_rowid in zip(rowids, new_rowids):
            if current_rowid != new_rowid:
                self.islem.execute("UPDATE veri1 SET rowid = ? WHERE rowid = ?", (new_rowid, current_rowid))

        self.baglanti.commit()
        self.anapencereform.statusbar.showMessage("Veritabanı güncellendi ve rowid'ler yeniden numaralandırıldı")
    def guncelle_rowids2(self): 
        self.islem.execute("SELECT rowid FROM veri2")
        rowids = [kayit[0] for kayit in self.islem.fetchall()]
        new_rowids = itertools.count(start=1)

        for current_rowid, new_rowid in zip(rowids, new_rowids):
            if current_rowid != new_rowid:
                self.islem.execute("UPDATE veri2 SET rowid = ? WHERE rowid = ?", (new_rowid, current_rowid))

        self.baglanti.commit()
        self.anapencereform.statusbar.showMessage("Veritabanı güncellendi ve rowid'ler yeniden numaralandırıldı")
    def guncelle_rowids3(self): 
        self.islem.execute("SELECT rowid FROM veri3")
        rowids = [kayit[0] for kayit in self.islem.fetchall()]
        new_rowids = itertools.count(start=1)

        for current_rowid, new_rowid in zip(rowids, new_rowids):
            if current_rowid != new_rowid:
                self.islem.execute("UPDATE veri3 SET rowid = ? WHERE rowid = ?", (new_rowid, current_rowid))

        self.baglanti.commit()
        self.anapencereform.statusbar.showMessage("Veritabanı güncellendi ve rowid'ler yeniden numaralandırıldı")
    def guncelle_rowids4(self): 
        self.islem.execute("SELECT rowid FROM veri4")
        rowids = [kayit[0] for kayit in self.islem.fetchall()]
        new_rowids = itertools.count(start=1)

        for current_rowid, new_rowid in zip(rowids, new_rowids):
            if current_rowid != new_rowid:
                self.islem.execute("UPDATE veri4 SET rowid = ? WHERE rowid = ?", (new_rowid, current_rowid))

        self.baglanti.commit()
        self.anapencereform.statusbar.showMessage("Veritabanı güncellendi ve rowid'ler yeniden numaralandırıldı")
    def verisil1(self):
        sil_mesaj = QMessageBox.question(self, "Silme Onayı", "Silmek İstediğinizden Emin Misiniz?", QMessageBox.Yes | QMessageBox.No)

        if sil_mesaj == QMessageBox.Yes:
            secilen_kayit = self.anapencereform.tableWidge_veritabani_1.selectedItems()
            if not secilen_kayit:
                self.anapencereform.statusbar.showMessage("Silinecek bir kayıt seçilmedi")
                return
            secilen_satir = secilen_kayit[0].row()

            try:
                self.islem.execute("DELETE FROM veri1 WHERE rowid = ?", (secilen_satir + 1,))
                self.baglanti.commit()

                self.guncelle_rowids1()
                self.anapencereform.statusbar.showMessage("Kayıt Başarıyla Silindi")
                self.kayit_listele_veri()
            except Exception as error:
                self.anapencereform.statusbar.showMessage("Kayıt Silinirken Hata Çıktı: " + str(error))
        else:
            self.anapencereform.statusbar.showMessage("Silme İşlemi İptal Edildi")
    def verisil2(self):
        sil_mesaj = QMessageBox.question(self, "Silme Onayı", "Silmek İstediğinizden Emin Misiniz?", QMessageBox.Yes | QMessageBox.No)

        if sil_mesaj == QMessageBox.Yes:
            secilen_kayit = self.anapencereform.tableWidge_veritabani_2.selectedItems()
            if not secilen_kayit:
                self.anapencereform.statusbar.showMessage("Silinecek bir kayıt seçilmedi")
                return
            secilen_satir = secilen_kayit[0].row()

            try:
                self.islem.execute("DELETE FROM veri2 WHERE rowid = ?", (secilen_satir + 1,))
                self.baglanti.commit()

                self.guncelle_rowids2()
                self.anapencereform.statusbar.showMessage("Kayıt Başarıyla Silindi")
                self.kayit_listele_veri()
            except Exception as error:
                self.anapencereform.statusbar.showMessage("Kayıt Silinirken Hata Çıktı: " + str(error))
        else:
            self.anapencereform.statusbar.showMessage("Silme İşlemi İptal Edildi")
    def verisil3(self):
        sil_mesaj = QMessageBox.question(self, "Silme Onayı", "Silmek İstediğinizden Emin Misiniz?", QMessageBox.Yes | QMessageBox.No)

        if sil_mesaj == QMessageBox.Yes:
            secilen_kayit = self.anapencereform.tableWidge_veritabani_3.selectedItems()
            if not secilen_kayit:
                self.anapencereform.statusbar.showMessage("Silinecek bir kayıt seçilmedi")
                return
            secilen_satir = secilen_kayit[0].row()

            try:
                self.islem.execute("DELETE FROM veri3 WHERE rowid = ?", (secilen_satir + 1,))
                self.baglanti.commit()

                self.guncelle_rowids3()
                self.anapencereform.statusbar.showMessage("Kayıt Başarıyla Silindi")
                self.kayit_listele_veri()
            except Exception as error:
                self.anapencereform.statusbar.showMessage("Kayıt Silinirken Hata Çıktı: " + str(error))
        else:
            self.anapencereform.statusbar.showMessage("Silme İşlemi İptal Edildi")
    def verisil4(self):
        sil_mesaj = QMessageBox.question(self, "Silme Onayı", "Silmek İstediğinizden Emin Misiniz?", QMessageBox.Yes | QMessageBox.No)

        if sil_mesaj == QMessageBox.Yes:
            secilen_kayit = self.anapencereform.tableWidge_veritabani_4.selectedItems()
            if not secilen_kayit:
                self.anapencereform.statusbar.showMessage("Silinecek bir kayıt seçilmedi")
                return
            secilen_satir = secilen_kayit[0].row()

            try:
                self.islem.execute("DELETE FROM veri4 WHERE rowid = ?", (secilen_satir + 1,))
                self.baglanti.commit()

                self.guncelle_rowids4()
                self.anapencereform.statusbar.showMessage("Kayıt Başarıyla Silindi")
                self.kayit_listele_veri()
            except Exception as error:
                self.anapencereform.statusbar.showMessage("Kayıt Silinirken Hata Çıktı: " + str(error))
        else:
            self.anapencereform.statusbar.showMessage("Silme İşlemi İptal Edildi")
    def kayit_listele_veri(self):
        self.verilistele1()
        self.verilistele2()
        self.verilistele3()
        self.verilistele4()
if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    main_window = AnapencerePage()
    main_window.show()
    sys.exit(app.exec_())