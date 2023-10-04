
# Ürün Listeleme Programı

Bu proje python ve Qt kullanılarak geliştirilen bir bilgisayar programıdır.. Program, ürün listeleme ve bu listeyi excele çevirerek kullanıcıya sunmaktadır. Program içerisinde bulunan ürünleri SQLite veritabanında depolar. 


## İÇİNDEKİLER

- Program Kurulum Kılavuzu
- Program Kullanım Kılavuzu




  
## Program Kurulum  Kılavuzu
   Dosyaları indirdikten sonra PyQt5, SQLite3, Tkinter, sys, json, shutil, pandas ve itertools kütüphanelerini yüklemeniz gerekmektedir.
   Eğer programı bilgisayarınıza exe dosyası olarak saklamak isterseniz ilk önce pyinstaller kütüphanesini yüklemelisiniz. Ardından terminal üzerinden 
```
cd (giris.py dosaysının bilgisayrınızdaki uzantısı)
```
komutunu çalıştırınız. Ardından 
```
pyinstaller --onefile --noconsole --icon=f_logo-150x150.ico giris.py
```
komutu ile programı exe dosyasına çevirebilrsiniz. 
## Program Kullanım  Kılavuzu
"giris.py" dosyası program açılış ekranını kapsar. "main.py" dosyası programın özelliklerini kapsamaktadır. "anapencere_python.py" dosyası "anapencere_python.ui" dosyasının python dosyasına dönüştürülmüş halidir ve programın tasarımını kapsamaktadır.
![Uygulama Ekran Görüntüsü](https://github.com/ahmetymtkn/Urun-Listeleme-Programi/blob/main/images/Ekran%20g%C3%B6r%C3%BCnt%C3%BCs%C3%BC%202023-10-03%201351201.png?raw=true)
![Uygulama Ekran Görüntüsü](https://github.com/ahmetymtkn/Urun-Listeleme-Programi/blob/main/images/Ekran%20g%C3%B6r%C3%BCnt%C3%BCs%C3%BC%202023-10-03%20135154123.png?raw=true)
