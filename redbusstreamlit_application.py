import mysql.connector
import pandas as pd
import streamlit as st

# Connect to MySQL
conn = mysql.connector.connect(
    user='root',
    password='Madhu@29',
    host='localhost',
    database='redbus'
)

# Query data
def fetch_data():
    query = "SELECT * FROM bus_values5;"  # Replace 'bus_values5' with your actual table name
    df = pd.read_sql_query(query, conn)
    return df

# Fetch data from SQL database
df = fetch_data()

# Function to filter data based on user inputs
def filter_data(df, bus_types, route_name, prices, star_ratings ):
    if not bus_types:
        bus_types = df['bus_types'].unique()
    if not route_name:
        route_name = df['route_name'].unique()
    #if not seats:
        #seats = df['seats'].unique()

    filtered_df = df[
        (df['bus_types'].isin(bus_types)) &
        (df['route_name'].isin(route_name)) &
        (df['prices'].between(prices[0], prices[1])) &
        (df['star_ratings'] >= star_ratings)
        #(df['seats'].isin(seats))
    ]
    return filtered_df

# Streamlit application starts here
def main():
    st.title('Redbus Data Analysis')

    # Sidebar filters
    st.sidebar.header('Filters')

    # Multi-select for bus types
    selected_bustypes = st.sidebar.multiselect('Select Bus Types', df['bus_types'].unique())

    # Multi-select for routes
    selected_routes = st.sidebar.multiselect('Select Routes', df['route_name'].unique())

    # Price range slider
    min_price, max_price = float(df['prices'].min()), float(df['prices'].max())
    price_range = st.sidebar.slider('Price Range', min_price, max_price, (min_price, max_price))

    # Star rating filter
    min_star_rating, max_star_rating = float(df['star_ratings'].min()), float(df['star_ratings'].max())
    star_rating = st.sidebar.slider('Minimum Star Rating', min_star_rating, max_star_rating, min_star_rating)

    # Checkbox for availability
   # seats_options = ['Yes', 'No']
    #selected_availability = st.sidebar.multiselect('Available Buses', seats_options)

    # Print filter values for debugging
    #st.write("Bus Types Selected:", selected_bustypes)
    #st.write("Routes Selected:", selected_routes)
    #st.write("Price Range Selected:", price_range)
    #st.write("Star Rating Selected:", star_rating)
    # Apply filters and display results
    filtered_data = filter_data(df, selected_bustypes, selected_routes, price_range, star_rating)

    st.subheader('Filtered Bus Tickets')
    st.dataframe(filtered_data)

if __name__ == '__main__':
    main()

# Close the connection when done
conn.close()