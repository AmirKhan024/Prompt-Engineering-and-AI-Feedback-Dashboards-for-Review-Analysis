import streamlit as st
import json
import os
import pandas as pd
from datetime import datetime
from groq import Groq
from dotenv import load_dotenv
import plotly.express as px
import plotly.graph_objects as go

load_dotenv()

st.set_page_config(page_title="Admin Dashboard", page_icon="📊", layout="wide")

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

DATA_FILE = "../data/reviews.json"

def load_reviews():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return []

def generate_summary(review_text):
    prompt = f"""Summarize the following customer review in one concise sentence:

"{review_text}"

Respond with the summary only, no extra text."""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=100
        )
        return response.choices[0].message.content.strip()
    except:
        return "Unable to generate summary"

def generate_actions(rating, review_text):
    prompt = f"""Based on a {rating}-star review with the following text:

"{review_text}"

Suggest 2-3 specific action items for management. Be concise.

Respond with plain text, one action per line."""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
            max_tokens=150
        )
        return response.choices[0].message.content.strip()
    except:
        return "Follow up with customer"

st.title("Admin Dashboard")
st.subheader("Review Management System")

reviews = load_reviews()

if st.button("Refresh Data"):
    st.rerun()

if len(reviews) > 0:
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Reviews", len(reviews))
    
    with col2:
        avg_rating = sum(r['rating'] for r in reviews) / len(reviews)
        st.metric("Average Rating", f"{avg_rating:.2f} ⭐")
    
    with col3:
        positive = sum(1 for r in reviews if r['rating'] >= 4)
        st.metric("Positive Reviews", f"{positive} ({positive/len(reviews)*100:.0f}%)")
    
    with col4:
        negative = sum(1 for r in reviews if r['rating'] <= 2)
        st.metric("Negative Reviews", f"{negative} ({negative/len(reviews)*100:.0f}%)")
    
    st.markdown("---")
    
    # Rating Distribution Chart
    rating_counts = pd.Series([r['rating'] for r in reviews]).value_counts().sort_index()
    fig1 = px.bar(x=rating_counts.index, y=rating_counts.values,
                 labels={'x': 'Star Rating', 'y': 'Count'},
                 title="Rating Distribution")
    st.plotly_chart(fig1, use_container_width=True)
    
    st.markdown("---")
    st.subheader("All Submissions")
    
    for idx, review in enumerate(reversed(reviews)):
        with st.expander(f"Review #{len(reviews)-idx} - {'⭐' * review['rating']} - {review['timestamp'][:10]}"):
            
            col_review, col_summary = st.columns([2, 1])
            
            with col_review:
                st.write("**Customer Review:**")
                st.write(review['review'])
                
                st.write("**AI Response Sent:**")
                st.info(review['ai_response'])
            
            with col_summary:
                st.write("**AI Summary:**")
                if 'summary' not in review:
                    summary = generate_summary(review['review'])
                    review['summary'] = summary
                    with open(DATA_FILE, 'w') as f:
                        json.dump(reviews, f, indent=2)
                else:
                    summary = review['summary']
                st.success(summary)
                
                st.write("**Recommended Actions:**")
                if 'actions' not in review:
                    actions = generate_actions(review['rating'], review['review'])
                    review['actions'] = actions
                    with open(DATA_FILE, 'w') as f:
                        json.dump(reviews, f, indent=2)
                else:
                    actions = review['actions']
                st.warning(actions)

else:
    st.info("No reviews submitted yet. Waiting for customer feedback...")

st.markdown("---")
st.caption("Dashboard updates in real-time as new reviews are submitted")
