import streamlit as st
import praw
from nltk.sentiment import SentimentIntensityAnalyzer
from datetime import datetime, timedelta

# Stored the username and password for reddit api in local files. Below codes to read files from local files.
with open('pw.txt', "r") as f:
          pw = f.read()

with open('usn.txt', "r") as f1:
          user_name = f1.read()

# Initializing the Reddit API
reddit = praw.Reddit(
    client_id = "zm5vqm_fuC2H5AHZonul0Q",
    client_secret = "yvLVMvkqKxh-mo3GSNEdHxxMXbz0sA",
    user_agent = "demo_app by u/Legitimate-Advisor30",
    user_name = user_name,
    password = pw,
)

# Initializing the  sentiment analyzer
sid = SentimentIntensityAnalyzer()

# Below function for sentiment classification based on polarity scores.
def classify_sentiment(score):
    if score >= 0.05:
        return "Positive"
    elif score <= -0.05:
        return "Negative"
    else:
        return "Neutral"

def main():
    st.title("Sentiment Analyzer for Reddit APP-Comments ")

    subreddit_name = st.text_input("Enter subreddit name", value='flask')
    time_filter = st.selectbox("Select the filter for Time-Range", ["hour", "day", "week", "month", "year"])

    if st.button("Retrieve the Top 25 Comments for the selected Filter Button "):
        subreddit = reddit.subreddit(subreddit_name)
        comments = subreddit.comments(limit=25)  

        filtered_comments = []

        # Below codes for Applying the time-range filter and sentiment analysis.
        current_time = datetime.now()
        st.markdown("## Top 25 Comments:")
        for comment in comments:
            created_time = datetime.fromtimestamp(comment.created_utc)
            if time_filter == "hour" and (current_time - created_time) > timedelta(hours=1):
                continue
            elif time_filter == "day" and (current_time - created_time) > timedelta(days=1):
                continue
            elif time_filter == "week" and (current_time - created_time) > timedelta(weeks=1):
                continue
            elif time_filter == "month" and (current_time - created_time).days > 30:
                continue
            elif time_filter == "year" and (current_time - created_time).days > 365:
                continue

            sentiment_score = sid.polarity_scores(comment.body)['compound']
            sentiment_class = classify_sentiment(sentiment_score)

            filtered_comments.append({
                'text': comment.body,
                'polarity_score': sentiment_score,
                'classification': sentiment_class
            })

        # Below codes for Sorting the comments based on polarity scores.
        filtered_comments.sort(key=lambda x: x['polarity_score'], reverse=True)

        # Below codes for Displaying the filtered and sorted comments.
        st.markdown(f"# Top 25 Comments for {subreddit_name} Filtered by {time_filter.capitalize()} and Sorted by Polarity Scores:")
        for comment_data in filtered_comments[:25]:  # Displaying the top 25 comments
            st.write(f"- **Text**: {comment_data['text']}")
            st.write(f"  **Polarity Score**: {comment_data['polarity_score']:.2f}, **Classification**: {comment_data['classification']}")
            st.write("---")

if __name__ == '__main__':
    main()
