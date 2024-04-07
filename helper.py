import dataclasses
import tempfile
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from wordcloud import STOPWORDS, WordCloud
from collections import Counter
import emoji


from urlextract import URLExtract
extract = URLExtract()
def fetch_stats(selected_user, data):
 # if its a specific user in that case we are changing 'data' (by data meaning adjusting the toggle via names) otherwise keeping 'data' the same
 # if selected user is not 'Overall' meaning its a specific user 
    # 1st step is that we are fetching number of messages
    # 2nd step is we are fetching number of words
    if selected_user != 'Overall':
       data = data[data['user'].str.contains(selected_user, case=False)]
 # In data, we have to find the specific user's number of messages with total len(words)
    num_messages = data.shape[0]

    words= []
    for message in data['message']:
      words.extend(message.split())
    
    # 3rd step fetch number of media messages
      num_media_msg = data[data['message'].str.contains('omitted')].shape[0]

    # fetch number of links shared
    links = []
    for message in data['message']:
       links.extend(extract.find_urls(message))
         

    return num_messages, len(words), num_media_msg, len(links)


    # if selected_user == 'Overall':

    # # 1st step is that we are fetching number of messages
    #     num_messages = data.shape[0]
    # # 2nd step is we are fetching number of words
    #     words= []
    #     for message in data['message']:
    #       words.extend(message.split())

    #     return num_messages, len(words)
    
    # else:
    #     # this is for the number of messages but with a specific user name the we need total messages sent by that user with the word length
    #     new_data = data[data['user'].str.contains(selected_user, case=False)] 
    #     num_messages = new_data.shape[0]
    #     # here it is for the total number of words
    #     words= []
    #     for message in new_data['message']:
    #       words.extend(message.split())

    #     return num_messages, len(words)

def most_busy_users(data):
   x = data['user'].value_counts().head()
   data = round((data['user'].value_counts()/data.shape[0])* 100,2).reset_index().rename(columns={'user':'name', 'count':'percent'})
   return x, data

def create_wordcloud(selected_user,data):
   # if selected_user != 'Overall': # if overall then it will be as it is otherwise if its a particular user data will change as per data
   #     data = data[data['user'].str.contains(selected_user, case=False)]
       # Open the stop words file and read its contents
       with open('stop_hinglish.txt', 'r') as f:
        stop_words = f.read().splitlines()

       if selected_user != 'Overall':
        data = data[data['user'] == selected_user]

    # Filter out 'group_notification' and '<omitted>' messages
       temp = data[(data['user'] != 'group_notification') & (data['message'] != '<omitted>\n')]

       def remove_stop_words(message):
          y = []
          for word in message.lower().split():
             if word not in stop_words:
                y.append(word)
          return " ".join(y)


       wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
       temp['message'] = temp['message'].apply(remove_stop_words)
       data_wc = wc.generate(temp['message'].str.cat(sep=" "))
       return data_wc

   

def most_common_words(selected_user, data):
    # Open the stop words file and read its contents
    with open('stop_hinglish.txt', 'r') as f:
        stop_words = f.read().splitlines()

    if selected_user != 'Overall':
        data = data[data['user'] == selected_user]

    # Filter out 'group_notification' and '<omitted>' messages
    temp = data[(data['user'] != 'group_notification') & (data['message'] != '<omitted>\n')]


    words = []
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    # Create DataFrame with word frequencies
    most_common_data = pd.DataFrame(Counter(words).most_common(20), columns=['Word', 'Frequency'])
    return most_common_data


def emoji_helper(selected_user, data):
    if selected_user != 'Overall':
        data = data[data['user'] == selected_user]

    emojis = []
    for message in data['message']:
        for character in message:
            if emoji.is_emoji(character):
                emojis.append(character)

    emoji_counts = Counter(emojis)
    emoji_data = pd.DataFrame(emoji_counts.most_common(), columns=['Emoji', 'Count'])
    return emoji_data

def monthly_timeline(selected_user, data):
    if selected_user != 'Overall':
        data = data[data['user'] == selected_user]
    timeline = data.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))
    
    # Assign the 'time' list to the 'time' column outside the loop
    timeline['time'] = time
    
    return timeline
def daily_timeline(selected_user,data):
    if selected_user != 'Overall':
        data = data[data['user'] == selected_user]

    daily_timeline = data.groupby('only_date').count()['message'].reset_index()

    return daily_timeline

def weekly_activity_map(selected_user,data):
    if selected_user != 'Overall':
        data = data[data['user'] == selected_user]

    return data['day_name'].value_counts()

def month_activity_map(selected_user,data):
    if selected_user != 'Overall':
        data = data[data['user'] == selected_user]

    return data['month'].value_counts()

def activity_heatmap(selected_user, data):
    if selected_user != 'Overall':
        data = data[data['user'] == selected_user]
    user_heatmap = data.pivot_table(index= 'day_name', columns= 'period', values= 'message', aggfunc='count').fillna(0)
    
    return user_heatmap

    





