# -*- coding: utf-8 -*-
"""Untitled4.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1qGffQerJUtqFI3lPTAnUeC583IQDjUv9
"""

!pip install pycountry

!pip install cartopy

import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import pyplot as plt
import plotly.express as px
from sklearn.linear_model import LinearRegression
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import pycountry
import plotly.graph_objects as go

cov20_21_22 = pd.read_excel("/content/Turkiye_Covid19_verileri_2020_2021_2022.xlsx")

cov20_21_22.head()

cov20_21_22.columns = cov20_21_22.columns.str.replace(" ", "_")

cov20_21_22.columns

cov20_21_22.drop(['Hasta_sayısı_Aktif','Ölüm_Yeni','İyileşen_Yeni','Test_sayısı_Yeni'], axis=1, inplace=True)

print(cov20_21_22)

cov20_21_22.replace([' ', '-'], 0, inplace=True)

cov20_21_22.replace('\.', '', regex=True, inplace=True)

print(cov20_21_22)

cov20_21_22.Ölüm_Toplam

cov20_21_22.Ölüm_Toplam.dtype

cov20_21_22['Ölüm_Toplam'] = cov20_21_22['Ölüm_Toplam'].replace('\.', '', regex=True)

cov20_21_22.Ölüm_Toplam

cov20_21_22['Ölüm_Toplam'] = pd.to_numeric(cov20_21_22['Ölüm_Toplam'], errors='coerce')

cov20_21_22.Ölüm_Toplam

cov20_21_22.Tarih

sns.set_theme()
sns.set(rc={"figure.dpi": 300, "figure.figsize": (12, 9)})
sns.heatmap(cov20_21_22.isnull(), cbar=False)

Stopveri = cov20_21_22[['Hasta_sayısı_Toplam', 'Ölüm_Toplam', 'İyileşen_Toplam',
       'Ağır_hastalar_Entübe', 'Ağır_hastalar_Yoğun_bakım',
       'Test_sayısı_Toplam']].count()

veriSay = pd.DataFrame({"Sütun": Stopveri.index, "Var Olan Veri Sayısı": Stopveri.values})

veriSay = veriSay.sort_values(by="Var Olan Veri Sayısı", ascending=False)

sns.set_theme()
sns.set(rc={"figure.dpi": 300, "figure.figsize": (12, 9)})
sns.barplot(x="Var Olan Veri Sayısı", y="Sütun", data=veriSay, palette="viridis", hue="Sütun", legend=False)

plt.title("Sütunlardaki Var Olan Veri Sayıları")
plt.xlabel("Var Olan Veri Sayısı")
plt.ylabel("Sütun")
plt.show()

cov20_21_22.Test_sayısı_Toplam.dtype

maxVAKA_row = cov20_21_22.sort_values(by="Hasta_sayısı_Yeni", ascending=False).iloc[0]
maxVAKA = maxVAKA_row["Tarih"]
print("En fazla hasta sayısı yeni kaydı olan tarih:", maxVAKA)

"""Toplam yeni vaka sayısını düzelttim sadece  by= yerine Hasta_sayısı_Yeni yazmam gerekiyormuş"""

topTestİyileşen=pd.read_excel("/content/toptestİyi20_21_22.xlsx")

topTestİyileşen.head()

cizim = topTestİyileşen[["YIL", "Test_sayısı_Toplam", "İyileşen_Toplam"]]

plt.figure(figsize=(12, 8))

for year in cizim["YIL"].unique():
    yılBilg = cizim[cizim["YIL"] == year]
    X = yılBilg["Test_sayısı_Toplam"].values.reshape(-1, 1)
    y = yılBilg["İyileşen_Toplam"].values.reshape(-1, 1)

    regression_model = LinearRegression()
    regression_model.fit(X, y)
    regression_line = regression_model.predict(X)

    plt.scatter(X, y, label=f"{year} Verileri")
    plt.plot(X, regression_line, label=f"{year} Regresyon", linewidth=2)

plt.title("Test_sayısı_Toplam vs. İyileşen_Toplam Regresyon Analizi - Yıllara Göre")
plt.xlabel("Test_sayısı_Toplam")
plt.ylabel("İyileşen_Toplam")
plt.legend()
plt.show()

cov20_21_22.Test_sayısı_Toplam.sum()

cov20_21_22.İyileşen_Toplam.sum()

ilGöc20=pd.read_excel("/content/2020 il il iç göç.xlsx")

ilGöc20.head()

maxgöc_satır=ilGöc20.sort_values(by="GÖÇ",ascending=False).iloc[0]
maxgöc=maxgöc_satır["İL"]
print("En fazla göç alan il : ",maxgöc)

minGöç_satır = ilGöc20.sort_values(by="GÖÇ").iloc[0]
minGöç_il = minGöç_satır["İL"]
print("En az göç alan il: ", minGöç_il)

ilGöc20.dtypes

ilgöcizim = ilGöc20[["İL", "GÖÇ"]]

plt.figure(figsize=(15, 8))
sns.barplot(x="İL", y="GÖÇ", data=ilgöcizim, palette="viridis")
plt.xticks(rotation=90)
plt.title("Şehirlere Göre Göç Verileri")
plt.xlabel("İL")
plt.ylabel("GÖÇ")
plt.show()

vakagöcizim=ilGöc20[["GÖÇ","TOPLAMVAKASAYISI"]]

plt.figure(figsize=(15,8))
sns.barplot(x="TOPLAMVAKASAYISI",y="GÖÇ",data=vakagöcizim, palette="viridis")
plt.xticks(rotation=90)
plt.title("Toplam Vaka Sayılarına göre göç verileri")
plt.xlabel("TOPLAMVAKASAYISI")
plt.ylabel("GÖÇ")
plt.show()

maxvaka_satır=ilGöc20.sort_values(by="TOPLAMVAKASAYISI",ascending=False).iloc[0]
maxvaka=maxvaka_satır["İL"]
print("En fazla vakaya sahip il : ",maxvaka)

minvaka_satır = ilGöc20.sort_values(by="TOPLAMVAKASAYISI").iloc[0]
minvaka_il = minGöç_satır["İL"]
print("En az vakaya sahip il: ", minvaka_il)

ilk_20_göc = ilGöc20.sort_values(by="GÖÇ", ascending=False).head(20)

for index, row in ilk_20_göc.iterrows():
    print(f"Il: {row['İL']}, Göç: {row['GÖÇ']}")

ilk_20_vaka = ilGöc20.sort_values(by="TOPLAMVAKASAYISI", ascending=False).head(20)

for index, row in ilk_20_vaka.iterrows():
    print(f"Il: {row['İL']}, Toplam Vaka Sayısı: {row['TOPLAMVAKASAYISI']}")

ilGöc20.head()

güneyDoguVaka = ilGöc20.loc[ilGöc20["BÖLGE"] == "Güneydoğu Anadolu", ["İL", "TOPLAMVAKASAYISI", "BÖLGE"]]

güneyDoguİl = ilGöc20.loc[ilGöc20["BÖLGE"] == "Güneydoğu Anadolu", ["İL", "GÖÇ", "BÖLGE"]]

doguAnadoluİl = ilGöc20.loc[ilGöc20["BÖLGE"] == "Doğu Anadolu", ["İL", "GÖÇ", "BÖLGE"]]

akdenizİl = ilGöc20.loc[ilGöc20["BÖLGE"] == "Akdeniz", ["İL", "GÖÇ", "BÖLGE"]]

içAnadoluİl = ilGöc20.loc[ilGöc20["BÖLGE"] == "İç Anadolu", ["İL", "GÖÇ", "BÖLGE"]]

karadenizİl = ilGöc20.loc[ilGöc20["BÖLGE"] == "Karadeniz", ["İL", "GÖÇ", "BÖLGE"]]

egeİl = ilGöc20.loc[ilGöc20["BÖLGE"] == "Ege", ["İL", "GÖÇ", "BÖLGE"]]

marmaraİl = ilGöc20.loc[ilGöc20["BÖLGE"] == "Marmara", ["İL", "GÖÇ", "BÖLGE"]]

print(güneyDoguİl)

içAnadoluİl.GÖÇ.sum()

karadenizİl.GÖÇ.sum()

güneyDoguİl.GÖÇ.sum()

akdenizİl.GÖÇ.sum()

marmaraİl.GÖÇ.sum()

doguAnadoluİl.GÖÇ.sum()

egeİl.GÖÇ.sum()

güneyDoguVaka = ilGöc20.loc[ilGöc20["BÖLGE"] == "Güneydoğu Anadolu", ["İL", "TOPLAMVAKASAYISI", "BÖLGE"]]
egeVaka = ilGöc20.loc[ilGöc20["BÖLGE"] == "Ege", ["İL", "TOPLAMVAKASAYISI", "BÖLGE"]]
doguAnadoluVaka = ilGöc20.loc[ilGöc20["BÖLGE"] == "Doğu Anadolu", ["İL", "TOPLAMVAKASAYISI", "BÖLGE"]]
içAnadoluVaka = ilGöc20.loc[ilGöc20["BÖLGE"] == "İç Anadolu", ["İL", "TOPLAMVAKASAYISI", "BÖLGE"]]
akdenizVaka = ilGöc20.loc[ilGöc20["BÖLGE"] == "Akdeniz", ["İL", "TOPLAMVAKASAYISI", "BÖLGE"]]
marmaraVaka = ilGöc20.loc[ilGöc20["BÖLGE"] == "Marmara", ["İL", "TOPLAMVAKASAYISI", "BÖLGE"]]
karadenizVaka = ilGöc20.loc[ilGöc20["BÖLGE"] == "Karadeniz", ["İL", "TOPLAMVAKASAYISI", "BÖLGE"]]

güneyDoguVaka.TOPLAMVAKASAYISI.sum()

egeVaka.TOPLAMVAKASAYISI.sum()

doguAnadoluVaka.TOPLAMVAKASAYISI.sum()

içAnadoluVaka.TOPLAMVAKASAYISI.sum()

akdenizVaka.TOPLAMVAKASAYISI.sum()

marmaraVaka.TOPLAMVAKASAYISI.sum()

karadenizVaka.TOPLAMVAKASAYISI.sum()

import geopandas as gpd

!pip install geopandas

tr_harita = gpd.read_file("/content/tr-cities-utf8.json")

il_goc_verisi = ilGöc20[["İL", "GÖÇ"]]

tr_harita_with_goc = tr_harita.merge(il_goc_verisi, how='left', left_on='name', right_on='İL')

fig, ax = plt.subplots(figsize=(15, 10))
tr_harita_with_goc.plot(ax=ax, column='GÖÇ', cmap='OrRd', legend=True, legend_kwds={'label': "Göç Sayısı"})
plt.title("Türkiye'deki İllere Göre Göç Sayısı")
plt.show()

print(tr_harita.columns)

tr_harita.info

"""PM10 ( µg/m3 ): Partiküler Madde 10 Mikrometre veya daha küçük (PM10) partikül madde konsantrasyonu. Havanın içinde bulunan solunabilir partikül maddenin bir ölçüsüdür.

PM 2.5 ( µg/m3 ): Partiküler Madde 2.5 Mikrometre veya daha küçük (PM2.5) partikül madde konsantrasyonu. PM10'dan daha küçük partikül madde miktarını ölçer ve solunabilir ince partikül maddenin bir göstergesidir.

SO2 ( µg/m3 ): Kükürt Dioksit (SO2) konsantrasyonu. Hava kalitesini değerlendirmek için önemli bir hava kirletici olan kükürt dioksitin bir ölçüsüdür.

CO ( µg/m3 ): Karbon Monoksit (CO) konsantrasyonu. Karbon monoksit, fosil yakıt yanması gibi kaynaklardan kaynaklanan bir hava kirleticisidir.

NO2 ( µg/m3 ): Nitrojen Dioksit (NO2) konsantrasyonu. Motorlu taşıtlardan ve endüstriyel faaliyetlerden kaynaklanan bir hava kirletici olan nitrojen dioksitin bir ölçüsüdür.

NOX ( µg/m3 ): Azot Oksit (NOx) konsantrasyonu. NO2 dahil olmak üzere tüm azot oksitleri ölçen bir parametredir.

NO ( µg/m3 ): Nitrik Oksit (NO) konsantrasyonu. Havanın içinde bulunan bir azot oksit türünü ölçer. NOx'in bir bileşeni olarak nitrik oksit, özellikle yanma süreçlerinden kaynaklanır.
"""

ilvakaS1ni20 = pd.read_excel("/content/il il vaka sayısı 1 nisan 2020'e kadar.xlsx")

ilvakaS1ni20

ilvakaS1ni20_sirali = ilvakaS1ni20.sort_values(by='TOPLAMVAKASAYISI1N20', ascending=False)

ilk_15_il = ilvakaS1ni20_sirali.head(15)

print(ilk_15_il[['İL', 'TOPLAMVAKASAYISI1N20']])

ilvakaS1ni20_sirali = ilvakaS1ni20.sort_values(by='TOPLAMVAKASAYISI1N20', ascending=True)

ilk_15_il = ilvakaS1ni20_sirali.head(15)

print(ilk_15_il[['İL', 'TOPLAMVAKASAYISI1N20']])

ilvakaS1ni20_sirali = ilvakaS1ni20.sort_values(by='CO ( µg/m3 )', ascending=False)

ilk_10_il = ilvakaS1ni20_sirali.head(10)

print(ilk_10_il[['İL', 'CO ( µg/m3 )']])

ilvakaS1ni20_sirali = ilvakaS1ni20.sort_values(by='PM10 ( µg/m3 )', ascending=False)

ilk_10_il = ilvakaS1ni20_sirali.head(10)

print(ilk_10_il[['İL', 'PM10 ( µg/m3 )']])

ilvakaS1ni20_sirali = ilvakaS1ni20.sort_values(by='PM 2.5 ( µg/m3 )', ascending=False)

ilk_10_il = ilvakaS1ni20_sirali.head(10)

print(ilk_10_il[['İL', 'PM 2.5 ( µg/m3 )']])

ilvakaS1ni20_sirali = ilvakaS1ni20.sort_values(by='SO2 ( µg/m3 )', ascending=False)

ilk_10_il = ilvakaS1ni20_sirali.head(10)

print(ilk_10_il[['İL']])

ilvakaS1ni20.columns

ilvakaS1ni20_sirali = ilvakaS1ni20.sort_values(by='O3 ( µg/m3 )', ascending=False)

ilk_10_il = ilvakaS1ni20_sirali.head(10)

print(ilk_10_il[['İL']])

ilvakaS1ni20_sirali = ilvakaS1ni20.sort_values(by='NOX ( µg/m3 )', ascending=False)

ilk_10_il = ilvakaS1ni20_sirali.head(10)

print(ilk_10_il[['İL']])

ilvakaS1ni20_sirali = ilvakaS1ni20.sort_values(by='NOX ( µg/m3 )', ascending=False)

ilk_10_il = ilvakaS1ni20_sirali.head(10)

print(ilk_10_il[['İL']])

tr_harita = gpd.read_file("/content/tr-cities-utf8.json")

merged_data = tr_harita.merge(ilvakaS1ni20, left_on='name', right_on='İL', how='inner')

fig, ax = plt.subplots(figsize=(20, 15))

merged_data.plot(column='SO2 ( µg/m3 )', cmap='OrRd', linewidth=0.8, ax=ax, edgecolor='0.8', legend=True,
                  legend_kwds={'label': "SO2 (µg/m3)"})

for x, y, label in zip(merged_data.geometry.centroid.x, merged_data.geometry.centroid.y, merged_data['İL']):
    ax.text(x, y, label, fontsize=8, ha='center')

plt.title("İllerin SO2 Konsantrasyonu")
plt.show()

from mpl_toolkits.axes_grid1 import make_axes_locatable

tr_harita.columns

ilvakaS1ni20.columns

ilvakaS1ni20_CO=ilvakaS1ni20[["İL","CO ( µg/m3 )"]]

ilvakaS1ni20 = pd.read_excel("/content/il il vaka sayısı 1 nisan 2020'e kadar.xlsx")

merged_data = tr_harita.merge(ilvakaS1ni20, left_on='name', right_on='İL', how='inner')


fig, ax = plt.subplots(1, 1, figsize=(15, 10))

divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.1)

merged_data.plot(column='CO ( µg/m3 )', cmap='OrRd', linewidth=0.8, ax=ax, edgecolor='0.8',
                 legend=True, cax=cax, legend_kwds={'label': "CO Yoğunluğu (µg/m3)"})

for x, y, label in zip(merged_data.geometry.centroid.x, merged_data.geometry.centroid.y, merged_data['İL']):
    ax.text(x, y, label, fontsize=8, ha='center')

plt.title("İllerin CO Yoğunluğu Haritası")
plt.show()

"""son iki haritadada istediğim sonuçu elde edemedim fakat verileri elde edebildim.Haritalarda istediğim görüntü CO yoğunluğunun fazla olduğu illeri koyudan açık renge renklendirmesi fakat koordinat veri setimin crs formatına dönüştüremediğimden çoğu il gözükmüyor."
"""