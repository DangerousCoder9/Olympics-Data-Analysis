import numpy as np

def medal_tally(df):
     medal_tally = df.drop_duplicates(subset=(['Team','NOC','Games','Year','City','Sport','Event','Medal']))
     # Now again Groupby with the Noc and the Medals
     medal_tally = medal_tally.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values('Gold' , ascending=False).reset_index()
     medal_tally['Total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']
     return medal_tally
 
 
def country_year_list(df):
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0,'Overall')
    country = np.unique(df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0,'Overall')
    return years,country


def fetch_medal_tally(df , years , country):
    medal_df = df.drop_duplicates(subset=(['Team','NOC','Games','Year','City','Sport','Event','Medal']))
    flag = 0
    if years == 'Overall' and country == 'Overall':
        temp_df = medal_df
    if years == 'Overall' and country != 'Overall':
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]
    if years != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == years]
    if years != 'Overall' and country != 'Overall':
        temp_df = medal_df[(medal_df['Year'] == years) & (medal_df['region'] == country)]  
    
    if flag == 1:
        X = temp_df.groupby('Year').sum()[['Gold','Silver','Bronze']].sort_values('Year').reset_index()
    else:
        X = temp_df.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values('Gold' , ascending=False).reset_index()
    
    X['Total'] = X['Gold'] + X['Silver'] + X['Bronze']
    return X

def nations_over_time(df):
    # Getting over the years how many nations participated in the Olympics
    nations_over_time =  df.drop_duplicates(['Year','region'])['Year'].value_counts().reset_index().sort_index(ascending=False)
    return nations_over_time

def events_over_time(df):
    events_over_time =  df.drop_duplicates(['Year','Event'])['Year'].value_counts().reset_index().sort_index(ascending=False)
    return events_over_time

def atheletes_over_time(df):
    atheletes_over_time =  df.drop_duplicates(['Year','Name'])['Year'].value_counts().reset_index().sort_index(ascending=False)
    return atheletes_over_time

def sports_events(df):
    x = df.drop_duplicates(['Year' , 'Sport' , 'Event'])
    # 2. Making a Pivot table
    x_pivot_table = x.pivot_table(index='Sport',columns='Year',values='Event',aggfunc='count').fillna(0).astype(int)
    return x_pivot_table

# Creating a function which will tell you the most successful athelete in then respective sport
def most_successful(df ,sport):
    # Now we dont need a Athelete who doesn't have any medal so 
    temp_df = df.dropna(subset='Medal')
    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]
    temp_df = temp_df['Name'].value_counts().reset_index().head(15).merge(df , left_on = 'Name' , right_on = 'Name' , how = 'left')[['Name','count','region','Sport']].drop_duplicates('Name')
    temp_df = temp_df.rename(columns={'count': 'Medals'})
    temp_df = temp_df.rename(columns={'region': 'Country'})
    return temp_df

def year_wise_medal_tally(df , country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'] , inplace=True) # this is telling that if a team has won a medal then count only one not 11 so drop all the duplicates with respect to 'Team','NOC','Games','Year','City','Sport','Event','Medal' 
    new_df = temp_df[temp_df['region'] == country]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()
    return final_df

def country_sports_map(df , country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Sport','Event','Medal'] , inplace=True) # this is telling that if a team has won a medal then count only one not 11 so drop all the duplicates with respect to 'Team','NOC','Games','Year','City','Sport','Event','Medal' 
    new_df = temp_df[temp_df['region'] == country]
    pivot_table = new_df.pivot_table(index='Sport',columns='Year',values='Medal',aggfunc='count').fillna(0).astype(int)
    return pivot_table
   
   
def most_successful_athelete_country(df , country):
    # Now we dont need a Athelete who doesn't have any medal so 
    temp_df = df.dropna(subset='Medal')
    temp_df = temp_df[temp_df['region'] == country]
    temp_df = temp_df['Name'].value_counts().reset_index().head(10).merge(df , left_on = 'Name' , right_on = 'Name' , how = 'left')[['Name','count','Sport']].drop_duplicates('Name')
    temp_df = temp_df.rename(columns={'count': 'Medals'})
    return temp_df

def menvswomen(df):
    athelete_df = df.drop_duplicates(subset =['Name','region'])
    return athelete_df