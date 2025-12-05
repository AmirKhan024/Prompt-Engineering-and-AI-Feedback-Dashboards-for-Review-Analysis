# Prompt Engineering & AI Feedback Dashboards for Review Analysis

An end-to-end solution using Large Language Models to predict review ratings and generate intelligent feedback. Includes prompt engineering experiments and interactive dashboards for users and admins, powered by Groq Llama models.


## Setup Instructions

### Prerequisites
- Python 3.9+
- Groq API key

### Installation

1. Clone the repository
2. Create virtual environment:
```bash
python -m venv env
env\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.env` file with your Groq API key:
```
GROQ_API_KEY=your_key_here
```

## Task 1: Rating Prediction

### Running the Notebook

1. Dataset already included: `yelp.csv` (10,001 Yelp reviews)
2. Open Jupyter:
```bash
jupyter notebook task1_rating_prediction/rating_prediction.ipynb
```
3. Run all cells

### Results Summary

**Performance Comparison (200 sample reviews):**

| Approach | Accuracy | JSON Validity | Valid Samples |
|----------|----------|---------------|---------------|
| Zero-Shot | 66.50% | 100.00% | 200/200 |
| Few-Shot | 59.00% | 100.00% | 200/200 |
| Chain-of-Thought | 68.37% | 98.00% | 196/200 |

**Winner:** Chain-of-Thought Reasoning (68.37% accuracy)

### Approach Overview

**Approach 1 - Zero-Shot Direct Classification:**
Straightforward prompting without examples or structured reasoning. Achieves 66.50% accuracy with perfect JSON compliance.

**Approach 2 - Few-Shot Learning:**
Provides 5 labeled examples across all rating levels to calibrate model understanding. Surprisingly achieved lowest accuracy (59%) despite example guidance.

**Approach 3 - Chain-of-Thought Reasoning:**
Guides model through step-by-step analysis of sentiment, food quality, service, and overall experience. Best performing approach at 68.37% accuracy.

## Task 2: Feedback System

### Running User Dashboard

```bash
cd task2_feedback_system/user_dashboard
streamlit run app.py
```

Access at: http://localhost:8501

### Running Admin Dashboard

```bash
cd task2_feedback_system/admin_dashboard
streamlit run app.py --server.port 8502
```

Access at: http://localhost:8502

### Features

**User Dashboard:**
- Star rating selection (1-5)
- Review text input
- AI-generated personalized response
- Data persistence to JSON

**Admin Dashboard:**
- Live review feed
- Analytics (total reviews, average rating, sentiment breakdown)
- AI-generated summaries for each review
- AI-suggested action items for management
- Rating distribution visualization
- Expandable review cards with full details

## Technologies Used

- **Task 1 LLM:** Groq Llama 3.1 8B Instant (for rating prediction)
- **Task 2 LLM:** Groq Llama 3.3 70B Versatile (for responses & summaries)
- **Notebook:** Jupyter
- **Web Framework:** Streamlit
- **Data Processing:** Pandas, NumPy
- **Visualization:** Plotly, Matplotlib, Seaborn
- **Metrics:** Scikit-learn

## Key Achievements

- **68.37% accuracy** in zero-shot rating prediction using Chain-of-Thought prompting
- **98-100% JSON validity** across all approaches
- **Production-ready** dual dashboard system with AI-powered insights
- **Complete documentation** with technical analysis and recommendations

## Deliverables

- Task 1 notebook with 3 prompting approaches
- User dashboard for review submission
- Admin dashboard for review management
- Complete evaluation metrics and comparison
- Deployment-ready code
