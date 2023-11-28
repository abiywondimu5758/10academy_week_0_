import os
import sys
import glob
import json
import datetime
from collections import Counter
from collections import Counter

import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
from nltk.corpus import stopwords


def break_combined_weeks(combined_weeks):
    """
    Breaks combined weeks into separate weeks.

    Args:
        combined_weeks: list of tuples of weeks to combine

    Returns:
        tuple of lists of weeks to be treated as plus one and minus one
    """
    plus_one_week = []
    minus_one_week = []

    for week in combined_weeks:
        if week[0] < week[1]:
            plus_one_week.append(week[0])
            minus_one_week.append(week[1])
        else:
            minus_one_week.append(week[0])
            plus_one_week.append(week[1])

    return plus_one_week, minus_one_week


def get_msgs_df_info(df):
    msgs_count_dict = df.user.value_counts().to_dict()
    replies_count_dict = dict(Counter([u for r in df.replies if r != None for u in r]))
    mentions_count_dict = dict(Counter([u for m in df.mentions if m != None for u in m]))
    links_count_dict = df.groupby("user").link_count.sum().to_dict()
    return msgs_count_dict, replies_count_dict, mentions_count_dict, links_count_dict


# def get_messages_dict(msgs):
#     msg_list = []
#     for msg in msgs:
#         for m in msg:
#             message_type = m.get("subtype", "message")
#             message_content = m.get("text", None)
#             sender_name = m.get("user", None)
#             time_sent = m.get("ts", None)
#             message_distribution = "channel_join" if message_type == "channel_join" else "message"

#             msg_dict = {
#                 "message_type": message_type,
#                 "message_content": message_content,
#                 "sender_name": sender_name,
#                 "time_sent": time_sent,
#                 "message_distribution": message_distribution,
#                 "time_thread_start": m["ts"] if "parent_user_id" in m else None,
#                 "reply_count": len(m["replies"]) if "thread_ts" in m and "reply_users" in m else None,
#                 "reply_user_count": len(m["reply_users"]) if "thread_ts" in m and "reply_users" in m else None,
#                 "time_thread_end": m["ts"] if "thread_ts" in m and "reply_users" in m else None,
#                 "reply_users": m["reply_users"] if "thread_ts" in m and "reply_users" in m else None,
#                 "blocks": [],
#                 "emojis": [],
#                 "mentions": [],
#                 "links": [],
#                 "link_count": 0
#             }

#             if "blocks" in m and m["blocks"] is not None:
#                 emoji_list = []
#                 mention_list = []
#                 links = []

#                 for blk in m["blocks"]:
#                     if "elements" in blk:
#                         for elm in blk["elements"]:
#                             if "elements" in elm:
#                                 for elm_ in elm["elements"]:
#                                     if "type" in elm_:
#                                         if elm_["type"] == "emoji":
#                                             emoji_list.append(elm_["name"])
#                                         elif elm_["type"] == "user":
#                                             mention_list.append(elm_["user_id"])
#                                         elif elm_["type"] == "link":
#                                             links.append(elm_["url"])

#                 msg_dict["emojis"] = emoji_list
#                 msg_dict["mentions"] = mention_list
#                 msg_dict["links"] = links
#                 msg_dict["link_count"] = len(links)

#             msg_list.append(msg_dict)

#     return msg_list


def from_msg_get_replies(msg):
    replies = []
    if "thread_ts" in msg and "replies" in msg:
        try:
            for reply in msg["replies"]:
                reply["thread_ts"] = msg["thread_ts"]
                reply["message_id"] = msg["client_msg_id"]
                replies.append(reply)
        except:
            pass
    return replies


def get_messages_df(msgs):
    msg_list = []

    for msg in msgs:
        for m in msg:
            message_type = m.get("subtype", "message")
            message_content = m.get("text", None)
            sender_name = m.get("user", None)
            time_sent = m.get("ts", None)
            message_distribution = "channel_join" if message_type == "channel_join" else "message"

            msg_dict = {
                "message_type": message_type,
                "message_content": message_content,
                "sender_name": sender_name,
                "time_sent": time_sent,
                "message_distribution": message_distribution,
                "time_thread_start": m["ts"] if "parent_user_id" in m else None,
                "reply_count": len(m["replies"]) if "thread_ts" in m and "reply_users" in m else 0,
                "reply_user_count": len(m["reply_users"]) if "thread_ts" in m and "reply_users" in m else 0,
                "time_thread_end": m["ts"] if "thread_ts" in m and "reply_users" in m else None,
                "reply_users": m["reply_users"] if "thread_ts" in m and "reply_users" in m else None,
                "blocks": [],
                "emojis": [],
                "mentions": [],
                "links": [],
                "link_count": 0
            }

            if "blocks" in m and m["blocks"] is not None:
                emoji_list = []
                mention_list = []
                links = []

                for blk in m["blocks"]:
                    if "elements" in blk:
                        for elm in blk["elements"]:
                            if "elements" in elm:
                                for elm_ in elm["elements"]:
                                    if "type" in elm_:
                                        if elm_["type"] == "emoji":
                                            emoji_list.append(elm_["name"])
                                        elif elm_["type"] == "user":
                                            mention_list.append(elm_["user_id"])
                                        elif elm_["type"] == "link":
                                            links.append(elm_["url"])

                msg_dict["emojis"] = emoji_list
                msg_dict["mentions"] = mention_list
                msg_dict["links"] = links
                msg_dict["link_count"] = len(links)

            msg_list.append(msg_dict)

    df = pd.DataFrame(msg_list)
    return df


def get_users_df(users):
    df = pd.json_normalize(users)
    columns = ['id', 'team_id', 'name', 'deleted', 'color', 'real_name', 'tz',
               'tz_label', 'tz_offset', 'is_admin', 'is_owner', 'is_primary_owner',
               'is_restricted', 'is_ultra_restricted', 'is_bot', 'is_app_user', 'profile.title', 'profile.phone', 'profile.skype', 'profile.real_name',
               'profile.display_name', 'profile.status_text',
               'profile.image_original', 'profile.email', 'profile.first_name', 'profile.last_name']
    return df[columns]


def get_channels_df(channels):
    df = pd.json_normalize(channels)
    columns = ['id', 'name', 'created', 'creator', 'is_general',
               'members']
    return df[columns]


def process_msgs(msg):
    '''
    select important columns from the message
    '''

    keys = ["client_msg_id", "type", "text", "user", "ts", "team",
            "thread_ts", "reply_count", "reply_users_count"]
    msg_list = {k: msg[k] for k in keys}
    rply_list = from_msg_get_replies(msg)

    return msg_list, rply_list


def get_messages_from_channel(channel_path):
    '''
    get all the messages from a channel        
    '''
    channel_json_files = os.listdir(channel_path)
    channel_msgs = [json.load(open(channel_path + "/" + f)) for f in channel_json_files]

    df = pd.concat([get_messages_df(msgs) for msgs in channel_msgs])
    print(f"Number of messages in channel: {len(df)}")

    return df


def convert_2_timestamp(column, data):
    """convert from unix time to readable timestamp
        args: column: columns that needs to be converted to timestamp
                data: data that has the specified column
    """
    if column in data.columns.values:
        timestamp_ = []
        for time_unix in data[column]:
            if time_unix == 0:
                timestamp_.append(0)
            else:
                a = datetime.datetime.fromtimestamp(float(time_unix))
                timestamp_.append(a.strftime('%Y-%m-%d %H:%M:%S'))
        return timestamp_
    else:
        print(f"{column} not in data")
