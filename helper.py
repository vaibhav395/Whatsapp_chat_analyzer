from urlextract import URLExtract
from wordcloud import WordCloud
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

    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    df_wc = wc.generate(df['message'].str.cat(sep=" "))
    return df_wc