import asyncio
import time
import pandas as pd

from datetime import datetime
from twscrape import API, gather
from twscrape.logger import set_log_level

class Replyretriever:

    def __init__(self, 
                 parent_tweets_df):
        
        self.api = API()
        
        self.tweet_ids = parent_tweets_df["tweet_id"]
        self.report_ids = [self._get_report_id(rep_id) for rep_id in parent_tweets_df["match_report"]]

    def _get_report_id(self, report_url):

        return report_url.split("/")[3]
    
    async def get_tweet_replies(self, tweet_id):

        tweet_replies = []

        async for tweet in self.api.tweet_replies(twid=tweet_id, 
                                                  limit=1000,
                                                  kv={"includePromotedContent": False}):

            tweet_replies.append({
                "datetime": tweet.date,
                "tweet": tweet.rawContent,
                "id": tweet.id,
                "user_handle": tweet.user.username,
                "likes": tweet.likeCount,
                "place": tweet.place,
                "coords": tweet.coordinates,
                "user_location": tweet.user.location,
                "user_description": tweet.user.rawDescription,
                "user_followers": tweet.user.followersCount,
                "user_verified": tweet.user.verified,
                "user_blue": tweet.user.blue,
                "user_blue_type": tweet.user.blueType})
            
        return pd.DataFrame(tweet_replies)

    async def save_all_replies(self):
        
        all_replies = []

        for i, (tweet_id, report_id) in enumerate(zip(self.tweet_ids, self.report_ids), start=1): 

            tweet_replies = await self.get_tweet_replies(tweet_id=tweet_id)
            tweet_replies["report_id"] = report_id
            tweet_replies["parent_tweet_id"] = tweet_id
            all_replies.append(tweet_replies)

            print(f"{tweet_replies.shape[0]} replies added for tweet {tweet_id}")

            if i % 500 == 0: 
                print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Pausing for 150 seconds...")
                await asyncio.sleep(150)
        
        all_replies = pd.concat(all_replies)
        all_replies.to_csv("REPLIES.csv", index=False)
        print(f"COMPLETED: {all_replies.shape[0]} replies added to REPLIES.csv")

if __name__ == "__main__":

    parent_tweets = pd.read_csv("/home/jasmine/PROJECTS/research/data_scrape/PARENT_TWEETS_FILTERED.csv")
    # parent_tweets = parent_tweets[parent_tweets["tweet_id"].isin([1790501124497080569, 1790498047715086687])]
    retriever = Replyretriever(parent_tweets_df=parent_tweets)

    asyncio.run(retriever.save_all_replies())

