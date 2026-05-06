import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="IPL Analyzer", layout="wide")

st.title("🏏 IPL Data Analyzer")
st.write("2008-2024 IPL Data Analysis | Python + Pandas + Streamlit")

# Data load karo
@st.cache_data
def load_data():
    matches = pd.read_csv("matches.csv")
    deliveries = pd.read_csv("deliveries.csv")
    return matches, deliveries

matches, deliveries = load_data()

# Sidebar filters
st.sidebar.header("Filters")
years = sorted(matches['season'].unique())
selected_year = st.sidebar.selectbox("Season select karo", years)
st.sidebar.divider()
teams = sorted(matches['team1'].unique())
selected_team = st.sidebar.multiselect(
    "Team Select Karo", 
    options=teams, 
    default=None,
    placeholder="All Teams"
)
# Filter data
# Filter data
season_matches = matches[matches['season'] == selected_year]

if selected_team:
    season_matches = season_matches[
        (season_matches['team1'].isin(selected_team)) | 
        (season_matches['team2'].isin(selected_team))
    ]


# KPI Cards - Safe version
col1, col2, col3, col4 = st.columns(4)

if not season_matches.empty:
    col1.metric("Total Matches", len(season_matches))
    col2.metric("Teams", season_matches['team1'].nunique())

    # Winner check
    # KPI Cards - Final Safe Version
col1, col2, col3, col4 = st.columns(4)

if not season_matches.empty:
    col1.metric("Total Matches", len(season_matches))
    col2.metric("Teams", season_matches['team1'].nunique())

    # Winner check
    if not season_matches['winner'].dropna().empty:
        col3.metric("Winner", season_matches['winner'].mode()[0])
    else:
        col3.metric("Winner", "No Data")

    # Player of Match check
    if not season_matches['player_of_match'].dropna().empty:
        col4.metric("Player of Match", season_matches['player_of_match'].mode()[0])
    else:
        col4.metric("Player of Match", "No Data")
else:
    col1.metric("Total Matches", 0)
    col2.metric("Teams", 0)
    col3.metric("Winner", "No Data")
    col4.metric("Player of Match", "No Data")
st.divider()
st.subheader(f"Toss Impact in {selected_year}")

if not season_matches.empty:
    toss_wins = season_matches['toss_winner'] == season_matches['winner']
    toss_win_percent = round(toss_wins.mean() * 100, 2)

    col5, col6 = st.columns(2)
    col5.metric("Toss Jeetke Match Jeeta", f"{toss_win_percent}%")

    if not season_matches['toss_decision'].mode().empty:
        col6.metric("Toss Decision", season_matches['toss_decision'].mode()[0])
    else:
        col6.metric("Toss Decision", "No Data")

    toss_fig = px.pie(season_matches, names='toss_decision', title='Toss Decision: Bat vs Field')
    st.plotly_chart(toss_fig, width='stretch')
else:
    st.warning("No toss data available for selected filters")
## Team wins chart
if not season_matches.empty:
    team_wins = season_matches['winner'].value_counts()
    fig = px.bar(team_wins, x=team_wins.index, y=team_wins.values,
                 title=f'Team Wins in {selected_year}',
                 labels={'x': 'Team', 'y': 'Wins'})
    fig.update_traces(text=team_wins.values, textposition='outside')
    st.plotly_chart(fig, width='stretch')
else:
    st.warning("No team wins data available for selected filters")
st.subheader(f"Top 10 Run Scorers in {selected_year}")

if not season_matches.empty:
    season_deliveries = deliveries[deliveries['match_id'].isin(season_matches['id'])]
    
    if not season_deliveries.empty:
        top_scorers = season_deliveries.groupby('batter')['batsman_runs'].sum().reset_index()
        top_scorers = top_scorers.sort_values('batsman_runs', ascending=False).head(10)
        top_scorers.columns = ['Player', 'Runs']
        
        col7, col8 = st.columns(2)
        with col7:
            st.dataframe(top_scorers, width='stretch', hide_index=True)
        with col8:
            bar_fig = px.bar(top_scorers, x='Player', y='Runs', title='Top Scorers',
                             text='Runs', color='Runs')
            bar_fig.update_traces(textposition='outside')
            st.plotly_chart(bar_fig, width='stretch')
    else:
        st.warning("No batting data available for selected filters")
else:
    st.subheader(f"Venue-wise Match Count in {selected_year}")

if not season_matches.empty:
    venue_counts = season_matches['venue'].value_counts().reset_index().head(8)
    venue_counts.columns = ['Venue', 'Matches']
    
    col9, col10 = st.columns(2)
    with col9:
        st.dataframe(venue_counts, width='stretch', hide_index=True)
    with col10:
        venue_fig = px.pie(venue_counts, names='Venue', values='Matches', 
                           title='Top 8 Venues', hole=0.3)
        st.plotly_chart(venue_fig, width='stretch')
else:
    st.warning("No venue data available for selected filters")
st.header("Player Comparison")
col1, col2 = st.columns(2)
players = sorted(deliveries['batter'].unique())
player1 = col1.selectbox("Player 1", players, index=0)
player2 = col2.selectbox("Player 2", players, index=1)

def get_player_stats(player):
    df = deliveries[deliveries['batter'] == player]
    runs = df['batsman_runs'].sum()
    balls = df[df['extras_type']!= 'wides'].shape[0]
    return {"Runs": runs, "Balls": balls, "SR": round(runs/balls*100, 2) if balls > 0 else 0}

p1_stats = get_player_stats(player1)
p2_stats = get_player_stats(player2)

comp_df = pd.DataFrame([p1_stats, p2_stats], index=[player1, player2])
st.dataframe(comp_df,  width='stretch')

fig2 = px.bar(comp_df, barmode='group', title="Player Comparison")
st.plotly_chart(fig2,  width='stretch')