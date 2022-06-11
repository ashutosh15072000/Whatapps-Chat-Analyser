# -*- coding: utf-8 -*-
"""
Created on Thu Jun  9 16:53:11 2022

@author: ayush

"""

import pandas as pd
from wordcloud import WordCloud
from urlextract import URLExtract
from collections import Counter
import emoji as em
extract=URLExtract()
def fetch_stats(selected_user,df):
    
    ### finding the stats
    if selected_user!='Overall':  
        df=df[df['User_name']==selected_user]
       
    total_message=df.shape[0]
    word=[]
    media=df[df['Message']=='<Media omitted>'].shape[0]
    links=[]
    for message in df['Message']:
        links.extend(extract.find_urls(message))
    for i in df['Message']:
        word.extend(i.split())    
    return total_message,len(word),media,len(links)

 ## finding the busiest user in the group
def most_busy_user(df):

    x=df['User_name'].value_counts().head()
    new_df=((df['User_name'].value_counts(normalize=True)*100).round(2))
    x1=pd.DataFrame({'User_Name':new_df.index,'Percent':new_df.values})
    
    return x,x1

def create_wordcloud(selected_user,df):
    f=open('stop_hinglish.txt','r')
    stopwords=f.read()
    if selected_user!='Overall':  
        df=df[df['User_name']==selected_user]
    temp=df[df['User_name']!='Whatapps']
    temp=temp[temp['Message']!='<Media omitted>']
    def remove_stopword(message):
        word1=[]
        for words in message.lower().split():
            if words not in stopwords:
                word1.append(words)
        return ' '.join(word1)
    wc=WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    temp['Message']=temp['Message'].apply(remove_stopword)
    df_wc=wc.generate(temp['Message'].str.cat(sep=' '))
    return df_wc

def most_common_word(selected_user,df):
    
    f=open('stop_hinglish.txt','r')
    stopwords=f.read()
    if selected_user!='Overall':  
        df=df[df['User_name']==selected_user]
    temp=df[df['User_name']!='Whatapps']
    temp=temp[temp['Message']!='<Media omitted>']
    word1=[]
    for message in temp['Message']:
        for words in message.lower().split():
            if words not in stopwords:
                word1.append(words)
    most_common_df=pd.DataFrame(Counter(word1).most_common(25),columns=['Word','Counts'])
    return most_common_df
       
def emoji(selected_user,df):
    if selected_user!='Overall':  
        df=df[df['User_name']==selected_user]
    emoji=[]
    for message in df['Message']:
        emoji.extend([c for c in message if c in em.UNICODE_EMOJI['en']])
    emoji_df=pd.DataFrame(Counter(emoji).most_common(5),columns=['Emoji','Counts'])
    return emoji_df
def monthly_timeline(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['User_name'] == selected_user]

    timeline = df.groupby(['Year','Month']).count()['Message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['Month'][i] + "-" + str(timeline['Year'][i]))

    timeline['Time'] = time

    return timeline    
def Daily_timeline(selected_user,df):
     if selected_user!='Overall':  
        df=df[df['User_name']==selected_user]
     df['only_date']=df['Date'].dt.date
     daily_timeline=df.groupby(['only_date']).count()['Message'].reset_index()
     return daily_timeline
     
    
    
def week_activit(selected_user,df):
     if selected_user!='Overall':  
        df=df[df['User_name']==selected_user]
     weekday=df['Day'].value_counts().reset_index()
     return weekday
 
def month_activit(selected_user,df):
     if selected_user!='Overall':  
        df=df[df['User_name']==selected_user]
     month=df['Month'].value_counts().reset_index()
     return month
def activity_heatmap(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['User_name'] == selected_user]

    user_heatmap = df.pivot_table(index='Day', columns='Periods', values='Message', aggfunc='count').fillna(0)

    return user_heatmap