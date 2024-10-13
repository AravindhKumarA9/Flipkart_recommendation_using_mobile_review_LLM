import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

# Load the dataset
df = pd.read_csv('fiipkart_data_py.csv')

# Preprocessing function to combine relevant features for the recommendation
def combine_features(row):
    return f"{row['ram_rom']} {row['display']} {row['camera']} {row['battery']} {row['processor']}"

# Create a new column 'combined_features' for the recommendation system
df['combined_features'] = df.apply(combine_features, axis=1)

# Use TF-IDF Vectorizer to convert the text data into numeric form
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(df['combined_features'])

# Calculate the cosine similarity between phones based on their features
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# Function to recommend phones
def recommend_mobile(filtered_df, phone_name, num_recommendations=5):
    if phone_name not in filtered_df['mobile_name'].values:
        return "Phone not found in the dataset."
    
    # Get index of the phone that matches the name
    idx = filtered_df[filtered_df['mobile_name'] == phone_name].index[0]
    
    # Get similarity scores for all phones with this phone
    sim_scores = list(enumerate(cosine_sim[idx]))
    
    # Sort phones based on similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    
    # Get indices of the most similar phones
    sim_indices = [i[0] for i in sim_scores[1:num_recommendations+1]]
    
    # Return the most similar phones
    return filtered_df[['mobile_name', 'price', 'mobile_link']].iloc[sim_indices]

# Extract phone brands from mobile names
df['brand'] = df['mobile_name'].apply(lambda x: x.split()[0])

# Streamlit app to display mobile recommendations
st.title("📱 Mobile Phone Recommendation System")

# Sidebar filter options
st.sidebar.header("🔍 Filter Options")

# Input: Select a brand in the sidebar
selected_brand = st.sidebar.selectbox("Select a Brand:", df['brand'].unique())

# Filter the phones based on the selected brand
brand_phones = df[df['brand'] == selected_brand]['mobile_name'].values

# Input: Select a phone from the filtered brand in the sidebar
phone_name = st.sidebar.selectbox("Select a Mobile Phone:", brand_phones)

# Button to trigger the recommendation
if st.sidebar.button("Recommend"):
    recommendations = recommend_mobile(df, phone_name, 5)  # Set the number of recommendations to 5
    if isinstance(recommendations, str):
        st.write(recommendations)
    else:
        st.write(f"Top 5 similar phones to *{phone_name}*:")

        # Define custom CSS to create box-style clickable cards and a colorful background
        st.markdown("""
            <style>
            body {
                background-color: #f8f9fa; /* Light background */
                color: #333; /* Dark text */
            }
            .sidebar .sidebar-content {
                background-color: #007bff; /* Sidebar background color */
                color: white; /* Sidebar text color */
            }
            .card {
                background-color: #ffffff; /* Card background */
                padding: 15px;
                margin-bottom: 10px;
                border-radius: 10px;
                border: 1px solid #ddd;
                box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
                text-align: left;
                transition: transform 0.2s;
            }
            .card:hover {
                transform: scale(1.02);
                box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
            }
            </style>
        """, unsafe_allow_html=True)

        # Loop through the recommendations and display each as a clickable box
        for i, row in recommendations.iterrows():
            st.markdown(f"""
                <div class="card">
                    <h4 style="color: #007bff;">{row['mobile_name']}</h4>
                    <p>Price: <strong>${row['price']}</strong></p>
                    <a href="{row['mobile_link']}" target="_blank" style="text-decoration: none; color: #007bff;">View Product</a>
                </div>
            """, unsafe_allow_html=True)