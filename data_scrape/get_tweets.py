import asyncio
import csv
import time
import pandas as pd

from twscrape import API, gather
from twscrape.logger import set_log_level

# async def get_club_tweets(user_id, api):
#     """Retrieves tweets by a given (parent) club account, returns a dataframe"""
#     tweets = []

#     async for tweet in api.user_tweets_and_replies(user_id, 
#                                                    limit=-1,
#                                                    kv={
#                                                        "includePromotedContent": False,
#                                                        "count": 50
#                                                    }):
#         tweets.append({
#                 "datetime": tweet.date, 
#                 "club_handle": tweet.user.username,
#                 "tweet_id": tweet.id,
#                 "tweet": tweet.rawContent
#             })
        
#     return pd.DataFrame(tweets)

# async def get_all_club_tweets(club_info):

#     api = API()

#     club_handles = club_info["handle"]
#     club_ids = club_info["id"]

#     all_club_tweets = pd.DataFrame(columns=["datetime",
#                                             "club_handle",
#                                             "tweet_id",
#                                             "tweet"])

#     for club_handle, club_id in zip(club_handles, club_ids):
#         club_tweets = get_club_tweets(club_id, api)

#         time.sleep(225)

#         # remove tweets that are *not* from the club account
#         club_tweets = club_tweets[club_tweets["club_handle"] == club_handle]
#         # add to all clubs df
#         all_club_tweets = pd.concat([all_club_tweets, club_tweets])
    
#     return all_club_tweets

async def get_club_tweets(handle, 
                          start_date,
                          end_date,
                          list_id):
    api = API()
    tweets = []

    q = f"{handle} since:{start_date} until:{end_date} list:1831730060866318808"
    async for tweet in api.search(q, limit=1000):
        tweets.append({
            "datetime": tweet.date, 
            "club_handle": tweet.user.username,
            "tweet_id": tweet.id,
            "tweet": tweet.rawContent
        })

    return pd.DataFrame(tweets)

if __name__ == "__main__":

    # club_info = pd.read_csv("ACCOUNTS.csv")
    # all_tweets = get_all_club_tweets(club_info=club_info)
    # all_tweets.to_csv("PARENT_TWEETS.csv", index=False)
    # api = API()
    # tweets = asyncio.run(get_club_tweets(user_id=121402638, api=api))
    tweets = asyncio.run(get_club_tweets(handle="spursofficial", start_date="2023-08-11", end_date="2024-05-19"))
    tweets.to_csv("QUERIED_TWEETS.csv", index=False)
    # tweets = pd.read_csv("QUERIED_TWEETS.csv")
    # tweets = tweets[tweets["club_handle"].str.lower() == "spursofficial"]
    # tweets.to_csv("QUERIED_TWEETS.csv", index=False)

# nvm the above, do it w queries instead - like from: account_name, date range
# from:SpursOfficial since:2023-08-11 until:2024-05-19
