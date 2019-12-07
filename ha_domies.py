"""
@timsmaluk
Python script to collect all messages from Ha_Domies.
Objective is to clean, format, and prepare the data
for analysis, and visualization
"""

import plotly.express as px
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
    with open("_chat.txt", 'r', encoding='utf-8') as file:
        return file.readlines()

def extract_emojis(str):
  return ''.join(c for c in str if c in emoji.UNICODE_EMOJI)

def prepare_for_pandas(chat_history):
    """
    Cleans up my name to discard alais, splits dates and name/message into seperete lists
    :param chat_history         (txt file): (list) of chat logs
    :return messages, dates:    (list) of messages and dates respectively
    """
    for line in chat_history:  
        if 'Tim Aka Professor Snowangel 🇷🇺🥦🥦 Smaluk' in line:
            line = line.replace('Tim Aka Professor Snowangel 🇷🇺🥦🥦 Smaluk', 'Tim Smaluk')
        result = date_time_pattern.match(line)
        if 'Ethan  Lipsker' in line:
            line = line.replace('Ethan  Lipsker', 'Ethan Lipsker')
        if result is not None:
            dates.append(result.group())
            messages.append(line.split(result.group())[1].rstrip('[').lstrip(']'))
    log_dictionary['Dates'] = dates
    log_dictionary['Messages'] = messages
    return log_dictionary


def clean_pandas_df(data):
    """
    Creates a Pandas Dataframe to prepare data for analysis
    :param  (dictionary): Dates(includes Time) and Messages(Includes Names)
    :return (DataFrame): orgonized chat log into 4 columns(Date, Time, Names, Messages)
    """
    ha_domies_df = pd.DataFrame(data)
    ha_domies_df = ha_domies_df.drop([0, 1, 2], axis=0)
    
    ha_domies_df[['Date', 'Time']] = ha_domies_df.Dates.str.split(",", expand=True)
    ha_domies_df['Date'] = ha_domies_df.Date.str.lstrip('[')
    
    ha_domies_df['Time'] = ha_domies_df.Time.str.rstrip(']')
    
    ha_domies_df['Names'] = ha_domies_df['Messages'].str.extract('([A-z][a-z]+\s[A-Z][a-z]+:)', expand=True)
    ha_domies_df['Names'] = ha_domies_df.Names.str.rstrip(":")
    
    ha_domies_df['Messages'] = ha_domies_df.Messages.str.split('([A-z][a-z]+\s[A-Z][a-z]+:)', expand=True)[2]
    ha_domies_df['Messages'] = ha_domies_df.Messages.str.replace("\n","").replace("\t","")

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

    ha_domies_df = ha_domies_df[['Date', 'Time', 'Names', 'Messages']]
    return ha_domies_df


def basic_analysis(df):
    """
    Collect basic statistics such as # of messages, # of members,
    total # of words, longest messsage length, longest message holder
    :param  (Dataframe): Takes in dataframe from clean_pandas_df
    :return (): stats from above
    """
    number_members = len(df['Names'].unique())
    number_messages = len(df['Messages'])
    
    msg_lengths = df.Messages.map(lambda x: len(x))
    msg_lengths_2 = df.Messages.map(lambda x: len(x.split(" ")))
    #print(list(msg_lengths.nlargest(10).values))
    #print(msg_lengths_2.nlargest())
    #print(df.loc[[36815, 27129, 14993, 36816, 16172]])

    # longest_message = df.Messages.map(lambda x: len(x.split(" "))).max()
    # total_words = df.Messages.map(lambda x: len(x.split(" "))).sum()
    # longest_message_index = df.Messages.apply(lambda x: len(x) == 2090)
    # longest_message_holder = df.loc[27130, 'Names']
    # longest_message_length = 2090
    #print(total_words)
    #print(number_messages, number_members, total_words, longest_message_holder, longest_message_length)


def emoji_stats(df):
    """
    Plots # of emojis used by each member in the group.
    :df     (dataframe)
    :return (none)
    """
    emojis = []
    num_emojis = []
    for msg in df.Messages:
        if len(extract_emojis(msg)) != 0:
            emojis.append(extract_emojis(msg))
            num_emojis.append(grapheme.length(extract_emojis(msg)))
        else:
            emojis.append('None')
            num_emojis.append(int('0'))
    df['Emojis'] = np.array(emojis)
    df['# of Emojis'] = np.array(num_emojis)
    emoji_df = df.groupby('Names').sum()[['# of Emojis']].sort_values(by=['# of Emojis'])
    emoji_df = emoji_df.reset_index()
    fig = px.bar(emoji_df, x='# of Emojis', y='Names', orientation='h')
    fig.show()



if __name__ == '__main__':  
    chat_history = get_chathistory()
    data = prepare_for_pandas(chat_history)
    df = clean_pandas_df(data)
    #basic_analysis(df)
    emoji_stats(df)

