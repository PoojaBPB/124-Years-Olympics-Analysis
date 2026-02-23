import streamlit as st
import pandas as pd
import preprocessorwinter, helper
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.figure_factory as ff

def run():
    df1 = pd.read_csv('Athletes_winter_games.csv')
    df2 = pd.read_csv('regions.csv')
    df = preprocessorwinter.preprocess(df1, df2)

    st.sidebar.title('Winter Olympics Analysis (1924–2014)')
    st.sidebar.image('https://www.wascocountylibrary.com/sites/default/files/2025-12/winter-olympic-games.jpg')

    user_menu = st.sidebar.radio(
        'SELECT AN OPTION',
        ['Medal Tally', 'Overall Analysis', 'Country wise Analysis', 'Athlete wise Analysis']
    )

    if user_menu == 'Medal Tally':
        st.sidebar.header('Medal Tally')
        Years, Country = helper.country_year_list(df)
        selected_year = st.sidebar.selectbox('Select Year', Years)
        selected_country = st.sidebar.selectbox('Select Country', Country)

        medal_tally = helper.fetch_medal_tally(df, selected_year, selected_country)
        if selected_year == 'Overall' and selected_country == 'Overall':
            st.title('Overall Medal Tally')
        if selected_year == 'Overall' and selected_country != 'Overall':
            st.title(f"{selected_country}'s Overall Performance in the Olympics")
        if selected_year != 'Overall' and selected_country != 'Overall':
            st.title(f"{selected_country}'s Performance in the {selected_year} Olympics")
        if selected_year != 'Overall' and selected_country == 'Overall':
            st.title(f'Medal Tally in the {selected_year} Olympics')

        st.table(medal_tally)

    if user_menu == 'Overall Analysis':
        st.title('Olympics Statistics (1924–2014)')

        editions = df['Year'].unique().shape[0] - 1
        cities = df['City'].unique().shape[0]
        sports = df['Sport'].unique().shape[0]
        events = df['Event'].unique().shape[0]
        athletes = df['Name'].unique().shape[0]
        countries = df['region'].unique().shape[0]

        col1, col2, col3 = st.columns(3)
        with col1:
            st.header('Editions')
            st.title(editions)
        with col2:
            st.header('Cities')
            st.title(cities)
        with col3:
            st.header('Sports')
            st.title(sports)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.header('Events')
            st.title(events)
        with col2:
            st.header('Athletes')
            st.title(athletes)
        with col3:
            st.header('Countries')
            st.title(countries)

        nation_over_time = helper.data_over_time(df, 'region')
        nation_over_time = nation_over_time.rename(columns={'region': 'Country'})
        fig = px.line(nation_over_time, x='Edition', y='Country')
        st.title('Participating Countries over the years')
        st.plotly_chart(fig)

        event_over_time = helper.data_over_time(df, 'Event')
        fig = px.line(event_over_time, x='Edition', y='Event')
        st.title('Events over the years')
        st.plotly_chart(fig)

        athletes_over_time = helper.data_over_time(df, 'Name')
        athletes_over_time = athletes_over_time.rename(columns={'Name': 'Athletes'})
        fig = px.line(athletes_over_time, x='Edition', y='Athletes')
        st.title('Athletes over the years')
        st.plotly_chart(fig)

        st.title('Events per Sport Over Time')
        fig, ax = plt.subplots(figsize=(20, 20))
        x = df.drop_duplicates(['Year', 'Sport', 'Event'])
        ax = sns.heatmap(
            x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'),
            annot=True)
        st.pyplot(fig)

        st.title('Most Successful Athletes')
        sport_list = df['Sport'].unique().tolist()
        sport_list.sort()
        sport_list.insert(0, 'Overall')

        selected_sport = st.selectbox('Select Sport', sport_list)
        x = helper.most_succesful(df, selected_sport)
        st.table(x)

    if user_menu == 'Country wise Analysis':
        st.sidebar.title('Country wise Analysis')
        country_list = df['region'].dropna().unique().tolist()
        country_list.sort()
        selected_country = st.sidebar.selectbox('Select Country', country_list)

        yearwise_medal_tally = helper.yearwise_medal_tally(df, selected_country)
        fig = px.line(yearwise_medal_tally, x='Year', y='Medal')
        st.title(f'{selected_country} Medal Tally')
        st.plotly_chart(fig)

        pt = helper.country_sport_wise_analysis(df, selected_country)
        st.title(f'{selected_country} Sport wise Analysis')
        if pt is None or pt.empty:
            st.warning(f'{selected_country} has no Winter Olympic medal data.')
        else:
            fig, ax = plt.subplots(figsize=(20, 20))
            sns.heatmap(pt, annot=True, fmt='g')
            st.pyplot(fig)



        top_10 = helper.most_succesful_countrywise(df, selected_country)
        st.title(f'{selected_country} - Top 10 Athletes')
        st.table(top_10)

    if user_menu == 'Athlete wise Analysis':
        x1, x2, x3, x4 = helper.distribution_age(df)
        fig = ff.create_distplot([x1, x2, x3, x4],
                                 ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],
                                 show_hist=False, show_rug=False)
        st.title('Distribution of Age')
        fig.update_layout(autosize=False, width=1200, height=600, xaxis_title='Age (Years)',
                          yaxis_title='Probability Density')
        st.plotly_chart(fig)

        x, name = helper.Age_wrt_sports(df)
        fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
        fig.update_layout(autosize=False, width=1200, height=600, xaxis_title='Age (Years)',
                          yaxis_title='Probability Density')
        st.title('Distribution of Age wrt sports(Gold Medalist)')
        st.plotly_chart(fig)

        st.title('Men vs Women Participation over the years')
        final = helper.men_vs_women(df)
        fig = px.line(final, x='Year', y=['Men', 'Women'])
        st.plotly_chart(fig)








