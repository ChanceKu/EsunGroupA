import csv
import pandas as pd
from datetime import datetime
import os
import subprocess
import matplotlib.pyplot as plt

dir_list = os.listdir(dir)
plt.rcParams['font.sans-serif'] = ['Taipei Sans TC Beta']
dir = ".//csv"
for i in dir_list:
    print(i)
    csv_name, extension = os.path.splitext(i)
    df = pd.read_csv(dir +"//" +i, encoding="utf-8")