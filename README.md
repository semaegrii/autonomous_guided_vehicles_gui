
## *AGV' LER İÇİN MANUEL VE OTONOM KONTROL ARAYÜZÜ*

**Geliştirme ve Deneme**: Sema EĞRİ💻 ve Ramazan GÜL💻

🚙🚙🚙🚙🚙🚙🚙🚙🚙🚙🚙🚙🚙🚙🚙🚙🚙🚙🚙🚙🚙🚙🚙🚙🚙🚙🚙🚙🚙🚙🚙🚙🚙🚙🚙🚙🚙🚙🚙🚙🚙🚙🚙🚙🚙🚙🚙🚙🚙🚙🚙

| ANASAYFA SEKMESI 🏡|KONTROL SEKMESI 🚗 | DURAK TAKİP SEKMESI 🕹 | AYARLAR SEKMESI 🛠️|
| ------ | ------ | ------ | ------ |
| ARAÇLARIN AKTİFLİK DURUMLARI | ARAÇLARIN İKON OLARAK GÖRSELLEŞTİRİLDİĞİ KISIM | DURAK İSMİ VE KONUMU KAYDETME | PLC HABERLEŞME |
| KAPATMA VE YENİLEME BUTONU | TEKİL VE SÜRÜ OTONOM OKLA HEDEF VERME |DURAKLARA NOT EKLEME | OPERATÖR EKLEME ÇIKARMA |
| LOGLARIN YAZILMASI İLE HATA KONTROLÜ |TEKİL VE SÜRÜ BUTON İLE MANUEL KONTROL | DURAK EKLEME VE ÇIKARMA | ROS AYARLARI |
| ARAYÜZ BAĞLANTI DURUMU KONTROLÜ | ARAÇ KONUM,HIZ,DÖNÜŞ AÇISI BİLGİSİ YAYINLAMA | İSTENEN DURAĞI SEÇEBİLME | ÖZEL KULLANICI GİRİŞİ |
|![anasayfa](https://user-images.githubusercontent.com/78825912/181281807-03768be9-78e6-454f-9cde-c994948567b8.jpeg) |![kontrol](https://user-images.githubusercontent.com/78825912/181281869-7b35bec2-a4eb-48ca-a7be-6565c2fa479f.jpeg) |![durak](https://user-images.githubusercontent.com/78825912/181282110-6e306728-110e-4e83-879b-f6d73bb2ddcd.jpeg) |![ayarlar](https://user-images.githubusercontent.com/78825912/181282194-e51ff406-4edb-4c2c-abe8-eecab5ccd654.jpeg) |
|![kontrol](https://user-images.githubusercontent.com/78825912/181281963-e16c2754-c279-4547-824f-cfea19da9c86.jpeg) |![durak](https://user-images.githubusercontent.com/78825912/181282154-8a8f71a9-ae4f-414f-be0d-67771b1e5120.jpeg) |![kontrol](https://user-images.githubusercontent.com/78825912/181282045-c086c4e9-21ed-435d-ac13-76cefaebc67f.jpeg) |![kontrol](https://user-images.githubusercontent.com/78825912/181281986-663518b1-f99f-4d40-aa6d-03a111d5e586.jpeg) |![durak](https://user-images.githubusercontent.com/78825912/181282132-854125b0-29c1-4651-8f3a-3d3979be3f63.jpeg) |![durak](https://user-images.githubusercontent.com/78825912/181282171-45509c4e-ec0b-4a07-8040-1eb037561a26.jpeg) |

🚙🚙🚙🚙🚙🚙🚙🚙🚙🚙🚙🚙🚙🚙🚙🚙🚙🚙🚙🚙🚙🚙🚙🚙🚙🚙🚙🚙🚙🚙🚙🚙🚙🚙🚙🚙🚙🚙🚙🚙🚙🚙🚙🚙🚙🚙🚙🚙🚙🚙🚙🚙🚙



ROS ortamında geliştirdiğim otonom takip araçları (AGV) için tasarladığım kullanıcı arayüzünü paylaşmak istiyorum sizlerle.

Arayüz 4 ana bölümden oluşmakta:

## 1. Ana sayfa

▪︎*Bu bölümde, araçların robot-arayüz ve plc-arayüz bağlantı durumları kontrol edilmekte*,

▪︎*Kodda herhangi bir sorun varsa hataları log kısmında görüntülenmektedir*.

## 2. Robot Kontrol

▪︎*Araçların birbirinden bağımsız ve sürü olarak manuel kontrolleri sağlanmakta*,

▪︎*Araçtan alınan açısal ve lineer hız, konum ve dönüş açısı bilgileri görüntülenmekte,*

▪︎*Opencv ile görselleştirilen araçlar Gazebo simülasyon ortamında hangi konumdaysa bu bölümden izlenebilmektedir.*

## 3. Araç İstasyon Takibi

▪︎*Araçların başlangıç ve hedef konumlarını yanına özet bilgi ilave ederek kaydedebileceğiniz bir bölme oluşturulmuştur.*

▪︎*Her araç için ayrı ayrı kayıtlar oluşturulmakta ve gerek kalmadığında silinebilmektedir.*

## 4. Ayarlar

▪︎*Yeni operatör kayıtları bu bölmeden yapılmaktadır.*

▪︎*Gazebo simülasyon ortamının görselleştirilmesi için kullanılan haritanın ve ikonların kayıtları bu bölümde tutulamaktadır.*

▪︎*Bu bölme güvenlidir, işlem yapabilmek için önce kullanıcı girişi yapılmaktadır.*
