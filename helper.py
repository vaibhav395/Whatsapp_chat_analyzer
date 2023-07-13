from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import pandas as pd
extract = URLExtract()
def fetch_stats(selected_users , df):
    if selected_users != 'Overall':
        df = df[df['users'] == selected_users]

    #1. fetch number of messages
    num_messages = df.shape[0]

    #2. fetch total number of words
    words = []
    for messages in df['message']:
        words.extend(messages.split())

    #3. fetch media messages
    number_of_media = df[df['message'] == '<Media omitted>\n'].shape[0]

    #4. fetch all the links shared
    links = []
    for messages in df['message']:
        links.extend(extract.find_urls(messages))

    return num_messages, len(words), number_of_media, len(links)

def most_active_users(df):
    x = df['users'].value_counts().head()
    df = round((df['users'].value_counts()/df.shape[0])*100, 2).reset_index().rename(columns={'index': 'name', 'user': 'percent'})
    return x, df

def create_wordcloud(selected_users, df):
    if selected_users != 'Overall':
        df = df[df['users'] == selected_users]

    temp = df[df['users'] != 'notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc

def most_common_words(selected_users, df):
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    if selected_users != 'Overall':
        df = df[df['users'] == selected_users]
    temp = df[df['users'] != 'notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    words = []
    for messages in temp['message']:
        for word in messages.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df

def monthly_timeline(selected_users, df):
    if selected_users != 'Overall':
        df = df[df['users'] == selected_users]

    timeline = df.groupby(['year', 'month', 'month_num']).count()['message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))
    timeline['time'] = time

    return timeline

def daily_timeline(selected_users, df):
    if selected_users != 'Overall':
        df = df[df['users'] == selected_users]
    daily_timeline = df.groupby('only_date').count()['message'].reset_index()
    return daily_timeline

def week_activity_map(selected_users, df):
    if selected_users != 'Overall':
        df = df[df['users'] == selected_users]

    return df['day_name'].value_counts()

def month_activity_map(selected_users, df):
    if selected_users != 'Overall':
        df = df[df['users'] == selected_users]

    return df['month'].value_counts()

def activity_heatmap(selected_users, df):
    if selected_users != 'Overall':
        df = df[df['users'] == selected_users]
    user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)
    return user_heatmap

