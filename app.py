import streamlit as st
import pandas as pd
import plotly.express as px
from io import StringIO

st.set_page_config(
    page_title="Shri Balaji Entertainment Dashboard",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 Shri Balaji Entertainment")
st.subheader("Social Media Performance Dashboard")
st.markdown("---")

# Load data
from io import StringIO

data = """Date,Content_Type,Topic,Likes,Comment,Views
01-06-2026,Reel,Promo,27,1,1600
31-05-2026,Reel,Announcement,12600,360,410000
30-05-2026,Reel,Promo,50,3,3600
29-05-2026,Reel,Promo,49,8,2600
28-05-2026,Reel,Announcement,1190,41,187000
27-05-2026,Post,Announcement,15400,109,159000
26-05-2026,Post,Announcement,103,10,8879
25-05-2026,Post,Announcement,4400,140,134000
24-05-2026,Reel,Promo,48,7,4300
18-05-2026,Post,Announcement,26100,911,532000
14-05-2026,Reel,Artist Feature,1714,46,16582
11-05-2026,Post,Promo,59,5,1857
08-05-2026,Reel,Concert Promo,3455,143,83011
06-05-2026,Reel,Behind Scenes,225,11,15815
04-05-2026,Reel,Promo,55,6,1931
02-05-2026,Post,Concert Promo,1430,63,35170
30-04-2026,Reel,Promo,235,26,17454
29-04-2026,Reel,Promo,123,8,5469
28-04-2026,Post,Announcement,2797,106,62037
26-04-2026,Reel,Promo,102,14,6364
25-04-2026,Reel,Promo,46,4,2000
22-04-2026,Reel,Concert Promo,1134,51,28939
21-04-2026,Post,Announcement,6570,148,154548
18-04-2026,Reel,Concert Promo,300,9,8487
16-04-2026,Reel,Artist Feature,232,8,3935
13-04-2026,Reel,Promo,42,6,2330
12-04-2026,Post,Promo,29,1,1856
10-04-2026,Reel,Audience Reaction,4211,215,115715
09-04-2026,Reel,Promo,32,4,2161
07-04-2026,Reel,Announcement,902,34,21841
05-04-2026,Post,Artist Feature,4101,144,38044
02-04-2026,Reel,Promo,55,4,2094
30-03-2026,Post,Concert Promo,1934,67,23667
28-03-2026,Reel,Promo,21,2,712
27-03-2026,Post,Announcement,2557,64,49134
26-03-2026,Reel,Behind Scenes,72,6,2922
23-03-2026,Reel,Artist Feature,389,12,6247
20-03-2026,Reel,Promo,90,5,2794
17-03-2026,Reel,Promo,41,4,1699
15-03-2026,Reel,Promo,52,6,2117
12-03-2026,Reel,Promo,41,3,2064
09-03-2026,Reel,Announcement,35000,1353,713800
06-03-2026,Reel,Announcement,4835,162,109505
05-03-2026,Reel,Promo,28,1,1487
04-03-2026,Reel,Behind Scenes,128,13,4163
03-03-2026,Post,Song Launch,533,24,7102
02-03-2026,Post,Song Launch,2228,55,22376
28-02-2026,Reel,Concert Promo,300,12,7700
26-02-2026,Reel,Promo,23,3,1356
23-02-2026,Reel,Promo,78,7,5925"""

df = pd.read_csv(StringIO(data))
df['Date'] = pd.to_datetime(df['Date'], format='%d-%m-%Y')
df['Engagement_Rate'] = ((df['Likes'] + df['Comment']) / df['Views'] * 100).round(2)
df['Day_of_Week'] = df['Date'].dt.day_name()
df['Month'] = df['Date'].dt.to_period('M').astype(str)

# Summary metrics row
st.subheader("📊 Overall Performance")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Posts", len(df))

with col2:
    st.metric("Avg Views per Post", f"{int(df['Views'].mean()):,}")

with col3:
    best_topic = df.groupby('Topic')['Views'].mean().idxmax()
    st.metric("Best Performing Topic", best_topic)

with col4:
    best_day = df.groupby('Day_of_Week')['Views'].mean().idxmax()
    st.metric("Best Day to Post", best_day)

st.markdown("---")
# Charts section
st.subheader("📈 Content Performance Analysis")

col1, col2 = st.columns(2)

with col1:
    avg_views = df.groupby('Topic')['Views'].mean().sort_values(ascending=False)
    fig1 = px.bar(
        x=avg_views.index,
        y=avg_views.values,
        title="Average Views by Topic",
        labels={'x': 'Topic', 'y': 'Average Views'},
        color=avg_views.values,
        color_continuous_scale='Oranges'
    )
    st.plotly_chart(fig1, use_container_width=True, key="fig1")

with col2:
    avg_engagement = df.groupby('Topic')['Engagement_Rate'].mean().sort_values(ascending=False)
    fig2 = px.bar(
        x=avg_engagement.index,
        y=avg_engagement.values,
        title="Engagement Rate by Topic (%)",
        labels={'x': 'Topic', 'y': 'Engagement Rate'},
        color=avg_engagement.values,
        color_continuous_scale='Greens'
    )
    st.plotly_chart(fig2, use_container_width=True, key="fig2")
st.markdown("---")

col3, col4 = st.columns(2)

with col3:
    day_order = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    avg_views_day = df.groupby('Day_of_Week')['Views'].mean().reindex(day_order)
    fig3 = px.bar(
        x=avg_views_day.index,
        y=avg_views_day.values,
        title="Best Days to Post",
        labels={'x': 'Day', 'y': 'Average Views'},
        color=avg_views_day.values,
        color_continuous_scale='Blues'
    )
    st.plotly_chart(fig3, use_container_width=True, key="fig3")
with col4:
    monthly_views = df.groupby('Month')['Views'].sum().reset_index()
    fig4 = px.line(
        monthly_views,
        x='Month',
        y='Views',
        title="Monthly Views Trend",
        markers=True
    )
    st.plotly_chart(fig4, use_container_width=True, key="fig4")
st.markdown("---")
# Charts section
st.subheader("📈 Content Performance Analysis")

col1, col2 = st.columns(2)

with col1:
    avg_views = df.groupby('Topic')['Views'].mean().sort_values(ascending=False)
    fig1 = px.bar(
        x=avg_views.index,
        y=avg_views.values,
        title="Average Views by Topic",
        labels={'x': 'Topic', 'y': 'Average Views'},
        color=avg_views.values,
        color_continuous_scale='Oranges'
    )
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    avg_engagement = df.groupby('Topic')['Engagement_Rate'].mean().sort_values(ascending=False)
    fig2 = px.bar(
        x=avg_engagement.index,
        y=avg_engagement.values,
        title="Engagement Rate by Topic (%)",
        labels={'x': 'Topic', 'y': 'Engagement Rate'},
        color=avg_engagement.values,
        color_continuous_scale='Greens'
    )
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

col3, col4 = st.columns(2)

with col3:
    day_order = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    avg_views_day = df.groupby('Day_of_Week')['Views'].mean().reindex(day_order)
    fig3 = px.bar(
        x=avg_views_day.index,
        y=avg_views_day.values,
        title="Best Days to Post",
        labels={'x': 'Day', 'y': 'Average Views'},
        color=avg_views_day.values,
        color_continuous_scale='Blues'
    )
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    monthly_views = df.groupby('Month')['Views'].sum().reset_index()
    fig4 = px.line(
        monthly_views,
        x='Month',
        y='Views',
        title="Monthly Views Trend",
        markers=True
    )
    st.plotly_chart(fig4, use_container_width=True)

st.markdown("---")
