# https://matplotlib.org/stable/gallery/pie_and_polar_charts/pie_features.html

def store(data, path = ".//df_csv"):
    import os
    import pandas as pd

    # create folder if path does not exist
    if not os.path.exists(path):
        os.makedirs(path)

    # 把ratio_dict中的每個dataframe寫成"key.csv"
    for key, value in data.items():
        file_name = key + ".csv"
        value.to_csv(os.path.join(".//df_csv//", file_name), encoding='utf-8', index=True)

def plotdir(dir_path='.//df_csv',delete=False):
    import csv
    import pandas as pd
    from datetime import datetime
    import os
    import subprocess

    # Use the subprocess module to run pip commands
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        subprocess.check_call(["python", '-m', 'pip', 'install', 'matplotlib'])
        import matplotlib.pyplot as plt

    # 更改plt的font
    plt.rcParams['font.sans-serif'] = ['Taipei Sans TC Beta']

    # 取得csv資料夾內的檔案
    dir_list = os.listdir(dir_path)
    fail_list=[]
    success_list=[]

    # 迴圈打開csv並生成plot.png
    for file in dir_list:
        if file.endswith(".csv"):
            try:
                df = pd.read_csv(os.path.join(dir_path, file), encoding="utf-8")
                
                #取得市占率
                share = [] # market share
                for i in range(13):
                    value = df.iloc[29, 14+2*i]
                    share.append(value)
                
                #取得排名
                rank = []   # market ranking
                for i in range(13):
                    value = df.iloc[29, 15+2*i]
                    rank.append(value)

                #取得月份
                month = []
                for i in df.columns[1:14]:
                    month.append(i)

                # 把月份格式更改, 例:2022年01月 -> 2022/01
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
                ax1.set_ylabel('市占率', color=color)     #中文可能會亂碼, to be fixed
                ax1.plot(new_month, share, color=color, marker='o')
                ax1.tick_params(axis='y', labelcolor=color)

                # Plot the second dataset (rank) on the right y-axis
                ax2 = ax1.twinx()  # Create a second y-axis that shares the same x-axis
                color = 'tab:blue'
                ax2.set_ylabel('排名', color=color)      #中文可能會亂碼, to be fixed
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
                success_list.append(file)
                plt.close()
            except:
                fail_list.append(file)
                pass

    print("成功:", success_list) 

    # 若fail_list不是空的則print
    if fail_list:
        print("失敗:", fail_list)

    #如果delete == True則圖表跑完後刪除csv資料夾
    if delete == True:
        import shutil
        shutil.rmtree(dir_path)

def plotcsv(csv_path='.//df_csv', delete = False):
    # import module
    import csv
    import pandas as pd
    from datetime import datetime
    import os
    import subprocess

    # Use the subprocess module to run pip commands
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        subprocess.check_call(["python", '-m', 'pip', 'install', 'matplotlib'])
        import matplotlib.pyplot as plt
    
    df = pd.read_csv(csv_path, encoding="utf-8")
    
    #取得市占率
    share = [] # market share
    for i in range(13):
        value = df.iloc[29, 14+2*i]
        share.append(value)
    
    #取得排名
    rank = []   # market ranking
    for i in range(13):
        value = df.iloc[29, 15+2*i]
        rank.append(value)

    #取得月份
    month = []
    for i in df.columns[1:14]:
        month.append(i)

    # 把月份格式更改, 例:2022年01月 -> 2022/01
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
    ax1.set_ylabel('市占率', color=color)     #中文可能會亂碼, to be fixed
    ax1.plot(new_month, share, color=color, marker='o')
    ax1.tick_params(axis='y', labelcolor=color)

    # Plot the second dataset (rank) on the right y-axis
    ax2 = ax1.twinx()  # Create a second y-axis that shares the same x-axis
    color = 'tab:blue'
    ax2.set_ylabel('排名', color=color)      #中文可能會亂碼, to be fixed
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
    plt.close()

    #如果delete == True則圖表跑完後刪除csv資料夾
    if delete == True:
        import shutil
        shutil.rmtree(csv_path)

def getrow(path, row):
    getrow_new_row = iloc[row]
    return getrow_new_row

def main():
    return None

if __name__ = "__main__":
    main()