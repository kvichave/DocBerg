from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt


extract = URLExtract()


from urlextract import URLExtract

extract = URLExtract()

def fetch_stats(selected_user, df):
    if selected_user == "Overall":
        num_messages = df.shape[0]
        words = []
        for message in df['message']:
            words.extend(message.split())
        media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]
        links = []
        for message in df['message']:
            links.extend(extract.find_urls(message))
        
        return num_messages, len(words),media_messages,len(links)

    elif selected_user != "Overall":
        new_df = df[df['user'] == selected_user]
        num_messages = new_df.shape[0]
        words = []
        for message in df['message']:
            words.extend(message.split())
        media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]
        links = []
        for message in df['message']:
            links.extend(extract.find_urls(message))
        
        return num_messages, len(words),media_messages,len(links)

def fetch_busy_users(df):
    x = df['user'].value_counts().head()
    neww_df = round(((df['user'].value_counts() / df.shape[0])) * 100, 2).reset_index().rename(
        columns={'user': 'name', 'index': 'percent'})
    # Convert 'name' and 'percent' columns to dictionary
    user_contro_percent_dict = dict(zip(neww_df['name'], neww_df['count']))
  
    return x,user_contro_percent_dict


def create_wordcloud(selected_user, df):
  #  f = open('stop_hinglish.txt', 'r')
  #  stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

   # def remove_stop_words(message):
       # y = []
        #for word in message.lower().split():
            #if word not in stop_words:
               #y.append(word)
       # return " ".join(y)

    wc = WordCloud(width=800, height=400, min_font_size=10, background_color='white')
   # temp['message'] = temp['message'].apply(remove_stop_words)
    df_wc = wc.generate(temp['message'].str.cat(sep=" "))
    return df_wc


def most_common_words(selected_user, df):
   # f = open('stop_hinglish.txt', 'r')
   # stop_words = f.read()
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']
    words = []
    for message in temp['message']:
       for word in message.lower().split():
         #   if word not in stop_words:
                words.append(word)
    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df



def monthly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time
    return timeline

def daily_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    daily_timeline = df.groupby('only_date').count()['message'].reset_index()

    return daily_timeline




def week_activity_map(selected_user, df):
    print(f"Selected User: {selected_user}")

    if selected_user != 'Overall':
        df_user = df[df['user'] == selected_user]
        print(f"Filtered DataFrame for {selected_user}:\n{df_user}")
    else:
        df_user = df

    activity_counts = df_user['day_name'].value_counts()
    print("Activity Counts by Day:", activity_counts)

    return activity_counts

def month_activity_map(selected_user, df):
    print(f"Selected User: {selected_user}")

    if selected_user != 'Overall':
        df_user = df[df['user'] == selected_user]
        print(f"Filtered DataFrame for {selected_user}:\n{df_user}")
    else:
        df_user = df

    month_counts = df_user['month'].value_counts()
    print("Month Counts:", month_counts)

    return month_counts





