
import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import yfinance as yf

#Writing the title & description

st.title("Nifty 50 app")

st.markdown("""
	This app retrieves the list of the **NIFTY 50** (from Wikipedia) and its corresponding **stock closing price** (year-to-date)!
* **Python libraries:** base64, pandas, streamlit, numpy, matplotlib, yfinance
* **Data source:** [Wikipedia](https://en.wikipedia.org/wiki/NIFTY_50).
""")

# Writing the Sidebar header

st.sidebar.header("Choose the sector")

# Webscraping the Nify50 data

@st.cache
# Writing a custom function to scrap data
def load_data():
    url = 'https://en.wikipedia.org/wiki/NIFTY_50'
    html = pd.read_html(url, header = 0)
    df = html[1]
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

st.header('Display Companies in Selected Sector')

# Verify & prompt if empty df
if chosen_sector_df.empty:
    st.write('You have not selected any sectors. Please select a sector.')

else: 
    st.write('Data Dimension: ' + str(chosen_sector_df.shape[0]) + ' rows and ' + str(chosen_sector_df.shape[1]) + ' columns.')
    st.dataframe(chosen_sector_df)

    # creating a download feature

    def filedownload(df):
        csv = df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
        href = f'<a href="data:file/csv;base64,{b64}" download="NIFTY50.csv">Download CSV File</a>'
        return href

    st.markdown(filedownload(chosen_sector_df), unsafe_allow_html=True)

    # Loading data of tickers

    data = yf.download(
            tickers = [(i+ '.NS') for i in list(chosen_sector_df['Symbol'])],
            period = "ytd",
            interval = "1d",
            group_by = 'ticker',
            auto_adjust = True,
            prepost = True,
            threads = True,
            proxy = None
        )

    # Plot Closing Price of Query Symbols

    def price_plot(symbol):
      df = pd.DataFrame(data[symbol].Close)
      df['Date'] = df.index
      plt.clf()
      plt.fill_between(df.Date, df.Close, color='skyblue', alpha=0.3)
      plt.plot(df.Date, df.Close, color='skyblue', alpha=0.8)
      plt.xticks(rotation=90)
      plt.title(symbol, fontweight='bold')
      plt.xlabel('Date', fontweight='bold')
      plt.ylabel('Closing Price', fontweight='bold')
      return st.pyplot(plt)
      

    num_company = st.sidebar.slider('Number of Companies', 1, 5)

    if st.button('Show Plots'):
        st.header('Stock Closing Price')
        for i in [(i+ '.NS') for i in list(chosen_sector_df['Symbol'])][:num_company]:
            price_plot(i)



