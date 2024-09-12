import pandas as pd
import streamlit as st
import ast

# Function to safely convert values to float
def safe_float_conversion(value):
    try:
        # If value is a string, evaluate it as a Python literal
        if isinstance(value, str):
            value = ast.literal_eval(value)
        
        # If value is a list, handle cases where the list may contain a single string or number
        if isinstance(value, list):
            if len(value) > 0:
                return float(value[0])
            else:
                return None
        
        # If value is already a number or string that can be converted
        return float(value)
    
    except (ValueError, TypeError, IndexError):
        return None

# Load data from CSV
def load_data():
    df = pd.read_csv("C:/Users/Madhu/Downloads/all_details_cleaned.csv")
    # st.write("Data Loaded Successfully")  # Confirm data loading
    # st.write(df.head())  # Display first few rows to verify
    
    # Convert relevant columns to float
    for column in ['price', 'star_rating']:
        df[column] = df[column].apply(safe_float_conversion)
    
    # Drop rows where conversion failed
    df = df.dropna(subset=['price', 'star_rating'])  
    
    if df.empty:
        st.error("Data cleaning failed. No valid data available.")
    
    return df

# Function to filter data based on user inputs
def filter_data(df, route_name, bus_type, price, star_rating, seat, state):
    if route_name:
        df = df[df['route_name'] == route_name]
    if bus_type:
        df = df[df['bus_type'] == bus_type]
    if state:
        df = df[df['state'] == state]

    min_star_rating, max_star_rating = star_rating
    filtered_df = df[
        (df['price'].between(price[0], price[1])) &
        (df['star_rating'].between(min_star_rating, max_star_rating)) &
        (df['seat'].between(seat[0], seat[1]))
    ]
    return filtered_df

# Streamlit application starts here
def main():
    st.title('Redbus Data Analysis')

    # Load data from CSV file
    df = load_data()

    if df.empty:
        st.error("No data available after cleaning.")
        return

    # Sidebar filters
    st.sidebar.header('Filters')
    
    # State filter
    states_options = df['state'].unique()
    selected_state = st.sidebar.selectbox('Select State', [None] + list(states_options))

    # Filter dataframe by selected state
    filtered_df_by_state = df[df['state'] == selected_state] if selected_state else df

    # Update route options based on selected state
    routes_options = filtered_df_by_state['route_name'].unique()
    selected_route = st.sidebar.selectbox('Select Route', [None] + list(routes_options))

    # Filter dataframe by selected route
    filtered_df_by_route = filtered_df_by_state[filtered_df_by_state['route_name'] == selected_route] if selected_route else filtered_df_by_state

    # Single select for bus types
    bus_types_options = filtered_df_by_route['bus_type'].unique()
    selected_bus_type = st.sidebar.selectbox('Select Bus Type', [None] + list(bus_types_options))

    # Price range slider
    min_price, max_price = float(filtered_df_by_route['price'].min()), float(filtered_df_by_route['price'].max())
    price_range = st.sidebar.slider('Price Range', min_price, max_price, (min_price, max_price))

    # Star rating filter
    min_star_rating, max_star_rating = float(filtered_df_by_route['star_rating'].min()), float(filtered_df_by_route['star_rating'].max())
    star_rating = st.sidebar.slider('Star Rating Range', min_star_rating, max_star_rating, (min_star_rating, max_star_rating))

    # Seat range filter
    min_seats, max_seats = int(filtered_df_by_route['seat'].min()), int(filtered_df_by_route['seat'].max())
    seat_range = st.sidebar.slider('Seats Range', min_seats, max_seats, (min_seats, max_seats))

    # Apply filters and display results
    filtered_data = filter_data(filtered_df_by_route, selected_route, selected_bus_type, price_range, star_rating, seat_range, selected_state)

    if filtered_data.empty:
        st.error("No buses found matching the selected criteria.")
    else:
        st.subheader('Filtered Bus Tickets')
        st.dataframe(filtered_data)

if __name__ == '__main__':
    main()