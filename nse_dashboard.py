from nselib import capital_market, derivatives
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Indian Stock Market Dashboard 2025", layout="wide")
st.header('📈 Indian Stock Market Dashboard 2025 – Real-Time Insights & Analytics')

# Sidebar selections
instrument = st.sidebar.radio('Select Market', options=('NSE Equity Market', 'NSE Derivative Market'))

def fetch_data():
    """Fetch data based on user selection."""
    try:
        if instrument == 'NSE Equity Market':
            data_info = st.sidebar.selectbox('Data to extract', [
                'equity_list', 'india_vix_data', 'nifty50_equity_list',
                'bhav_copy_with_delivery', 'bhav_copy_equities',
                'price_volume_and_deliverable_position_data',
                'deliverable_position_data', 'fno_equity_list'
            ])
            
            if data_info in ['equity_list', 'fno_equity_list', 'nifty50_equity_list']:
                return getattr(capital_market, data_info)()
            
            if data_info in ['bhav_copy_with_delivery', 'bhav_copy_equities']:
                date = st.sidebar.date_input('Select Date').strftime('%d-%m-%Y')
                return getattr(capital_market, data_info)(date)
            
            if data_info == 'india_vix_data':
                period = st.sidebar.text_input('Enter period', '1m')
                return capital_market.india_vix_data(period=period)
            
            if data_info in ['price_volume_and_deliverable_position_data', 'deliverable_position_data']:
                symbol = st.sidebar.text_input('Enter Symbol', 'VEDL')
                from_date = st.sidebar.date_input('From Date').strftime('%d-%m-%Y')
                to_date = st.sidebar.date_input('To Date').strftime('%d-%m-%Y')
                return getattr(capital_market, data_info)(symbol, from_date, to_date)

        elif instrument == 'NSE Derivative Market':
            data_info = st.sidebar.selectbox('Data to extract', [
                'expiry_dates_future', 'expiry_dates_option_index',
                'fii_derivatives_statistics', 'fno_bhav_copy',
                'future_price_volume_data', 'participant_wise_open_interest',
                'nse_live_option_chain', 'option_price_volume_data',
                'participant_wise_trading_volume'
            ])
            
            if data_info in ['expiry_dates_future', 'expiry_dates_option_index']:
                return getattr(derivatives, data_info)()
            
            if data_info in ['fii_derivatives_statistics', 'fno_bhav_copy', 'participant_wise_trading_volume', 'participant_wise_open_interest']:
                date = st.sidebar.date_input('Select Date').strftime('%d-%m-%Y')
                return getattr(derivatives, data_info)(date)
            
            if data_info in ['future_price_volume_data', 'option_price_volume_data']:
                ticker = st.sidebar.text_input('Enter Ticker', 'VEDL')
                type_ = st.sidebar.text_input('Instrument Type', 'FUTSTK' if 'future' in data_info else 'OPTIDX')
                period = st.sidebar.text_input('Enter period', '1m')
                return getattr(derivatives, data_info)(ticker, type_, period=period)
            
            if data_info == 'nse_live_option_chain':
                ticker = st.sidebar.text_input('Enter Ticker', 'BANKNIFTY')
                expiry_date = st.sidebar.date_input('Select Expiry Date').strftime('%d-%m-%Y')
                return derivatives.nse_live_option_chain(ticker, expiry_date=expiry_date)

    except Exception as e:
        st.error(f"⚠️ Error fetching data: {e}")
        return None

# Fetch data
data = fetch_data()

if data is not None:
    st.subheader("📊 Extracted Data")
    
    # Convert data into a DataFrame safely
    try:
        if isinstance(data, pd.DataFrame):
            df = data
        elif isinstance(data, list):
            df = pd.DataFrame(data)
        elif isinstance(data, dict):
            df = pd.DataFrame([data])  # Convert dict to a single-row DataFrame
        else:
            df = pd.DataFrame()
        
        # Display data
        if df.empty:
            st.warning("⚠️ No data available for the selected options.")
        else:
            st.dataframe(df)
            
            # Visualization if 'date' column exists
            if 'date' in df.columns:
                df['date'] = pd.to_datetime(df['date'])
                numeric_cols = df.select_dtypes(include='number').columns
                if len(numeric_cols) > 0:
                    col_to_plot = st.selectbox("📌 Select Column to Plot", numeric_cols)
                    fig = px.line(df, x='date', y=col_to_plot, title=f'{col_to_plot} Over Time')
                    st.plotly_chart(fig)

            # CSV Download Button
            st.download_button("📥 Download Data as CSV", df.to_csv(index=False), file_name="market_data.csv", mime="text/csv")

    except Exception as e:
        st.error(f"⚠️ Data processing error: {e}")
