#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 16 20:33:34 2017

@author: imhotepisis
"""

import pandas as pd
import os
import time
from datetime import datetime
import re

path = '/Users/imhotepisis/Desktop/stocks'

def Key_Stats(gather='Total Dept/Equity (mrq)'):
    statspath = path + '/_KeyStats'
    stock_list = [x[0] for x in os.walk(statspath)]
    df = pd.DataFrame(columns = ['Date','Units', 'Ticker', 'DE Ratio', 'Price', 'SP500'])
    
    sp500_df = pd.DataFrame.from_csv("S&P-500.csv")
    
    
    
    
    for each_dir in stock_list[1:25]:
        each_file = os.listdir(each_dir)
        ticker = each_dir.split('/')[-1]
        if len(each_file) > 0: 
            for file in each_file:
                
                date_stamp = datetime.strptime(file, '%Y%m%d%H%M%S.html')
                unix_time = time.mktime(date_stamp.timetuple())
#                print(date_stamp, unix_time)
                full_file_path = each_dir+'/'+file
#                print(full_file_path)
                with open(full_file_path, encoding = 'utf-8', mode = 'r') as infile:
                    source = infile.read()
                    try:
                        
                        value = re.findall('\>Total Debt\/Equity \(mrq\)\:\<\/td\>\<td class\=\"yfnc\_tabledata1\"\>(.*?)\<\/td\>',source)
                        stock_price = float(source.split('</small><big><b>')[1].split('</b></big>')[0])


#                        print(stock_price, ticker)
#                        print(date_stamp,unix_time,ticker[-1], value, stock_price)
#                        try:
                        sp500_date = datetime.fromtimestamp(unix_time).strftime('%Y-%m-%d')
                        print(sp500_date)
                        row = sp500_df[(sp500_df.index == sp500_date)]
                        sp500_value = float(row["Close"])
                        print(sp500_value)

                        sp500_date = datetime.fromtimestamp(unix_time-259200).strftime('%M/%d/%Y')
                        row = sp500_df[(sp500_df.index == sp500_date)]
                        sp500_value = float(row['Close'])
                        
                        
                        
                        
                        
                        df = df.append({'Date':date_stamp,
                                        'Unix':unix_time,
                                        'Ticker':ticker,
                                        'DE Ratio':value,
                                        'Price': stock_price,
                                        'SP500': sp500_value}, ignore_index = True)
                    except Exception as e:
                        pass

            
    save = gather.replace(' ','').replace(')','').replace('(','').replace('/','')+('.csv')
    print(save)
    df.to_csv(save)

Key_Stats()