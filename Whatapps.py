# -*- coding: utf-8 -*-
"""
Created on Thu Jun  9 16:42:11 2022

@author: ayush
"""

import streamlit as st
import preprocessors
import helper
from matplotlib import pyplot as plt
import seaborn as sns

st.sidebar.title('Whatapps Analyser')
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
     # To read file as bytes:
     bytes_data = uploaded_file.getvalue()
     data=bytes_data.decode("utf-8")
     df=preprocessors.preprocess(data)
     name=df['User_name'].unique().tolist()
     name.sort()
     name.insert(0,'Overall')
     selected_user = st.sidebar.selectbox('Show Analaysis Wrt?',name)
     if st.sidebar.button('Show Analysis'):
         total_message,words,media,links=helper.fetch_stats(selected_user, df)
         st.title('Top Statistics')
         col1,col2,col3,col4 = st.columns(4)
         with col1:
             st.header('Total  Message')
             st.title(total_message)
         with col2:
             st.header('Total    Words')
             st.title(words)
         with col3:
             st.header('Media Shared')
             st.title(media)
         with col4:
             st.header('Links Shared')
             st.title(links)  
             
     ### monthly timeline
             
     timeline=helper.monthly_timeline(selected_user,df)
     st.title('Monthly Timeline')
     fig,ax=plt.subplots()
     ax.plot(timeline['Time'],timeline['Message'])
     plt.xticks(rotation='90')
     st.pyplot(fig)
     
     ##### daily timeline
     daily_timeline=helper.Daily_timeline(selected_user, df)
     st.title('Daily Timeline')
     fig,ax=plt.subplots()
     ax.plot(daily_timeline['only_date'],daily_timeline['Message'],color='black')
     plt.xticks(rotation='90')
     st.pyplot(fig)
     
     
     #### week day
     st.title('Activity Map')
     weekday=helper.week_activit(selected_user, df)
     month=helper.month_activit(selected_user, df)
  
     
     
     col1,col2=st.columns(2)
 
     with col1:
         
         st.header('Most Busy Day')
      
         fig,ax=plt.subplots()
         ax.bar(weekday['index'],weekday['Day'])
         plt.xticks(rotation='90')
         st.pyplot(fig,width=10000)
         
      
     with col2:
         st.header('Most Busy Month') 
         fig,ax=plt.subplots()
         ax.bar(month['index'],month['Month'],color='orange')
         plt.xticks(rotation='90')
         st.pyplot(fig)
    
                  

     st.title("Weekly Activity Map")
     user_heatmap = helper.activity_heatmap(selected_user,df)
     fig,ax = plt.subplots()
     ax = sns.heatmap(user_heatmap)
     st.pyplot(fig)
     s = user_heatmap.unstack()
     so = s.sort_values(kind="quicksort",ascending=False)
     so=so[:2].reset_index()
     st.write('Most of time is online at',so['Periods'][0],'PM and ',so['Periods'][1],'PM', 'and day is ',so['Day'][0],'and',so['Day'][1])
    
     
    
    
    
    
    
     if selected_user=='Overall':
         st.title('Most Busy User')
         x,new_df=helper.most_busy_user(df)
         fig,ax=plt.subplots()
         ax.grid(b = True, color ='grey',linestyle ='-.', linewidth = 1,alpha = 0.2)
         col1,col2=st.columns(2)
         with col1:
             ax.bar(x.index,x.values,color='red')
             plt.xticks(rotation='vertical')
             st.pyplot(fig)
         with col2:    
              st.dataframe(new_df)
      ## word cloud
     st.header('WordCloud')
     df_wc=helper.create_wordcloud(selected_user, df)      
     fig,ax=plt.subplots()
     ax.imshow(df_wc)
     st.pyplot(fig)
     ## most commom word
     
     st.header('Most Common Words')
     fig,ax=plt.subplots()
     most_common_word=helper.most_common_word(selected_user, df)
     ax.bar(most_common_word['Word'],most_common_word['Counts'],color='#4CAF50')
     plt.xticks(rotation='vertical')
     st.pyplot(fig)
     
     ### emoji Analysis
     emoji_df=helper.emoji(selected_user,df)
     st.header('Emoji Analysis')
     col1,col2 = st.columns(2)

     with col1:
         st.dataframe(emoji_df)
     with col2:
         fig,ax = plt.subplots()
         ax.bar(emoji_df['Emoji'],emoji_df['Counts'])
         st.pyplot(fig)