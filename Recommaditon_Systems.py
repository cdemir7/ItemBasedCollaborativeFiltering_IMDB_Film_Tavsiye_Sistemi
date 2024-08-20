#Gerekli kütüphaneleri ekleyelim.
import numpy as np
import pandas as pd


#Tab'lar ile ayrılan verileri başlıkları ile alıp dataframe'e aktarıyoruz ve ekrana yazdırıyoruz.
column_names = ["user_id", "item_id", "rating", "timestamp"]
df = pd.read_csv("users.data", sep="\t", names=column_names)
#print(df.head()) #1

#Kaç kayıt olduğunu da görelim.
#print(len(df))  #100003


#Diğer dosyamızı da yükleyelim.
movie_titles =  pd.read_csv("movie_id_titles.csv")
#print(movie_titles.head()) #2

#Kaç kayıt olduğunu da görelim.
#print(len(movie_titles))  #1682


#Şimdi iki tablo arasında merge işlemini yapalım.
df = pd.merge(df, movie_titles, on="item_id")
#print(df.head()) #3


#Şimdi gerekli sistemimizi yani veri modelimizi kuralım.
#Öncelikle Excel'deki gibi pivot tabloya benzeyen bir yapı kuruyoruz.
#Kurulan bu yapıda satırlar kullanıcı(user_id) ve sütunlar film isimleri(title) olacak şeklinde ayarlıyoruz.
#Tablo içerisinde ise rating değerleri bulunacak. Bu istenirleree uygun dataframe oluşturalım.
moviemat = df.pivot_table(index="user_id", columns="title", values="rating")
#print(moviemat.head()) #4


#Şimdi dataframe'de bulunan "Star Wars (1977)" filminin ratinglerine bakalım.
starwars_userratings = moviemat["Star Wars (1977)"]
#print(starwars_userratings) #5


#Pandas kütüphanesinde bulunan corrwith() metodu ile verilen serinin
#korelasyonunu hesaplıyoruz.
similar_to_starwars = moviemat.corrwith(starwars_userratings)
#print(similar_to_starwars) #6

#Bu sonuç bir dataframe değil ve içerisinde boş veriler bulunuyor.
#Bu seriyi temizleyip dataframe'e çevirelim.
corr_starwars = pd.DataFrame(similar_to_starwars, columns=["Correlation"])
corr_starwars.dropna(inplace=True)
#print(corr_starwars.head())

#Sonuçta ortaya çıkan dataframe'i sıralayalım ve Star Wars filmine en yakın filmi bulalalım.
#print(corr_starwars.sort_values("Correlation", ascending=False).head()) #7

#Görüldüğü üzere çok fazla alakasız sonuç ortaya çıktı. Bunun nedenini incelediğimizde,
#bazı filmlerin oy sayısının çok az olması sebep olmuştur. Buradaki hatayı düzeltmek için 100 oydan
#daha az oy alan filmleri eleyelim. Bunun için ratings isminde bir dataframe oluşturalım ve her filmin oy sayılarını bulalım.
#Bu arada kullanmadığım "timestamp" sütununu atalım.
df.drop(["timestamp"], axis=1)

#Her filmin ortalama rating değerini bulalım.
ratings = pd.DataFrame(df.groupby("title")["rating"].mean())

#Dataframe'i büyükten küçüğe sıralayıp bir göz atalım.
#print(ratings.sort_values("rating", ascending=False).head()) #8

#Her filmin aldığı oy sayısına bakalım.
ratings["rating_oy_sayisi"] = pd.DataFrame(df.groupby("title")["rating"].count())
#print(ratings.head()) #9

#En çok oy alan filmleri sıralayalım.
#print(ratings.sort_values("rating_oy_sayisi", ascending=False).head()) #10


#Şimdi star wars dataframe'ine oy sayısı sütununuu da ekleyelim.
corr_starwars = corr_starwars.join(ratings["rating_oy_sayisi"])
#print(corr_starwars.head()) #11

#Sonuç olarak, 100den fazla oy alan ve star wars filmine en yakın 10 filmi görelim.
print(corr_starwars[corr_starwars["rating_oy_sayisi"]>100].sort_values("Correlation", ascending=False).head(10)) #12