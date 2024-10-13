import streamlit as st  # Import streamlit module
import pandas as pd

# List of Mobile_data to choose from - mobile prices, brands, and ratings
Mobile_data = {
    'Mobile_Brand': ['OnePlus', 'Samsung Galaxy', 'Samsung Galaxy', 'Motorola', "Google", "Realme", "Nothing"], # brand information
    'Model': ['Edge 40 5G', 'Galaxy S23 5G', '11R 5G', 'Galaxy S21 FE', 'Pixel 7', 'Nothing Phone (2)', '12 Pro+ 5G'],
    'Price': [29999, 31999, 35999, 38999, 34999, 39999, 36999], # price in INR
    'Rating': [4.3, 4.2, 4.1, 4.4, 4.7, 4.7, 4.5]
}

# Create a DataFrame for visualization
df1 = pd.DataFrame(Mobile_data)

# Streamlit Title of the app
st.title('Mobile Product Recommendations')
st.write("### Based on sentiment analysis from Reviews:")

# Sidebar for filtering options
st.sidebar.header('Filter Options')

# Multiselect for multiple Brand selection
brand_options = df1['Mobile_Brand'].unique().tolist()  # Get unique brands from the data
selected_brands = st.sidebar.multiselect("Select Multiple Brands:", options=brand_options) #, default=brand_options)  # Default selects all brands

# Price filter slider
min_price, max_price = st.sidebar.slider('Select price range (in INR):', min_value=20000, max_value=50000, value=(20000, 50000))

# Rating filter slider
min_rating = st.sidebar.slider('Select minimum rating', min_value=0.0, max_value=5.0, value=3.0)

# Filter data based on user input
if selected_brands:  # Check if any brands are selected
    filtered_data = df1[(df1['Price'] >= min_price) & (df1['Price'] <= max_price) & (df1['Rating'] >= min_rating)]
    filtered_data = filtered_data[filtered_data['Mobile_Brand'].isin(selected_brands)]
    st.write("You selected the following brands:")
    
    for brand in selected_brands:
        st.write(f"- {brand}")

    # Display the filtered data
    st.subheader(f'Showing results for products priced between ₹{min_price} and ₹{max_price} with rating above {min_rating}')
    
    if filtered_data.empty:
        st.write("No products found matching the selected criteria.")
    else:
        st.write(f"Selected Brands: {', '.join(selected_brands)}")  # Show selected brands
        st.write(filtered_data)

        # Display individual recommendations
        for i, row in filtered_data.iterrows():
            st.write(f"**{row['Mobile_Brand']}** (Model: {row['Model']})")
            st.write(f"Price: ₹{row['Price']}, Rating: {row['Rating']} ⭐")
            st.write("---")
else:
    st.write("No brand selected yet.")  # Message when no brands are selected
# streamlit run phone_recommendation.py