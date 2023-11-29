import pandas as pd
from dotenv import load_dotenv
import os
from pymongo import MongoClient
from loader import SlackDataLoader
import utils


load_dotenv()

mongo_url = os.getenv("DATABASE_URL")



data_path = 'C:/Users/Abiy/Documents/Projects/10 Academy/10academy_week_0_/anonymized'


loader = SlackDataLoader(data_path)

def combining_all_channel_messages():
    # List of channels
    channels = loader.get_channels()
    channel_df = utils.get_channels_df(channels)

    names_list = channel_df['name'].tolist()

    # Combining the channels
    dfs = []

    for name in names_list:
        # Get channel messages
        channel_messages = loader.get_channel_messages(name)
        
        # Get DataFrame for channel messages
        channel_df = utils.get_messages_df(channel_messages)
        
        # Add a new column for the channel name
        channel_df['channel_name'] = name

        # Append the channel_df to the combined_df
        dfs.append(channel_df)

    combined_df = pd.concat(dfs, ignore_index=True)
    list_of_dicts = combined_df.to_dict(orient='records')
    return list_of_dicts

try:
    # Connect to MongoDB
    client = MongoClient(mongo_url)

    # Check if the connection is successful
    if client:
        print('MongoDB connection successful')

    # Select or create a database
    db = client["slack_workspace_db"]

    # Select or create a database
    db = client["slack_workspace_db"]

    # Function to get or create a workspace collection
    def get_workspace_collection(workspace_name):
        return db[workspace_name]

    # Workspace 1
    workspace_1_name = "workspace_1"
    workspace_1 = get_workspace_collection(workspace_1_name)
    users_collection_1 = workspace_1["users"]
    channels_collection_1 = workspace_1["channels"]
    messages_collection_1 = workspace_1["messages"]

    # Workspace 2
    workspace_2_name = "workspace_2"
    workspace_2 = get_workspace_collection(workspace_2_name)
    users_collection_2 = workspace_2["users"]
    channels_collection_2 = workspace_2["channels"]
    messages_collection_2 = workspace_2["messages"]


    # Storing my data
    users_collection_1.insert_many(loader.users)
    channels_collection_1.insert_many(loader.channels)
    messages_collection_1.insert_many(combining_all_channel_messages())

except Exception as e:
    print(f"Error connecting to MongoDB: {e}")



