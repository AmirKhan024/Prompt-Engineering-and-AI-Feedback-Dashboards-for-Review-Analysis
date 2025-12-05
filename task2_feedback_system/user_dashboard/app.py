import streamlit as st
import json
import os
from datetime import datetime
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Review Feedback System", page_icon="⭐", layout="centered")

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

DATA_FILE = "../data/reviews.json"

def load_reviews():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return []

def save_review(review_data):
    reviews = load_reviews()
    reviews.append(review_data)
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, 'w') as f:
        json.dump(reviews, f, indent=2)

def generate_ai_response(rating, review_text):
    prompt = f"""You are a customer service assistant. A user has submitted a review with {rating} stars and the following text:

"{review_text}"

Generate a professional, empathetic response thanking them for their feedback. Keep it brief and appropriate to their rating.

Respond in plain text only, no JSON."""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=150
        )
        return response.choices[0].message.content.strip()
    except:
        return "Thank you for your feedback. We appreciate you taking the time to share your experience with us."

st.title("Customer Feedback System")
st.write("Share your experience with us")

rating = st.select_slider(
    "How would you rate your experience?",
    options=[1, 2, 3, 4, 5],
    value=3,
    format_func=lambda x: "⭐" * x
)

review_text = st.text_area(
    "Tell us about your experience",
    placeholder="Share your thoughts here...",
    height=150
)

if st.button("Submit Review", type="primary"):
    if review_text.strip():
        ai_response = generate_ai_response(rating, review_text)
        
        review_data = {
            "timestamp": datetime.now().isoformat(),
            "rating": rating,
            "review": review_text,
            "ai_response": ai_response
        }
        
        save_review(review_data)
        
        st.success("Thank you for your review!")
        st.write("**Our Response:**")
        st.info(ai_response)
    else:
        st.error("Please write a review before submitting.")

st.markdown("---")
st.caption("Your feedback helps us improve our service")
