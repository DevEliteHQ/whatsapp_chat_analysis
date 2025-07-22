from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import pandas as pd
import emoji

def fetch_stats(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]
    
    # fetch the number of messages
    num_messages = df.shape[0]
    
    # Number of words
    words = []
    
    for message in df['message']:
        words.extend(message.split(' '))
    
    num_words = len(words)
    
    # Number of media items - using exact match as it's more reliable
    num_media = df[df['message'] == '<Media omitted>'].shape[0]

    links = []
    extractor = URLExtract()

    for message in df['message']:
        urls = extractor.find_urls(message)
        links.extend(urls)

    return num_messages, num_words, num_media, links


def most_busy_users(df):
    per_df = round((df['user'].value_counts().head(5) / df.shape[0]) * 100, 2).reset_index(name='percentage')
    busy_user_df = df['user'].value_counts()
    return busy_user_df, per_df

def create_wordcloud(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]
    
    # Top words used in chatting

    # Remove the ommitted media
    # Remove group_notifications message

    # Remove StopWords
    # import stop words
    stop_words = open('stop_hinglish.txt', 'r').read().split('\n')
    
    def remove_stopwords(message):
        words = []
        for w in message.lower().split(' '):
            if w not in stop_words:
                words.append(w)
        return " ".join(words)

    # Remove group Notifications

    new_df = df[df['user'] != 'group_notification']
    new_df = new_df[new_df['message'] != '<Media omitted>']
    new_df['message'] = new_df['message'].apply(remove_stopwords)
    
    
    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    df_wc = wc.generate(new_df['message'].str.cat(sep=" "))
    return df_wc

def most_common_words(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]
    
    # Top words used in chatting

    # Remove the ommitted media
    # Remove group_notifications message

    # Remove StopWords
    # import stop words
    stop_words = open('stop_hinglish.txt', 'r').read().split('\n')
    words = []

    # Remove group Notifications

    new_df = df[df['user'] != 'group_notification']
    new_df = new_df[new_df['message'] != '<Media omitted>']

    for message in new_df['message']:
        for w in message.lower().split(' '):
            if w not in stop_words:
                words.append(w)

    count = Counter(words)
    mcw = pd.DataFrame(count.most_common(20))
    
    return mcw

def get_emojis(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    emojis = []

    for message in df['message']:
        emojis.extend(emoji.distinct_emoji_list(message))

    count_emojis = Counter(emojis)
    column_name = ['Emoji', 'Count']
    emoji_df = pd.DataFrame(count_emojis.most_common(20), columns=column_name)

    return emoji_df.head(5)

def get_monthly_timeline(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]
    
    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(f"{timeline['month'][i]}-{timeline['year'][i]}")
    timeline['time'] = time
    
    return timeline

def get_daily_timeline(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]
    
    daily_timeline = df.groupby('date').count()['message'].reset_index()
    return daily_timeline

def weekly_activity_map(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()

def monthly_activity_map(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()

def user_heatmap(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    return df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count')