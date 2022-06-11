# -*- coding: utf-8 -*-
"""
Created on Thu Jun  9 16:50:58 2022

@author: ayush

"""
import re
import pandas as pd

def preprocess(file):
    pattern='\d{1,2}/\d{1,2}/\d{1,2},\s\d{1,2}:\d{1,2}\s\w{2}'
    pattern1='\d{1,2}/\d{1,2}/\d{1,2},\s\d{1,2}:\d{1,2}\s\w{2}\s-\s'
    Dates=re.findall(pattern,file)
    message=re.split(pattern1,file)[1:]
    df=pd.DataFrame({'Date':Dates,'Message':message})
    user_name=[]
    messages=[]
    for i in df['Message']:
        message=re.split(':\s',i)
        if len(message)==1:
                user_name.append('Whatapps')
                messages.append(message[0].strip('\n'))
        else:
                user_name.append(message[0])
                messages.append(message[1].strip('\n'))
    df['User_name']=user_name
    df['Message']=messages
    df['Date']=pd.to_datetime(df['Date'])
    second=[]
    minute=[]
    date=[]
    for i in pd.to_datetime(df['Date']):
        minute.append(i.time().hour)
        second.append(i.time().minute)
    df['Hour']=minute 
    df['Minute']=second
    df['Year']=df['Date'].dt.year
    df['Month']=df['Date'].dt.month_name()
    df['Day']=df['Date'].dt.day_name()
    period = []
    for hour in df[['Day', 'Hour']]['Hour']:
            if hour == 23:
                period.append(str(hour) + "-" + str('00'))
            elif hour == 0:
                period.append(str('00') + "-" + str(hour + 1))
            else:
                period.append(str(hour) + "-" + str(hour + 1))
    
    df['Periods']=period
    
    return df