import pandas as pd
import matplotlib.pyplot as plt

from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import cross_val_score, train_test_split

from sklearn.pipeline import Pipeline

from sklearn.feature_extraction.text import CountVectorizer

import streamlit as st


dataset = pd.read_csv("./spam.csv") 

pipeline = Pipeline([
    ('vectorize', CountVectorizer()),
    ('classification', MultinomialNB())
])


X_train, X_test, y_train, y_test = train_test_split(dataset.Message, dataset.Category, test_size=0.25)

pipeline.fit(X_train, y_train)
pipeline.predict(y_test)

accuracy = cross_val_score(pipeline, X_train, y_train, cv=10).mean()


# Web code

# Set page config
st.set_page_config(page_title="Spam Email Predictor", layout="wide", page_icon="🚫")

# Custom CSS to reduce space
st.markdown(
    """
    <style>
        .tight-text {
            margin-bottom: -20px;
        }
    </style>
""",
    unsafe_allow_html=True,
)

# Layout columns
left, center, right = st.columns([1, 2, 1])

with center:
    st.title("Spam Email Predictor")
    st.divider()

    # Custom header text with tight spacing
    st.markdown(
        """
        <div class='tight-text'>
        <h4 style='font-weight:600; margin-bottom:10px;'>
            Enter your email content below to check -
            <span style='color:#E4572E;'>Spam</span> or <span style='color:#2E8540;'>Not Spam</span>:
        </h4>
        </div>
    """,
        unsafe_allow_html=True,
    )

    # Collapsed label to remove default gap
    email = st.text_area(" ", label_visibility="collapsed", height=100)

    # Prediction logic
    if email:
        res = pipeline.predict([email])
        if res[0] == "ham" or res[0] == 0:
            st.markdown(
                "<h4 style='color:#2E8540; font-weight:600;'>Not Spam</h4>",
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                "<h4 style='color:#E4572E; font-weight:600;'>Spam</h4>",
                unsafe_allow_html=True,
            )

        plt.title("Graph (Spam vs Not Spam)")
        plt.bar(["Not Spam", "Spam"], pipeline.predict_proba([email])[0], width=0.5, color='skyblue')
        plt.xlabel("Prediction")
        plt.ylabel("Probability")
        plt.tight_layout()
        st.pyplot(plt)
    
    st.markdown("## Dataset Preview")
    st.dataframe(dataset)
    st.markdown("### Dataset Information")
    st.dataframe(dataset.groupby('Category').describe())
    st.markdown(f"### Model Accuracy : {round(accuracy*100, 4)}")
    
