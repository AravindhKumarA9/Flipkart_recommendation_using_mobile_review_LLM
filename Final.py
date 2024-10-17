import streamlit as st  # Import streamlit module
import pandas as pd
import pickle

# Load the pickle file containing LangChain results (if applicable, this is just a placeholder in this code)
with open("most_recommended_mobile_phones.pkl", 'rb') as f:
    df = pickle.load(f)

# List of Mobile_data to choose from - mobile prices, brands, ratings, and images
Mobile_data = {
    'Mobile_Brand': ['Samsung Galaxy', 'Samsung Galaxy', 'OnePlus', 'Motorola', "Google", "Nothing", "Realme"], # brand information
    'Model': ['Galaxy S21 FE', 'Galaxy S23 5G', '11R 5G', 'Edge 40 5G', 'Pixel 7', 'Nothing Phone (2)', '12 Pro+ 5G'],
    'Price': ['₹34,999', '₹39,999', '₹37,988', '₹26,999', '₹36,999', '₹38,999', '₹26,999'], # price in INR
    'Rating': [4.3, 4.6, 4.5, 4.3, 4.3, 4.4, 4.4],
    'image': [
        'https://rukminim2.flixcart.com/image/312/312/xif0q/mobile/z/j/v/galaxy-s21-fe-5g-sm-g990blv4ins-samsung-original-imah3nhk5c4dncfm.jpeg?q=70',
        'https://rukminim2.flixcart.com/image/312/312/xif0q/mobile/8/v/0/-original-imah5ywfebrs9bfg.jpeg?q=70',
        'https://rukminim2.flixcart.com/image/312/312/xif0q/mobile/6/x/a/11r-5g-5011102525-oneplus-original-imagn3afeqfr6acy.jpeg?q=70',
        'https://rukminim2.flixcart.com/image/312/312/xif0q/mobile/2/m/o/edge-40-pay40030in-motorola-original-imagpqzchzhg6fex.jpeg?q=70',
        'https://rukminim2.flixcart.com/image/312/312/xif0q/mobile/g/x/9/-original-imaggsudg5fufyte.jpeg?q=70',
        'https://rukminim2.flixcart.com/image/312/312/xif0q/mobile/i/s/b/-original-imagrdefh2xgenzz.jpeg?q=70',
        'https://rukminim2.flixcart.com/image/312/312/xif0q/mobile/z/f/g/-original-imagxhd5gqhzszeb.jpeg?q=70'
    ]  # image URLs
}

# Create a DataFrame for visualization
df1 = pd.DataFrame(Mobile_data)

# Remove '₹' symbol and commas from the 'Price' column and convert it to integer
df1['Price'] = df1['Price'].replace({'₹': '', ',': ''}, regex=True).astype(int)

# Streamlit Title of the app
st.title('Mobile Product Recommendations')
st.write("### Based on sentiment analysis from Reviews:")

# Sidebar for filtering options
st.sidebar.header('Filter Options')

# Multiselect for multiple Brand selection
brand_options = df1['Mobile_Brand'].unique().tolist()  # Get unique brands from the data
# selected_brands = st.sidebar.multiselect("Select Multiple Brands:", options=brand_options)
selected_brands = st.sidebar.multiselect("Select Brands:", options=brand_options) #, default=brand_options)  # Default selects all brands

# Price filter slider
min_price, max_price = st.sidebar.slider('Select price range (in INR):', min_value=20000, max_value=50000, value=(20000, 50000))

# Rating filter slider
min_rating = st.sidebar.slider('Select minimum rating', min_value=0.0, max_value=5.0, value=3.0)

# Filter data based on user input
if selected_brands:  # Check if any brands are selected
    filtered_data = df1[(df1['Price'] >= min_price) & (df1['Price'] <= max_price) & (df1['Rating'] >= min_rating)]
    filtered_data = filtered_data[filtered_data['Mobile_Brand'].isin(selected_brands)]
    st.write(f'Showing results for products priced between ₹{min_price} and ₹{max_price} with rating above {min_rating}')     # Display the filtered data
    
    if filtered_data.empty:
        st.write("No products found matching the selected criteria.")
    else:
        st.subheader(f"You Selected : {', '.join(selected_brands)} Brands")  # Show selected brands
        # st.write(filtered_data)

        # Display individual recommendations
        for i, row in filtered_data.iterrows():
            st.subheader(f"**{row['Mobile_Brand']} {row['Model']}**")
            st.image(row['image'], width=150)  # Display the image
            st.write(f"Price: ₹{row['Price']}")
            st.write(f"Rating: {row['Rating']} ⭐")
            st.write("---")
else:
    st.write("No brand selected yet.")  # Message when no brands are selected
# streamlit run Final.py

# Dictionary of phone prices and image URLs
# phones = {
#     "Samsung Galaxy S21 FE": {"price": "₹34,999", "image": "https://rukminim2.flixcart.com/image/312/312/xif0q/mobile/z/j/v/galaxy-s21-fe-5g-sm-g990blv4ins-samsung-original-imah3nhk5c4dncfm.jpeg?q=70"}}

# Display phone prices and images
# for phone, details in phones.items():
#     st.subheader(phone)
#     st.image(details["image"], caption=f"Price: {details['price']}")