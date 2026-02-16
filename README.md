# 📞 Bank Marketing Campaign Response Prediction

---

## 🚀 Gerçek Hayat Kullanım Senaryosu (Operasyonel Perspektif)

Bir bankada kampanya yöneticisi olduğunuzu düşünün.

Elinizde 200.000 müşteri var ve yeni bir kampanya başlatacaksınız.  
Çağrı merkezi kapasitesi sınırlı. Her müşteriyi aramak:

- Çağrı merkezi çalışan maliyeti
- Operasyonel zaman
- Müşteri memnuniyeti riski
- Marka algısı etkisi

oluşturuyor.

Ayrıca veri setinde bulunan `campaign` değişkeni şunu gösteriyor:

> Bu müşteri mevcut kampanya kapsamında kaç kez aranmış?

Gerçek hayatta süreç şu şekilde işler:

1. Kampanya başlatılır.
2. Müşteriler aranır.
3. İlk aramada dönüşüm olmazsa bazı müşteriler tekrar aranır.
4. Çok fazla arama yapılması müşteriyi rahatsız edebilir ve negatif dönüşe sebep olabilir.

### 🎯 Model Nerede Devreye Giriyor?

Bir banka çalışanı için kullanım senaryosu:

- Kampanya başlamadan önce model çalıştırılır.
- Her müşteri için **kampanyaya olumlu yanıt verme olasılığı** hesaplanır.
- Skoru yüksek müşteriler önceliklendirilir.
- Skoru düşük müşteriler ya hiç aranmaz ya da daha az aranır.

Bu sayede:

- Gereksiz tekrar aramalar azaltılır.
- `campaign` sayısı optimize edilir.
- Aynı bütçe ile daha fazla dönüşüm elde edilir.
- Çağrı merkezi kaynakları verimli kullanılır.

---

# 🎯 Projenin Amacı

Bu proje bir **ikili sınıflandırma (binary classification)** problemidir.

Hedef değişken:

- `y = 1` → Müşteri kampanyaya olumlu yanıt verdi  
- `y = 0` → Müşteri kampanyaya olumsuz yanıt verdi  

Toplam veri: **~750.000 kayıt**

Sınıf dağılımı:

- %88 → 0 (olumsuz yanıt)
- %12 → 1 (olumlu yanıt)

Bu ciddi bir **class imbalance** problemidir.  
Bu nedenle model performansı yalnızca accuracy ile değil:

- F1-score
- ROC-AUC
- PR-AUC

metrikleri ile değerlendirilmiştir.

---

# 📊 Veri Seti Değişkenleri

## 🔹 Kimlik ve Hedef

- `id` → Benzersiz müşteri kaydı (modelde kullanılmaz)
- `y` → Kampanya sonucu

---

## 🔹 Demografik Özellikler

- `age` → Yaş  
- `job` → Meslek  
- `marital` → Medeni durum  
- `education` → Eğitim seviyesi  
- `default` → Temerrüt durumu  

---

## 🔹 Finansal Bilgiler

- `balance` → Hesap bakiyesi  
- `housing` → Konut kredisi var mı?  
- `loan` → Tüketici kredisi var mı?  

---

## 🔹 Kampanya ve İletişim Bilgileri

- `contact` → İletişim türü  
- `day` → Aramanın günü  
- `month` → Aramanın ayı  
- `campaign` → Bu kampanya sürecinde müşterinin kaç kez arandığı  


- Çok yüksek değerler → müşteri yorgunluğu
- Çok düşük değerler → yeterince denenmemiş müşteri
- Model sayesinde tekrar arama stratejisi optimize edilebilir

---

## 🔹 Geçmiş Kampanya Bilgileri

- `pdays` → Önceki kampanyadan sonra geçen gün sayısı  
- `previous` → Önceki kampanyalardaki arama sayısı  
- `poutcome` → Önceki kampanya sonucu  

---

# 🧠 Modelleme Süreci

- Veri temizleme
- Encoding
- Class imbalance analizi
- Train/Test split
- Model eğitimi
- Threshold optimizasyonu

### Optimal threshold (F1 için):

0.689

Bu değer, varsayılan 0.5 yerine F1-score’u maksimize edecek şekilde seçilmiştir.

---

# 📈 Model Performansı

## 🔹 Eğitim Sonuçları

| Metric | Score |
|--------|-------|
| ROC-AUC | 0.8876 |
| PR-AUC | 0.5953 |
| F1 | 0.5611 |
| Accuracy | 0.89 |

Class 1:

- Precision: 0.54  
- Recall: 0.58  
- F1: 0.56  

---

## 🔹 Test Sonuçları

| Metric | Score |
|--------|-------|
| ROC-AUC | 0.8546 |
| PR-AUC | 0.5438 |
| F1 | 0.5321 |

### 📌 Yorum

- Train ve Test skorları yakın → düşük overfitting
- ROC-AUC > 0.85 → güçlü ayrıştırma
- PR-AUC > 0.54 → dengesiz veri için iyi performans
- F1 ≈ 0.53 → %12 pozitif oranlı veri için başarılı

---

# 💰 Business Etkisi

Örnek senaryo:

- 100.000 müşteri
- Arama maliyeti: 10 TL
- Ortalama kampanya getirisi: 500 TL
- Pozitif oran: %12

Model olmadan:

- 100.000 arama
- 12.000 dönüş
- Toplam maliyet: 1.000.000 TL

Model ile:

- Sadece en yüksek skorlu 40.000 müşteri aranır
- Daha yüksek dönüşüm oranı elde edilir
- Daha az maliyet ile benzer gelir

Ayrıca:

- Gereksiz tekrar aramalar azaltılır
- `campaign` optimizasyonu yapılır
- Müşteri memnuniyeti korunur

---

# 🔎 Neden Accuracy Yeterli Değil?

Veri setinde %88 negatif sınıf vardır.

Eğer model herkese "0" dese:

Accuracy = %88

Ama business açısından sıfır değer üretir.

Bu nedenle F1 ve PR-AUC kritik metriklerdir.

---

# ⚠️ Önemli Teknik Not

`duration` değişkeni kampanya sonucu oluştuktan sonra bilinir.

Gerçek zamanlı tahmin sisteminde bu bilgi bilinemez.  
Production ortamında dikkatli kullanılmalıdır.

---

# 🏁 Sonuç

Bu proje:

- Dengesiz veri setinde dengeli performans göstermektedir.
- Operasyonel karar destek sistemi olarak kullanılabilir.
- Kampanya maliyetlerini düşürme potansiyeline sahiptir.
- ROI artırma potansiyeli taşımaktadır.

---

# 🔮 Gelecek Geliştirmeler

- Cost-sensitive threshold optimizasyonu
- SMOTE / class weighting
- XGBoost / LightGBM
- Gerçek zamanlı scoring pipeline
- Arama sayısı (`campaign`) için optimum tekrar stratejisi modeli

---

# 👨‍💻 Özet

Bu model, kampanya yönetimini rastgele arama stratejisinden çıkarıp  
**veri temelli karar verme sistemine dönüştürmektedir.**

Hedef:

> Doğru müşteriye, doğru zamanda, doğru sıklıkta ulaşmak.
