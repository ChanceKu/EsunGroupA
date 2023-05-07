import csv
import pandas as pd
from datetime import datetime
import os
import subprocess
import matplotlib.pyplot as plt

def plots(dir, bk):
    banks = bk
    dir_list = os.listdir(dir)
    plt.rcParams['font.sans-serif'] = ['Taipei Sans TC Beta']
    for i in dir_list:
        print(i)
        csv_name, extension = os.path.splitext(i)
        df = pd.read_csv(dir +"//" +i, encoding="utf-8")

        data = []
        bank = []
        for i in range(len(banks)):
            try:
                data.append(df[banks[i]])
                bank.append(banks[i])
            except:
                pass             

        #取得月份
        month = df.iloc[:,0]

        # 把月份格式更改, 例:2022年01月 -> 2022/01
        new_month = []
        try:
            for m in month:
                dt = datetime.strptime(m, '%Y年%m月')
                new_month.append(dt.strftime('%Y/%m'))
        except:
            new_month = month

        # Create the plot
        fig, ax = plt.subplots()

        fig, ax = plt.subplots(figsize=(16, 9))

        colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'purple', 'orange', 'brown']

        for i in range(len(bank)):
            try:
                ax.plot(data[i], color = colors[i], label = bank[i])
            except:
                print(bank[i], "404")

        # Set the x-tick positions and labels
        plt.xticks(range(0, len(month), 3), [new_month[i] for i in range(0, len(new_month), 3)])
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)

        # 幫圖加上標題
        plt.title(csv_name)     

        # Add a legend to the plot
        ax.legend()

        # create folder if it does not exist
        directory = ".//graph"

        if not os.path.exists(directory):
            os.makedirs(directory)

        # Save the plot
        name = csv_name + '.png'
        plt.savefig(os.path.join(".//graph//", name))
        plt.close()

def main():
    plots(".//csv", ["中國信託商業銀行", "台北富邦商業銀行", "國泰世華商業銀行", "合作金庫銀行", "兆豐國際商業銀行", "第一商業銀行", "臺灣銀行", "玉山商業銀行"])
    return None

if __name__ == "__main__":
    main()