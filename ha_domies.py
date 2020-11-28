"""
@timsmaluk
Python script to collect all messages from Ha_Domies.
Objective is to clean, format, and prepare the data
for analysis, and visualization
"""

import plotly.express as px
import plotly.graph_objects as go
import datetime
import emoji
import grapheme
import re
import pandas as pd
import numpy as np

dates = []
messages = []
log_dictionary = {'Dates': '', 'Messages': messages}
date_time_pattern = re.compile(r'(\[.*\])')


def get_chathistory():
    """
    Loads txt file
    :param 
    :return: (list) of chat logs
    """
    with open("/Users/Tim_Smaluk/Desktop/shit/christmas_present/_chat.txt", 'r', encoding='utf-8') as file:
        return file.readlines()

def extract_emojis(str):
  return ' '.join(c for c in str if c in emoji.UNICODE_EMOJI)


def prepare_for_pandas(chat_history):
    """
    Cleans up my name to discard alais, splits dates and name/message into seperete lists
    :param chat_history         (txt file): (list) of chat logs
    :return messages, dates:    (list) of messages and dates respectively
    """
    for line in chat_history:  
        if 'Tim Aka Professor Snowangel 🇷🇺🥦🥦 Smaluk' in line:
            line = line.replace('Tim Aka Professor Snowangel 🇷🇺🥦🥦 Smaluk', 'Tim Smaluk:')
        result = date_time_pattern.match(line)
        if 'Ethan  Lipsker' in line:
            line = line.replace('Ethan  Lipsker', 'Ethan Lipsker:')
        if 'Mohit:' in line:
            line = line.replace('Mohit:', 'Mohit Veligenti:')
        if '\u202a+1\xa0(925)\xa0699‑5459\u202c:' in line:
            line = line.replace('\u202a+1\xa0(925)\xa0699‑5459\u202c:', 'Zac Pinard:')
        if result is not None:
            dates.append(result.group())
            # print(result.group())
            # print(line.split(result.group()))
            messages.append(line.split(result.group()))
    log_dictionary['Dates'] = dates
    log_dictionary['Messages'] = messages
    return log_dictionary


def clean_pandas_df(data):
    """
    Creates a Pandas Dataframe to prepare data for analysis
    :param  (dictionary): Dates(includes Time) and Messages(Includes Alias)
    :return (DataFrame): orgonized chat log into 4 columns(Date, Time, Alias, Messages)
    """
    ha_domies_df = pd.DataFrame(data)
    ha_domies_df = ha_domies_df.drop([0, 1, 2], axis=0) 
    
    ha_domies_df[['Date', 'Time']] = ha_domies_df.Dates.str.split(",", expand=True)
    ha_domies_df['Date'] = ha_domies_df.Date.str.lstrip('[')
    
    ha_domies_df['Time'] = ha_domies_df.Time.str.rstrip(']')
    
    ha_domies_df['Names'] = ha_domies_df.Messages.str[1]
    ha_domies_df['Names'] = ha_domies_df.Names.str.extract(('([A-Z][a-z]+\s[A-Z][a-z]+:)'))
    ha_domies_df['Names'] = ha_domies_df.Names.str.replace(':', "")

    ha_domies_df['Messages'] = ha_domies_df.Messages.str[1]
    ha_domies_df['Messages'] = ha_domies_df.Messages.str.split(':', 1,  expand=True)[1]
    ha_domies_df['Messages'] = ha_domies_df.Messages.astype(str).str.replace("\n","").replace("\t","")

    ha_domies_df.drop(columns='Dates')
    ha_domies_df = ha_domies_df.dropna()

    ha_domies_df = ha_domies_df.reset_index(drop=True)
    
    ha_domies_df.at[15316, 'Time'] = '2:08:09 PM'
    ha_domies_df.at[15316, 'Names'] = 'Dustin Bradley'
    ha_domies_df.at[15316, 'Messages'] = '[Lunar eclipse]@19258955572' 

    ha_domies_df.at[15317, 'Time'] = '2:19:07 PM'
    ha_domies_df.at[15317, 'Names'] = 'Owen Gilbert'
    ha_domies_df.at[15317, 'Messages'] = '[Solar eclipse]@19257847841'

    ha_domies_df.at[19915 ,'Time'] = '2:21:08 PM'
    ha_domies_df.at[19915 ,'Names'] = 'Mohit Veligenti'
    ha_domies_df.at[19915 ,'Messages'] = '[Developing Story] XXXTentacion might be dead? https://www.reddit.com/r/hiphopheads/comments/8s2mxk/' 

    ha_domies_df['Alias'] = ha_domies_df.Names.apply(lambda x: x.split()[0])
    ha_domies_df = ha_domies_df[['Date', 'Time', 'Alias', 'Messages']]
    return ha_domies_df


def basic_analysis(df):
    """
    Collect basic statistics such as # of messages, # of members,
    total # of words, longest messsage length, longest message holder
    :param  (Dataframe): Takes in dataframe from clean_pandas_df
    :return (): stats from above
    """
    number_members = len(df['Alias'].unique())
    number_messages = len(df['Messages'])
    
    msg_lengths = df.Messages.map(lambda x: len(x))
    msg_lengths_2 = df.Messages.map(lambda x: len(x.split(" ")))
    # print(list(msg_lengths.nlargest(10).values))
    # print(msg_lengths_2.nlargest())
    # print(df.loc[[36815, 27129, 14993, 36816, 16172]])

    longest_message = df.Messages.map(lambda x: len(x.split(" "))).max()
    
    # total_words = df.Messages.map(lambda x: len(x.split(" "))).sum()
    # longest_message_index = df.Messages.apply(lambda x: len(x) == 2090)
    # longest_message_holder = df.loc[27130, 'Alias']
    # longest_message_length = 2090
    #print(total_words)
    #print(number_messages, number_members, total_words, longest_message_holder, longest_message_length)


def emoji_stats(df):
    """
    Plots # of emojis used by each member in the group.
    :df     (dataframe)
    :return (none)
    """
    for row in df['Messages']:
        for x in row:
            if x in emoji.UNICODE_EMOJI:
                print(x)
    df['Emojis'] = df['Messages'].apply(lambda x: [c for c in x if x in emoji.UNICODE_EMOJI])
    print(df['Emojis'])
    emoji_df = df[df['Emojis'].apply(lambda x: True if x else False)]
    #print(emoji_df)
    emoji_dict = {alias: {emoji: 0 for emoji in emoji.UNICODE_EMOJI.keys()} for alias in emoji_df.Alias}
    #print(emoji_dict)
    # for name, emotes in zip(df['Alias'], df['Emojis']):
    #     for emote in emotes:
    #         if emote is not '':
                

    #print(emoji_frq)
    #print(emoji_frq['Emojis'].value_counts())
    # emojis_by_name = emoji_frq.groupby(['Alias', 'Emojis']).agg(lambda x: x.value_counts().index[0])
    # #print(emojis_by_name)
    # df['# of Emojis'] = np.array(num_emojis)
    # emoji_df = df.groupby('Alias').sum()[['# of Emojis']].sort_values(by=['# of Emojis'])
    # emoji_df = emoji_df.reset_index()
    # fig = px.bar(emoji_df, x='# of Emojis', y='Alias', orientation='h')
    # #fig.show()

def get_day_of_the_week(df):
    """
    Gets day of the week from input of Date (xx/xx/xx)
    :param  (dataframe): 
    :return (dataframe): Includes day of the week
    """
    days = []
    years = []
    month_name = []
    weekDays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    months   = ['Jan', 'Feb', 'March', 'Apr', 'May', 'June', 'July', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec']
    for day in df.Date:
        dates = day.split('/')
        year = "20" + dates[2]
        day = dates[1]
        month = dates[0]
        day_of_the_week = datetime.date(int(year), int(month), int(day))
        years.append(year)
        month_name.append(months[int(month)-1])
        days.append(weekDays[day_of_the_week.weekday()])
    correct_time = []
    for time in df.Time:
        if len(time) == 11:
            time = time[0:5] + time[8:]
            correct_time.append(time)
        else:
            time = time[0:6] + time[9:]
            correct_time.append(time)
    df['Redacted Time'] = np.array(correct_time)
    df['Year'] = np.array(years)
    df['Month'] = np.array(month_name)
    df['Day'] = np.array(days)
    return df


def freq_msg_day(df_1):
    """
    Plots the graph of frequency of messages for every day of the week
    :param (dataframe)
    :return (plotly graph)
    """
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    day_dict = {num : 0 for num in days}  # fills dictionary values with 0
    for day in days:
        if day in day_dict.keys():
            day_dict[day] = df_1.Day.str.count(day).sum()  # counts the sum of each day occruence
    freq = list(day_dict.values())
    days = list(day_dict.keys())
    fig = go.Figure(go.Line(x=days, y=freq))
    #fig.update_layout(title='Frequency of Messages per Day', xaxis='Day of the Week', yaxis='# of Messages')
    fig.show()


def freq_msg_month(df_1):
    """
    Plots the graph of frequency of messages for every month of the year
    :param (dataframe)
    :return (plotly graph)
    """   
    months = df_1.Month.unique()
    month_dict = {num: 0 for num in months}
    for month in months:
        if month in month_dict.keys():
            month_dict[month] = df_1.Month.str.count(month).sum()
    freq = list(month_dict.values())
    months = list(month_dict.keys())
    fig = go.Figure(go.Line(x=months, y=freq))
    fig.show()


def freq_msg_year(df_1):
    """
    Plots the graph of frequency of messages for every month of the year
    :param (dataframe)
    :return (plotly graph)
    """
    years = df_1.Year.unique()
    year_dict = {num: 0 for num in years}
    for year in years:
        if year in year_dict.keys():
            year_dict[year] = df_1.Year.str.count(year).sum()
    freq = list(year_dict.values())
    years = list(year_dict.keys())
    fig = go.Figure(go.Line(x=years, y=freq))
    fig.show()

def msg_over_all_time(df):
    df['Count'] = 1
    date_count = df.groupby(['Date'])['Count'].sum()
    date_sum = date_count.to_frame()
    date_sum = date_sum.reset_index()
    date_sum['Date'] = pd.to_datetime(date_sum.Date)
    date_sum.sort_values(by='Date', inplace=True)
    #print(date_sum)
    d = date_sum['Date'].tolist()
    c = date_sum['Count'].tolist()
    fig = go.Figure(go.Line(x=d, y=c))
    fig.show()

def avg_msg_length(df):
    df['Msg Length'] = df.Messages.apply(lambda x: len(x))
    avg_msg_length = df.groupby('Alias').mean().reset_index().sort_values(by='Msg Length', ascending=False)
    #print(avg_msg_length)
    name = avg_msg_length['Alias'].tolist()
    avg = avg_msg_length['Msg Length'].tolist()
    fig = px.bar(avg_msg_length, x="Alias", y="Msg Length", title="Average Message Length by Person", color="Msg Length")
    fig.show()


if __name__ == '__main__':  
    chat_history = get_chathistory()
    data = prepare_for_pandas(chat_history)
    df = clean_pandas_df(data)

    #df_1 = get_day_of_the_week(df)
    #print(df_1)
    #print(freq_msg_day(df))
    #print(freq_msg_year(df_1))
    #print(freq_msg_month(df_1))
    
    #print(df.Date)
    #basic_analysis(df)
    emoji_stats(df)
    #msg_over_all_time(df)
    #avg_msg_length(df)

