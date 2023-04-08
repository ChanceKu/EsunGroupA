# https://matplotlib.org/stable/gallery/pie_and_polar_charts/pie_features.html

import csv
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import os

plt.rcParams['font.sans-serif'] = ['Taipei Sans TC Beta']

dir_path = './/csv'
dir_list = os.listdir(dir_path)
failed_list=[]

for file in dir_list:
    if file.endswith(".csv"):
        try:
            df = pd.read_csv(os.path.join(dir_path, file), encoding="utf-8")

            share = [] # market share
            for i in range(13):
                value = df.iloc[29, 14+2*i]
                share.append(value)
            
            rank = []   # market ranking
            for i in range(13):
                value = df.iloc[29, 15+2*i]
                rank.append(value)

            month = []
            for i in df.columns[1:14]:
                month.append(i)

            # Convert the 'month' list to the new format
            new_month = []
            for m in month:
                dt = datetime.strptime(m, '%Y年%m月')
                new_month.append(dt.strftime('%Y/%m'))

            # Convert the 'share' list to numeric values
            share = [float(s.strip('%')) / 100 for s in share]

            # Create the plot
            fig, ax1 = plt.subplots()

            # Plot the first dataset (share) on the left y-axis
            color = 'tab:red'
            ax1.set_xlabel('Month')
            ax1.set_ylabel('市占率', color=color)     #中文會亂碼, to be fixed
            ax1.plot(new_month, share, color=color, marker='o')
            ax1.tick_params(axis='y', labelcolor=color)

            # Plot the second dataset (rank) on the right y-axis
            ax2 = ax1.twinx()  # Create a second y-axis that shares the same x-axis
            color = 'tab:blue'
            ax2.set_ylabel('排名', color=color)      #中文會亂碼, to be fixed
            ax2.plot(new_month, rank, color=color, marker='o')
            ax2.tick_params(axis='y', labelcolor=color)

            # Set the x-tick positions and labels
            xticks = range(len(new_month))
            plt.xticks(xticks, new_month)
            plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45)

            # Add data labels to the plot
            for x, y1, y2 in zip(xticks, share, rank):
                ax1.text(x, y1, f'{y1:.2f}', ha='center', va='bottom')
                ax2.text(x, y2, f'{y2:.0f}', ha='center', va='bottom')

            # 幫圖加上標題
            plt.title(os.path.splitext(file)[0])     

            # create folder if it does not exist
            directory = ".//graph"

            if not os.path.exists(directory):
                os.makedirs(directory)

            # Save the plot
            name = os.path.splitext(file)[0] + '.png'
            plt.savefig(os.path.join(".//graph//", name))
            print(name, "created")
            plt.close()
        except:
            print(file,"failed")
            failed_list.append(file)
            pass

print(failed_list)