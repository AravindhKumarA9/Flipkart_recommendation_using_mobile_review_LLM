import streamlit as st
import pandas as pd
import pickle
import requests
from PIL import Image
from io import BytesIO

# Load the pickle file containing LangChain results
# with open("top_mobile_phones.pkl", 'rb') as f:
#     df = pickle.load(f)

# Add a column with mobile prices and brands
# price_data = {
#     "mobile": ["Apple iPhone 12", "Google Pixel 8", "Motorola Edge 40", "Motorola Edge 50 Pro 5G", "SAMSUNG Galaxy S23 5G", "realme 13 Pro+ 5G"],
#     "price": [35999, 38999, 34999, 31999, 39999, 36999],  # price in INR
#     "brand": ["Apple", "Google", "Motorola", "Motorola", "Samsung", "Realme"] # brand information
# } 
# price_df = pd.DataFrame(price_data)
ds = df.merge(price_df, on='mobile', how='left')

# st.title("Mobile Phone Recommendations")
# st.write("### Based on sentiment analysis from reviews:")

# Sidebar for brand selection
# brand_options = ds['brand'].unique()
# selected_brand = st.sidebar.selectbox("Select Brand:", brand_options)

# Sidebar for price range selection
# price_filter = st.sidebar.slider("Select Price Range (in INR):", min_value=30000, max_value=40000, value=(30000, 40000))

# Filter based on selected brand and price
filtered_phones = ds[
    (ds['brand'] == selected_brand) &
    (ds['price'] >= price_filter[0]) &
    (ds['price'] <= price_filter[1])]

# Show filtered results
if not filtered_phones.empty:
    for _, row in filtered_phones.iterrows():
        # Display the image of the mobile phone
        image_url = f"https://www.allerin.com/wp-blog/wp-content/uploads/2017/01/mob-apps.jpg"  # Adjust this URL as necessary
        response = requests.get(image_url)
        img = Image.open(BytesIO(response.content))

        st.image(img, caption=row['mobile'], use_column_width=True)

        # Create a prompt using the loaded recommendation template
        prompt = f"""
        Based on sentiment analysis, we recommend the following mobile phone:

        **Model**: {row['mobile']}
        - Positive review Count: {row['average_adjusted_sentiment']}
        - Price: ₹{row['price']}
        """

        st.write(prompt)
else:
    st.write("No mobile phones available in this brand and price range.")