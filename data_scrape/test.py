import asyncio
from twscrape import API, gather
from twscrape.logger import set_log_level

import pandas as pd

async def main():
    api = API()
    replies = []
    async for tweet in api.tweet_replies(twid=1740440031343644772, 
                                         limit=20):
        replies.append({
            "datetime": tweet.date,
            "tweet": tweet.rawContent,
            "user_handle": tweet.user.username,
            "likes": tweet.likeCount,
            "place": tweet.place,
            "coords": tweet.coordinates,
            "user_location": tweet.user.location
        })
    
    return pd.DataFrame(replies)

if __name__ == "__main__":
    replies = asyncio.run(main())
    replies.to_csv("test_replies.csv", index=False)