# Introduction to Python, Ödev 2
# IEEE Hacettepe University Student Branch, Güz 2026
#
# Bu ödevin sonunda klavyeden okuduğunuz bilgiyi temizleyip doğru type'a
# çevirebilecek, kıyaslama ve if, elif, else ile programınıza karar
# verdirebileceksiniz.
#
# Son teslim: 1 Kasım 2026 Pazar 23.59
# Teslim formu: https://forms.gle/85GMMkxWLvinDtiW6
# Ödev reposu: https://github.com/natozenbilek/student-card-python-hw
#
# Ödevi nasıl yapacaksınız
# 1. Bu dosyayı python-kurs klasörünüze kaydedin ve PyCharm'da açın.
# 2. Her görevde "# TODO" satırının yerine kodunuzu yazın.
# 3. Dosyayı Run ile çalıştırın. Her görevin başlık satırından sonraki
#    çıktısı, o görevin "Beklenen çıktı" kısmıyla birebir aynı olmalı.
#    input() soran görevlerde, görevde yazan değerleri Run penceresine
#    yazıp Enter'a basın.
# 4. Dosya her çalıştığında bütün görevlerin sorularını baştan sorar. Bir
#    görev üzerinde çalışırken öteki görevlerin kodunu seçip Ctrl+/
#    (macOS: Cmd+/) ile comment yapabilirsiniz; teslimden önce geri açın.
# 5. Bitince formda "İsim" alanına isminizi yazın, odev2.py'yi "Ödev
#    dosyası" alanına yükleyin ve "Kişisel verileriniz" sorusundaki onay
#    kutusunu işaretleyin. Söylemek istediğiniz bir şey varsa "Açıklama"
#    alanına yazabilirsiniz; bu alan isteğe bağlı.
#
# Dosya bu haliyle de hatasız çalışır ve yalnızca görev başlıklarını yazar.
# Yalnızca Ders 1 ve Ders 2'de gördüğümüz yapıları kullanın; while ve for
# Ders 3'te gelecek.


print("=== 1. Öğrenci kartı ===")
# input() ile adı ve bölümü sorun; name ve department variable'larına
# koyun. Ortadaki satırı + ile birleştirin. Üst ve alt çizgi "*" * 20 olsun.
# Çalıştırınca şunları yazın: Mehmet, BBM
# TODO
#
# Beklenen çıktı:
# Adınız: Mehmet
# Bölümünüz: BBM
# ********************
# Mehmet, BBM öğrencisi
# ********************


print("=== 2. Kelime sayacı ===")
text = "  Python  ile   ilk programımı yazdım "
# Bir cümlede kelime sayısı, boşluk sayısının bir fazlasıdır.
# a) text'i strip() ile temizleyip yine text'e atayın. Kelimeleri bu
#    kuralla, count() ile sayın. Kelimelerin arasında fazladan boşluk
#    olduğu için sonuç yanlış çıkar.
# b) replace() ile çift boşlukları ("  ") tek boşluğa çevirip sonucu yine
#    text'e atayın. Kaç çift boşluk kaldığını count() ile yazdırın. Hala
#    çift boşluk varsa aynı iki satırı bir kez daha yazın.
# c) text'i köşeli parantez içinde yazdırın ve kelimeleri yeniden sayın.
# d) Bir replace() neden yetmedi? Kodun altına bir comment ile yazın.
# TODO
#
# Beklenen çıktı:
# Önce: 8 kelime
# Kalan çift boşluk: 1
# Kalan çift boşluk: 0
# [Python ile ilk programımı yazdım]
# Sonra: 5 kelime


print("=== 3. Ağırlıklı puan ===")
# Ders kodunu sorun; strip() ve upper() ile temizleyin.
# Krediyi int() ile alın.
# Katsayı virgülle yazılıyor: virgülü replace() ile noktaya çevirin, sonra
# float() ile sayıya çevirip coefficient'a koyun.
# Ağırlıklı puan, kredi * katsayıdır. Bir f-string ile, iki basamakla
# yazın.
# Sonra iki bool yazdırın: ders geçildi mi (katsayı en az 1.75 mi) ve
# katsayı geçerli mi (0 ile 4 arasında mı, and ile).
# Çalıştırınca şunları yazın: "  fiz127" (önünde iki boşlukla), 3, 2,75
# TODO
#
# Beklenen çıktı:
# Ders kodu:   fiz127
# Kredi: 3
# Katsayı: 2,75
# FIZ127: 8.25 puan
# Geçti mi? True
# Katsayı geçerli mi? True


print("=== 4. Tek ve çift ===")
# input() ile bir tam sayı isteyin ve int() ile number'a koyun.
# Önce sayının 2'ye bölümünden kalanı yazdırın. Kalan 0 ise sayı çifttir:
# if ve else ile sayının yanına "çift" ya da "tek" yazdırın.
# Çalıştırınca 2026 yazın. Öteki yolu da görmek için bir kez de 7 ile
# çalıştırın; son iki satır "Kalan: 1" ve "7 tek" olmalı.
# TODO
#
# Beklenen çıktı:
# Bir tam sayı: 2026
# Kalan: 0
# 2026 çift


print("=== 5. Geçti mi ===")
# Bir derste vize yüzde 40, final yüzde 60 sayılsın:
# ortalama = vize * 0.4 + final * 0.6
# Yönetmeliğe göre final barajı 50'den düşük olamaz; bu derste 50 olsun.
# Finalden 50 alamayan öğrenci, ortalaması ne olursa olsun kalır.
# a) Vize ve final puanlarını int() ile alıp midterm ve final
#    variable'larına koyun. Ortalamayı round() ile tam sayıya yuvarlayıp
#    average'a koyun ve yazdırın.
# b) if, elif ve else ile üç yoldan birini yazdırın:
#    - final 50'nin altındaysa "Kaldı, çünkü final 50'nin altında."
#    - değilse ve ortalama en az 50 ise "Geçti."
#    - ikisi de değilse "Kaldı, çünkü ortalama 50'nin altında."
#    Hangi şartı önce sınadığınız önemli: 90 ve 45'in ortalaması 63'tür,
#    ama bu öğrenci kalır.
# Çalıştırınca şunları yazın: 90, 45
# Sonra iki kez daha çalıştırıp öteki yolları da görün:
#   30 ve 70: "Ortalama: 54" ve "Geçti."
#   40 ve 55: "Ortalama: 49" ve "Kaldı, çünkü ortalama 50'nin altında."
# TODO
#
# Beklenen çıktı:
# Vize: 90
# Final: 45
# Ortalama: 63
# Kaldı, çünkü final 50'nin altında.


print("=== Meraklısına ===")
# Zorunlu değil.
# Taş, kağıt, makas: taş makası, makas kağıdı, kağıt taşı yener.
# İki oyuncunun seçimini input() ile sorun, strip() ile temizleyip first
# ve second variable'larına koyun.
# if ile önce beraberliği sınayın: "Berabere."
# elif'te birinci oyuncunun kazandığı üç durumu and ve or ile tek bir
# condition'da birleştirin: "1. oyuncu kazandı."
# else'te: "2. oyuncu kazandı."
# Satır çok uzarsa üç durumu önce ayrı bool variable'lara koyabilirsiniz:
# rock_wins = first == "taş" and second == "makas"
# Cevapları küçük harfle yazın; yalnızca taş, kağıt ya da makas yazıldığını
# varsayabilirsiniz.
# Çalıştırınca şunları yazın: taş, makas
# TODO
#
# Beklenen çıktı:
# 1. oyuncu: taş
# 2. oyuncu: makas
# 1. oyuncu kazandı.
