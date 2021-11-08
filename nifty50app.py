import streamlit as st
import pandas as pd
import base64
import plotly.express as px
import yfinance as yf

#Writing the title & description

st.image('https://upload.wikimedia.org/wikipedia/en/thumb/b/be/Nifty_50_Logo.svg/1200px-Nifty_50_Logo.svg.png', width = 100)
st.title("NIFTY 50: India's top 50 companies")
st.markdown("""
#### Get current list of NIFTY 50 stocks and visualize their year-to-date closing price on Interactive Plotly charts!

* **Python libraries**: base64, pandas, streamlit, numpy, plotly, yfinance
* **Data source**: [Wikipedia](https://en.wikipedia.org/wiki/NIFTY_50)
""")

# Writing the Sidebar header

st.sidebar.header("Choose the sector")

# Webscraping the Nify50 data from Wikipedia
# Writing a custom function to scrap data
@st.cache # Caching skips function re-run if the inputs or code haven't changed
def load_data():
    url = 'https://en.wikipedia.org/wiki/NIFTY_50'
    html = pd.read_html(url, header = 0) # Returns row of all tables in url
    df = html[1] # Gets the 2nd table with nifty50 stocks
    return df

# loading the data
df = load_data()
sector = df.groupby('Sector')

# Creating the sidebar Sector selector

u_sectors = sorted(df["Sector"].unique())  #creates list of unique sectors
#creates side bar with unique sector names
chosen_sector= st.sidebar.multiselect('Sector options', u_sectors, u_sectors) 

# Filtering data based on sector
chosen_sector_df = df[df['Sector'].isin(chosen_sector)]

st.markdown("""
    ***NOTE:***  *Use the sidebar on left to select **Sectors**. *

""")
st.header(' List of Companies from Selected Sectors')

# Verify & prompt if empty df
if chosen_sector_df.empty:
    st.write('You have not selected any sectors. Please select a sector.')

else: 
    st.write('Data Dimension: ' + str(chosen_sector_df.shape[0]) + ' rows and ' + str(chosen_sector_df.shape[1]) + ' columns.')
    st.dataframe(chosen_sector_df)

    # Creating a CSV download feature

    def filedownload(df):
        csv = df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
        href = f'<a href="data:file/csv;base64,{b64}" download="NIFTY50.csv">Download CSV File</a>'
        return href

    st.markdown(filedownload(chosen_sector_df), unsafe_allow_html=True)

    # Plot Closing Price of Query Symbols

    def price_plot(symbol):
      df = yf.Ticker(symbol + '.NS').history(period="ytd", interval = "1d")
      #df = pd.DataFrame(data[symbol].Close)
      df['Date'] = df.index
      #             Using Matplotlib
      # plt.clf()
      # plt.fill_between(df.Date, df.Close, color='skyblue', alpha=0.3)
      # plt.plot(df.Date, df.Close, color='skyblue', alpha=0.8)
      # plt.xticks(rotation=90)
      # plt.title(symbol, fontweight='bold')
      # plt.xlabel('Date', fontweight='bold')
      # plt.ylabel('Closing Price', fontweight='bold')
      #             Using Plotly
      plt = px.line(df,x= 'Date', y = 'Close', title = symbol, 
        labels = {'Close':'<b>Closing Price<b>', 'Date':'<b>Date<b>'})
      plt.update_layout(font_family="Arial",
        font_color="black   ", title={
        'y':0.85,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'},
        title_font_family = 'Times New Roman',
        title_font_color="black")
      plt.update_xaxes(rangeslider_visible=True, )
      return st.plotly_chart(plt)

    num_company = st.slider('Slide to select the Number of charts to plot', 1,10)

    if st.button('View Price charts'):
        #st.header('Closing Price')
        for i in list(chosen_sector_df['Symbol'])[:num_company]:
            price_plot(i)



