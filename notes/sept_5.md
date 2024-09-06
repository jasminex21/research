## Sept. 5 Group Meeting

* Suggestions (David, Jessy)
    * See if you can incorporate tweets from specific users on the tl in addition to replies to tweets
        * Potentially go through the followers of each club account, maybe choose a hundred or so of them that you are certain are not bots and are actual active fans
            * There is then the issue of determining which tweets are about the ongoing game and which are not - can use an LLM to do this; feed it examples of tweets about the game. 
                * HOWEVER, an issue I am thinking of rn is that people can tweet about other (simultaneous) games as well, so this route may not be ideal

* Misc.: 
    * Geolocation tagging of tweets allows me to work on my original idea of investigating cultural differences in the expression of intergroup bias
        * Using location as a proxy for culture
            * Venkat suggested I look into tweet language as a proxy for culture too, though I have doubts about the feasibility of that, plus a vast majority of fans tweet in English anyways regardless of where they are from
        * I haven't ran it yet (still writing the code), but it *appears* that I can get country data, and possibly even coordinates. Coordinates would be interesting.
    * Associating each tweet with a game event - time frame of a minute ish? Timestamp stuff
    * Be aware of bots - my thoughts are that if the last season's tweets contain too many bot tweets that I cannot filter out, just go back another season, though idk if that is possible API-wise. 
        * When it comes to identifying bot tweets though, one way to go about it is to see if the user is following the club, and I can also get rid of tweets that are just one-two words, since bots tend to have short tweets. Short tweets and multiple replies to the same parent tweet.