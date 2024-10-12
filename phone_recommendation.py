import streamlit as st
import pandas as pd

# Sample Data with mobile prices, brands, and ratings
Mobile_data = {
    'Mobile_Brand': ['OnePlus', 'Samsung Galaxy', 'Samsung Galaxy', 'Motorola', "Google", "Realme", "Nothing"], # brand information
    'Model': ['Edge 40 5G', 'Galaxy S23 5G', '11R 5G', 'Galaxy S21 FE', 'Pixel 7', 'Nothing Phone (2)', '12 Pro+ 5G'],
    'Price': [29999, 31999, 35999, 38999, 34999, 39999, 36999], # price in INR
    'Rating': [4.3, 4.2, 4.1, 4.4, 4.7, 4.7, 4.5]
}

# Create a DataFrame for visualization
df1 = pd.DataFrame(Mobile_data)

# Streamlit App Title
st.title('Mobile Product Recommendations')
st.write("### Based on sentiment analysis from Reviews:")

# Sidebar for filtering options
st.sidebar.header('Filter Options')

# Brand selection
brand_options = ['All'] + df1['Mobile_Brand'].unique().tolist()  # Add "All" option to include all brands
selected_brand = st.sidebar.selectbox("Select Brand:", brand_options)

# Price filter slider
min_price, max_price = st.sidebar.slider('Select price range (in INR):', min_value=20000, max_value=50000, value=(20000, 50000))

# Rating filter slider
min_rating = st.sidebar.slider('Select minimum rating', min_value=0.0, max_value=5.0, value=3.0)

# Filter data based on user input
filtered_data = df1[(df1['Price'] >= min_price) & (df1['Price'] <= max_price) & (df1['Rating'] >= min_rating)]

# Filter by brand if not 'All'
if selected_brand != 'All':
    filtered_data = filtered_data[filtered_data['Mobile_Brand'] == selected_brand]

# Display the filtered data
st.subheader(f'Showing results for products priced between ₹{min_price} and ₹{max_price} with rating above {min_rating}')
if filtered_data.empty:
    st.write("No products found matching the selected criteria.")
else:
    st.write(filtered_data)

    # Display individual recommendations
    for i, row in filtered_data.iterrows():
        st.write(f"**{row['Mobile_Brand']}** (Model: {row['Model']})")
        st.write(f"Price: ₹{row['Price']}, Rating: {row['Rating']} ⭐")
        st.write("---")
