# IPL Data Analyzer 2008-2024 🏏

**Live App:** [https://ipl-data-analyzer-c35hf9gnuruvd5c7na5j65.streamlit.app/)

### Project Overview
An interactive Streamlit web app for analyzing IPL cricket data from 2008 to 2024. This project processes 2.5L+ ball-by-ball records to generate insights on teams, players, and match trends using Python, Pandas, and Plotly.

### Dashboard Preview

#### 1. Main Dashboard
![Dashboard](screenshots/1-dashboard-home.png)
Season-wise filters, key stats, and toss impact analysis for 2024 season showing KKR as winners.

#### 2. Top Performers Analysis  
![Top Performers](screenshots/2-top-performers.png)
Interactive bar charts showing Top 10 Run Scorers and stadium-wise match distribution for 2024.

#### 3. Player Comparison
![Player Comparison](screenshots/3-player-comparison.png)
Head-to-head statistical comparison between any two players. Example: Virat Kohli vs Rohit Sharma.

### Key Features
- **Dynamic Filters**: Analyze data by Season and Team
- **Toss Impact**: Visualize how toss decisions affect match outcomes with pie charts
- **Performance Tracking**: Top run scorers, wicket takers with interactive Plotly charts
- **Player vs Player**: Compare batting stats like Runs, Balls, Strike Rate of any two players
- **Venue Analysis**: Donut chart showing stadium-wise match distribution

### Tech Stack
- **Python** - Core language
- **Pandas** - Data cleaning, manipulation & analysis of 26MB dataset
- **Streamlit** - Web framework for deployment
- **Plotly** - Interactive data visualizations

### Dataset
- `matches.csv` - Contains 1000+ match-level data from 2008-2024
- `deliveries.csv` - Contains 2.5L+ ball-by-ball data, 26MB file

### How to Run Locally
```bash
git clone https://github.com/akash1234-design/ipl-data-analyzer.git
cd ipl-data-analyzer
pip install -r requirements.txt
streamlit run app.py
