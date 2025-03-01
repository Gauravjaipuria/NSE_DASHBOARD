from nselib import capital_market
from nselib import derivatives
import streamlit as st


st.header('📈 Indian Stock Market Dashboard 2025 – Real-Time Insights & Analytics')

instrument = st.sidebar.selectbox('Instrument type', options=('NSE equity Market','NSE Derivative Market'))
if instrument == 'NSE equity Market':
    data_info = st.sidebar.selectbox('Data to extract',options=('equity_list','india_vix_data','nifty50_equity_list','bhav_copy_with_delivery','bhav_copy_equities','price_volume_and_deliverable_position_data','deliverable_position_data','fno_equity_list'))
    if (data_info == 'equity_list') or (data_info == 'fno_equity_list') or (data_info == 'nifty50_equity_list'):
        data = getattr(capital_market,data_info)()
    if (data_info == 'bhav_copy_with_delivery') or (data_info == 'bhav_copy_equities'):
        date = st.sidebar.text_input('Date','25-02-2025')
        data = getattr(capital_market,data_info)(date)
    if (data_info == 'india_vix_data'):
       period = st.sidebar.text_input('period','1m')
       data = getattr(capital_market,data_info)(period=period) 
    if (data_info == 'price_volume_and_deliverable_position_data') or (data_info == 'deliverable_position_data'):
       Symbol = st.sidebar.text_input('Symbol','VEDL')
       from_date = st.sidebar.text_input('from_date','25-02-2024')
       to_date = st.sidebar.text_input('to_date','25-02-2025')
       method = getattr(capital_market, data_info)  # Get the method
       data = method(Symbol, from_date, to_date)  # Call the method correctly
if instrument == 'NSE Derivative Market':
        data_info = st.sidebar.selectbox('Data to extract',options=('expiry_dates_future','expiry_dates_option_index','fii_derivatives_statistics','fno_bhav_copy','future_price_volume_data','participant_wise_open_interest','nse_live_option_chain','option_price_volume_data','participant_wise_trading_volume'))
        if (data_info == 'expiry_dates_future') or (data_info == 'expiry_dates_option_index'):
            data = getattr(derivatives,data_info)()
        if (data_info == 'fii_derivatives_statistics') or (data_info == 'fno_bhav_copy') or (data_info == 'participant_wise_trading_volume') or (data_info == 'participant_wise_open_interest') :
            date = st.sidebar.text_input('Date','25-02-2025')
            data = getattr(derivatives,data_info)(date)
        if (data_info == 'future_price_volume_data') :
            ticker = st.sidebar.text_input('Ticker','VEDL')
            type_ = st.sidebar.text_input('Instrument Type','FUTSTK')
            period = st.sidebar.text_input('period','1m')
            data = derivatives.future_price_volume_data(ticker,type_,period=period)
        if (data_info == 'option_price_volume_data') :
            ticker = st.sidebar.text_input('Ticker','BANKNIFTY')
            type_ = st.sidebar.text_input('Instrument Type','OPTIDX')
            period = st.sidebar.text_input('period','1m')
            data = derivatives.option_price_volume_data(ticker,type_,period=period)
        if (data_info == 'nse_live_option_chain') :
            ticker = st.sidebar.text_input('Ticker','BANKNIFTY')
            expiry_date = st.sidebar.text_input('Expiry Date','27-03-2025')
            data = derivatives.nse_live_option_chain(ticker,expiry_date=expiry_date)


st.write(data)