import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean
from sqlalchemy.orm import declarative_base

from sqlalchemy.orm import sessionmaker

load_dotenv()

DATABASE_URL = os.getenv("POSTGRE_URL")

engine = create_engine(str(DATABASE_URL))
Base = declarative_base()

class MLFeature(Base):
    __tablename__ = 'ml_features'

    id = Column(Integer, primary_key=True, index=True)
    sender_name = Column(String, index=True)  
    msg_sent_in_threads = Column(Integer)
    top_sender = Column(Boolean)
    bottom_sender = Column(Boolean)
    avg_reply_count = Column(Float)
    avg_reply_users_count = Column(Float)
    user_with_most_reactions = Column(String)
    wordcloud_image_path = Column(String)
    message_category = Column(String)
    topics_extracted = Column(String)
    reactions_for_topics = Column(String)
    distribution_of_messages_across_hours = Column(String)
    time_diff_message_histogram_path = Column(String)
    time_diff_reply_histogram_path = Column(String)
    time_diff_reaction_histogram_path = Column(String)
    time_diff_event_histogram_path = Column(String)
    accuracy = Column(Float)
    num_topics = Column(Integer)
    sentiment_over_time_plot_path = Column(String)

Base.metadata.create_all(bind=engine)

# Example of inserting data
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = Session()
ml_feature_data = [
    {
        'sender_name': 'John Doe',
        'msg_sent_in_threads': 100,
        'top_sender': True,
        'bottom_sender': False,
        'avg_reply_count': 2.5,
        'avg_reply_users_count': 1.8,
        'user_with_most_reactions': 'Alice',
        'wordcloud_image_path': r'C:\path\to\wordcloud.png',  # Use raw string or double backslashes
        'message_category': 'Question',
        'topics_extracted': 'Topic1, Topic2, Topic3',
        'reactions_for_topics': 'Topic1: 50, Topic2: 30, Topic3: 20',
        'distribution_of_messages_across_hours': '[10, 20, 30, 40]',
        'time_diff_message_histogram_path': r'C:\path\to\time_diff_message_hist.png',  # Use raw string or double backslashes
        'time_diff_reply_histogram_path': r'C:\path\to\time_diff_reply_hist.png',  # Use raw string or double backslashes
        'time_diff_reaction_histogram_path': r'C:\path\to\time_diff_reaction_hist.png',  # Use raw string or double backslashes
        'time_diff_event_histogram_path': r'C:\path\to\time_diff_event_hist.png',  # Use raw string or double backslashes
        'accuracy': 0.85,
        'num_topics': 10,
        'sentiment_over_time_plot_path': r'C:\path\to\sentiment_over_time.png',  # Use raw string or double backslashes
    },
]

for entry in ml_feature_data:
    ml_feature = MLFeature(**entry)
    session.add(ml_feature)

# Commit changes
session.commit()
