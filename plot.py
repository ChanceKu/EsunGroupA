# https://matplotlib.org/stable/gallery/pie_and_polar_charts/pie_features.html
import csv
import matplotlib.pyplot as plt
import pandas as pd
plt.rcParams['font.sans-serif'] = ['SimHei']
df = pd.read_csv('外匯存款_112年1月 (1).csv', encoding="utf-8")

# print(df)
print(df['112年1月市占率'])
print(df.iloc[:, 0])

fig, ax = plt.subplots()
ax.pie(df['112年1月市占率'], labels = df.iloc[:, 0])
plt.show()