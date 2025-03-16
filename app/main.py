import streamlit as st
import pandas as pd
from database import create_connection, init_db
from utils import get_stock_data, calculate_portfolio_value
from mysql.connector import Error

def add_stock():
    with st.form("add_stock_form"):
        symbol = st.text_input("Stock Symbol").upper()
        shares = st.number_input("Number of Shares", min_value=0.0)
        purchase_price = st.number_input("Purchase Price", min_value=0.0)
        purchase_date = st.date_input("Purchase Date")
        
        if st.form_submit_button("Add Stock"):
            conn = create_connection()
            if conn:
                try:
                    cursor = conn.cursor()
                    cursor.execute("""
                        INSERT INTO portfolio (symbol, shares, purchase_price, purchase_date)
                        VALUES (%s, %s, %s, %s)
                    """, (symbol, shares, purchase_price, purchase_date))
                    conn.commit()
                    st.success("Stock added successfully!")
                except Error as e:
                    st.error(f"Error adding stock: {e}")
                finally:
                    conn.close()

def main():
    st.title("Stock Portfolio Tracker")
    
    # Initialize database
    init_db()
    
    # Sidebar for adding new stocks
    with st.sidebar:
        st.header("Add New Stock")
        add_stock()
    
    # Main content
    st.header("Portfolio Overview")
    
    # Fetch and display portfolio
    conn = create_connection()
    if conn:
        df = pd.read_sql("SELECT * FROM portfolio", conn)
        if not df.empty:
            # Add current prices and calculations
            current_prices = []
            current_values = []
            gains_losses = []
            
            for _, row in df.iterrows():
                stock_data = get_stock_data(row['symbol'])
                if stock_data:
                    current_price = stock_data['current_price']
                    current_value = current_price * row['shares']
                    gain_loss = current_value - (row['purchase_price'] * row['shares'])
                    
                    current_prices.append(current_price)
                    current_values.append(current_value)
                    gains_losses.append(gain_loss)
            
            df['Current Price'] = current_prices
            df['Current Value'] = current_values
            df['Gain/Loss'] = gains_losses
            
            st.dataframe(df)
            
            total_value = df['Current Value'].sum()
            total_gain_loss = df['Gain/Loss'].sum()
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total Portfolio Value", f"${total_value:,.2f}")
            with col2:
                st.metric("Total Gain/Loss", f"${total_gain_loss:,.2f}")
        else:
            st.info("No stocks in portfolio yet. Add some using the sidebar!")
        conn.close()

if __name__ == "__main__":
    main()
