import streamlit as st
import pandas as pd
from preprocessor import preprocessor
import helper
from urlextract import URLExtract
import matplotlib.pyplot as plt
from helper import most_busy_users
import seaborn as sns


st.set_page_config(page_title="WhatsApp Chat Analysis", page_icon=":bar_chart:", layout="wide")
st.sidebar.title("WhatsApp Chat Analysis")
st.title(f"WhatsApp Chat Analysis Report")


uploaded_file = st.sidebar.file_uploader("Upload Chat file", type="txt")

if uploaded_file is not None:
    byte_data = uploaded_file.getvalue()
    data = byte_data.decode("utf-8")
    df = preprocessor(data)
    
    # Setup drop down for the selecte users
    users = df['user'].unique().tolist()
    users.remove('group_notification')
    users.sort()
    users.insert(0, "Overall")
    
    selected_user = st.sidebar.selectbox("Select User", users)
    
    if st.sidebar.button("Show Analysis"):
        st.title("Statistics")
        c1, c2, c3, c4 = st.columns(4)

        num_messages, num_words, num_media, links = helper.fetch_stats(selected_user, df)
        with c1:
            st.subheader("Total Messages")
            st.title(num_messages)
        
        with c2:
            st.subheader("Total Words")
            st.title(num_words)
            
        with c3:
            st.subheader("Media Shared")
            st.title(num_media)
        
        with c4:
            st.subheader("Links Shared")
            st.title(len(links))
        
        # timeline
        st.title("Monthly Timeline")
        timeline = helper.get_monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'], color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
        
        st.title("Daily Timeline")
        daily_timeline = helper.get_daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['date'], daily_timeline['message'], color='red')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # Activity map
        col1, col2 = st.columns(2)
        
        with col1:
            # Weekly activity map
            st.title("Weekly Activity Map")
            weekly_activity = helper.weekly_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(weekly_activity.index, weekly_activity.values, color='blue')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
            
        with col2:
            # Monthly activity map
            st.title("Monthly Activity Map")
            monthly_activity = helper.monthly_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(monthly_activity.index, monthly_activity.values, color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        
        # User heatmap
        st.title("User Heatmap")
        user_heatmap = helper.user_heatmap(selected_user, df)
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.heatmap(df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count'), annot=True, cmap='Blues')
        plt.yticks(rotation='horizontal')
        st.pyplot(fig)

        # Most busy users
        if selected_user == "Overall":
            st.title("Most Busy Users")
            x, y = most_busy_users(df)
            fig, ax = plt.subplots()
        
            col1, col2 = st.columns(2)
            
            with col1:
                ax.bar(x.index, x.values, color='orange')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(y)
        
        st.title("Word Cloud")
        
        # return wordcloud image
        word_cloud = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(word_cloud)
        st.pyplot(fig)

        st.title("Most Common Words")
        mcw = helper.most_common_words(selected_user, df)
        fig, ax = plt.subplots()
        ax.barh(mcw[0], mcw[1], color='purple')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
        
        st.title("Emoji Analysis")
        col1, col2 = st.columns(2)
        
        emoji_df = helper.get_emojis(selected_user, df)
        
        with col1:
            st.dataframe(emoji_df)
            
        with col2:
            fig, ax = plt.subplots()
            ax.pie(emoji_df['Count'], labels=emoji_df['Emoji'], autopct='%1.1f%%', startangle=140)
            ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
            st.pyplot(fig)
    