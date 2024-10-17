import streamlit as st  # Import streamlit module
import pandas as pd
import pickle

# Load the pickle file containing LangChain results (if applicable, this is just a placeholder in this code)
with open("most_recommended_mobile_phones.pkl", 'rb') as f:
    df = pickle.load(f)

# List of Mobile_data to choose from
Mobile_data = {
    'Product Name': ['Samsung Galaxy S21 FE', 'SAMSUNG Galaxy S23 5G', 'OnePlus 11R', 'Motorola Edge 40', 'Google Pixel 7', 'Nothing Phone (2)', 'Realme 12 Pro+'],
    'Price': ['₹34,999', '₹39,999', '₹37,988', '₹26,999', '₹36,999', '₹38,999', '₹26,999'],
    'Rating': [4.3, 4.6, 4.5, 4.3, 4.3, 4.4, 4.4],
    'image': [
        'https://rukminim2.flixcart.com/image/312/312/xif0q/mobile/z/j/v/galaxy-s21-fe-5g-sm-g990blv4ins-samsung-original-imah3nhk5c4dncfm.jpeg?q=70',
        'https://rukminim2.flixcart.com/image/312/312/xif0q/mobile/8/v/0/-original-imah5ywfebrs9bfg.jpeg?q=70',
        'https://rukminim2.flixcart.com/image/312/312/xif0q/mobile/6/x/a/11r-5g-5011102525-oneplus-original-imagn3afeqfr6acy.jpeg?q=70',
        'https://rukminim2.flixcart.com/image/312/312/xif0q/mobile/2/m/o/edge-40-pay40030in-motorola-original-imagpqzchzhg6fex.jpeg?q=70',
        'https://rukminim2.flixcart.com/image/312/312/xif0q/mobile/g/x/9/-original-imaggsudg5fufyte.jpeg?q=70',
        'https://rukminim2.flixcart.com/image/312/312/xif0q/mobile/i/s/b/-original-imagrdefh2xgenzz.jpeg?q=70',
        'https://rukminim2.flixcart.com/image/312/312/xif0q/mobile/z/f/g/-original-imagxhd5gqhzszeb.jpeg?q=70'
    ]
}

# Create a DataFrame for visualization
df1 = pd.DataFrame(Mobile_data)
ri = df.merge(df1, on='Product Name', how='left')

# Clean the 'Price' column in the merged DataFrame (ri)
ri['Price'] = ri['Price'].replace({'₹': '', ',': ''}, regex=True).astype(int)

# Streamlit Title of the app
st.title('Mobile Product Recommendations')
st.write("### Based on sentiment analysis from Reviews:")

# Sidebar for filtering options
st.sidebar.header('Filter Options')

# Multiselect for multiple Brand selection
brand_options = ri['Product Name'].unique().tolist()
selected_brands = st.sidebar.multiselect("Select Brands:", options=brand_options)

# Price filter slider
min_price, max_price = st.sidebar.slider('Select price range (in INR):', min_value=20000, max_value=50000, value=(20000, 50000))

# Rating filter slider
min_rating = st.sidebar.slider('Select minimum rating', min_value=0.0, max_value=5.0, value=3.0)

# Filter the DataFrame based on the user's input
filtered_phones = ri[
    (ri['Product Name'].isin(selected_brands)) &
    (ri['Price'] >= min_price) &
    (ri['Price'] <= max_price) &
    (ri['Rating'] >= min_rating)
]

# Check if the filtered data is empty
if filtered_phones.empty:
    st.write("No products found matching the selected criteria.")
else:
    st.write(f"Selected Brands: {', '.join(selected_brands)}")

    # Display individual recommendations
    for i, row in filtered_phones.iterrows():
        st.subheader(f"**{row['Product Name']}**")
        st.image(row['image'], width=150)
        st.write(f"Price: ₹{row['Price']}")
        st.write(f"Rating: {row['Rating']} ⭐")
        st.write("---")

# streamlit run i.py