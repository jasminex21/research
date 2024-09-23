import asyncio
import time
import pandas as pd

from twscrape import API, gather
from twscrape.logger import set_log_level

class Tweetretriever:

    def __init__(self, 
                 club_info,
                 start_date,
                 end_date,
                 save_filepath="TWEETS.csv"):

        self.api = API()
        self.club_handles = list(club_info["handle"])
        self.ids = list(club_info["id"])
        self.list_ids = list(club_info["list_id"])
        self.start_date = start_date
        self.end_date = end_date
        self.save_filepath = save_filepath

    async def get_club_tweets(self, 
                              handle, 
                              list_id):
        
        tweets = []
        q = f"{handle} since:{self.start_date} until:{self.end_date} list:{list_id}"

        async for tweet in self.api.search(q, limit=5000):
            tweets.append({
                "datetime": tweet.date, 
                "club_handle": tweet.user.username,
                "tweet_id": tweet.id,
                "tweet": tweet.rawContent,
                "user_location": tweet.user.location,
                "place": tweet.place
            })

        return pd.DataFrame(tweets)

    async def save_all_club_tweets(self):

        all_club_tweets = pd.DataFrame(columns=["datetime", 
                                                "club_handle",
                                                "tweet_id",
                                                "tweet"])
        
        for club_handle, list_id in zip(self.club_handles, self.list_ids): 

            club_tweets = await self.get_club_tweets(handle=club_handle, list_id=list_id)
            time.sleep(150)
            # remove tweets that are not by the club account
            club_tweets = club_tweets[club_tweets["club_handle"].str.lower() == club_handle]
            # add to all clubs df
            all_club_tweets = pd.concat([all_club_tweets, club_tweets])
            print(f"{club_tweets.shape[0]} tweets added for {club_handle}")
        
        all_club_tweets.to_csv(self.save_filepath, index=False)
        print(f"Tweets for {self.club_handles} saved to {self.save_filepath}")

if __name__ == "__main__":
    club_info = pd.read_csv("/home/jasmine/PROJECTS/research/data_scrape/ACCOUNTS.csv")
    retriever = Tweetretriever(club_info=club_info,
                               start_date="2023-08-11",
                               end_date="2024-05-19",
                               save_filepath="PARENT_TWEETS.csv")
    asyncio.run(retriever.save_all_club_tweets())