import streamlit as st
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from io import BytesIO
import mlflow
from gensim import corpora, models
from textblob import TextBlob

# Load data and models
combined_df = pd.read_csv('combined_df.csv')  # Replace with your actual file path
mlflow_model_path = '../notebooks/lda_model'  # Replace with your actual run ID

# Sidebar
st.sidebar.title("Dashboard Menu")
selected_chart = st.sidebar.selectbox("Select Chart", ["Top Users", "Message Distribution", "Word Cloud"])

# Main content
st.title("Slack Analytics Dashboard")

# Display selected chart
if selected_chart == "Top Users":
    st.header("Top Users")
    # Function to get top users

    def get_top_users(data, top_n=10):
        return data['sender_name'].value_counts()[:top_n]

    top_users = get_top_users(combined_df)
    st.bar_chart(top_users)

elif selected_chart == "Message Distribution":
    st.header("Message Distribution Across Hours")
    plt.figure(figsize=(15, 7))
    sns.countplot(x='time_sent', data=combined_df)
    st.pyplot()

elif selected_chart == "Word Cloud":
    st.header("Word Cloud")
    # Function to generate word cloud

    def generate_wordcloud(text):
        wordcloud = WordCloud(width=500, height=300, background_color='white').generate(text)
        return wordcloud.to_image()

    # Combine messages for word cloud
    all_messages = ' '.join(combined_df['message_content'].dropna())
    st.image(generate_wordcloud(all_messages), use_column_width=True)

# MLflow integration
st.header("MLflow Model Info")
with st.spinner("Loading model info..."):
    # Load LDA model
    lda_model = models.LdaModel.load(mlflow_model_path)
    st.text("Number of Topics: {}".format(lda_model.num_topics))

# Download data link
st.header("Download Data")
st.markdown("[Download Combined Data](combined_df.csv)", unsafe_allow_html=True)

# Streamlit app command
if __name__ == '__main__':
    st.set_page_config(layout="wide")
    st.sidebar.title("Navigation")
    st.write("Streamlit app initialized!")
    st.sidebar.title("Navigation")
    st.sidebar.markdown("[Home](#)")
