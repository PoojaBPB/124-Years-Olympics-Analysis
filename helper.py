import numpy as np

def fetch_medal_tally(df, Year, Country):
    medal_df = df.drop_duplicates(subset=['NOC', 'Sport', 'Event', 'Medal', 'Year', 'region', 'Team', 'City'])
    flag = 0
    if Year == 'Overall' and Country == 'Overall':
        temp_df = medal_df
    if Year == 'Overall' and Country != 'Overall':
        flag = 1
        temp_df = medal_df[medal_df['region'] == Country]
    if Year != 'Overall' and Country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == int(Year)]
    if Year != 'Overall' and Country != 'Overall':
        temp_df = medal_df[(medal_df['Year'] == int(Year)) & (medal_df['region'] == Country)]

    if flag == 0:
        x = temp_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',
                                                                                      ascending=False).reset_index()
    else:
        x = temp_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year').reset_index()

    x['Total'] = x['Gold'] + x['Bronze'] + x['Silver']

    return x

def medal_tally(df):
    medal_tally = df.drop_duplicates(subset=['NOC', 'Sport', 'Event', 'Medal', 'Year', 'region', 'Team', 'City'])
    medal_tally = medal_tally.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',ascending=False).reset_index()
    medal_tally['Total'] = medal_tally['Gold'] + medal_tally['Bronze'] + medal_tally['Silver']

    return medal_tally

def country_year_list(df):
    Years = df['Year'].unique().tolist()
    Years.sort()
    Years.insert(0, 'Overall')

    Country = np.unique(df['region'].dropna().values).tolist()
    Country.sort()
    Country.insert(0, 'Overall')

    return Years, Country

def data_over_time(df, col):
    nation_over_time = (
        df.drop_duplicates(['Year', col])
        .groupby('Year')
        .size()
        .reset_index(name= col)
        .rename(columns={'Year': 'Edition'})
    )
    return nation_over_time

def most_succesful(df,sport):
    temp_df = df.dropna(subset=['Medal'])

    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport']==sport]
    x= temp_df['Name'].value_counts().reset_index().head(15).merge(df, on='Name', how='left')[['Name', 'count', 'Sport', 'region']].drop_duplicates('Name')
    x.rename(columns={'count': 'Medals'},inplace=True)
    return x

def yearwise_medal_tally(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['NOC', 'Sport', 'Event', 'Medal', 'Year', 'region', 'Team', 'City'], inplace=True)
    new_df = temp_df[temp_df['region'] == country]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()
    return final_df

def country_sport_wise_analysis(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['NOC', 'Sport', 'Event', 'Medal', 'Year', 'region', 'Team', 'City'], inplace=True)
    new_df = temp_df[temp_df['region'] == country]
    pt= new_df.pivot_table(index = 'Sport', columns='Year', values='Medal', aggfunc='count').fillna(0).astype('int')
    return pt

def most_succesful_countrywise(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df = temp_df[temp_df['region']==country]
    x= temp_df['Name'].value_counts().reset_index().head(10).merge(df, on='Name', how='left')[['Name', 'count', 'Sport']].drop_duplicates('Name')
    x.rename(columns={'count': 'Medals'},inplace=True)
    return x

def distribution_age(df):
    athlete_df = df.drop_duplicates(subset=['Name', 'region', 'Year'])
    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()
    return x1,x2,x3,x4

def Age_wrt_sports(df):
    temp_df = df.dropna(subset=['Medal', 'Sport', 'Age'])
    gold_df = temp_df[temp_df['Medal'] == 'Gold']
    top_sports =  popular_sports = gold_df['Sport'].value_counts().head(15).index
    x = []
    name = []
    for sport in top_sports:
        ages = gold_df[gold_df['Sport'] == sport]['Age']
        x.append(ages)
        name.append(sport)
    return x, name

def men_vs_women(df):
    athlete_df = df.drop_duplicates(subset=['Name', 'region', 'Year'])
    Men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    Women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()
    final = Men.merge(Women, on='Year', how='left')
    final.rename(columns={'Name_x': 'Men', 'Name_y': 'Women'}, inplace=True)
    final.fillna(0, inplace=True)
    return final