# Aug. 28 Meeting Notes

## My summer project
Main project was a web application that we called SKLZ Quantifier. Essentially had 3 aims: 

1. To quantify and visualize the team's competencies and deficiencies
2. To assign employees to projects such that key requirements are fulfilled
3. To recommend skillsets of future hires by looking into the team's future project backlog

Leveraged Mixtral-8x22b in 2 ways:
1. When a project description or proposal is entered by a manager, it is sent to the LLM so that it can extract the skill categories required for this project and how important they are on a scale of 1-5
2. We originally had a bunch of individual skills like "Python programming" or "Git"; we embedded each skill, clustered using HDBSCAN, and then passed each cluster to the LLM so that it could come up with an adequate skill category name

Didn't really touch on the actual structure / construction / fine-tuning of LLMs; it was mainly just prompt engineering, which seems relevant in that first paper.

## Thoughts on papers

### Do they mean "us"?

I really liked this one and of the few papers I've gone over, this would be the one I'm most willing to further pursue. It was the easiest to understand for me and I think that my skill level would most fit this project. 

My main thoughts about potential pathways to go with this are: 
* I would love to explore intergroup bias in other sports fandoms - mainly the Premier League for me, but I'm of course open-minded to others. 
* In addition to exploring a different sport, I was also wondering if perhaps cultural differences manifest in intergroup biases, and if so, how. Specifically, I'd be interested to see if members of individualist cultures may perhaps express stronger connections to their in-group while being harsher towards their out-group, and if members of collectivist cultures are less hostile towards their out-group. Is intergroup bias more subtle in collectivist cultures?
* Wonder if it is feasible to use tweets instead of Reddit posts. Might be a reach, and would be better to utlize the Reddit tools that have already been built for this paper for future steps.

My questions: 
1. What are the lab's future plans for this project? Are they actively working on it, and if so, in what way would I contribute?
2. Related, who would I be working most closely with if I choose this project?

### How people talk about each other

I liked this, but it didn't pique my interest as much as the other. Might inherently be because I am not super into politics, but I'm also not too sure about the emotion component. Feel like it is hard to glean a ton of emotion from tweets by political leaders, as was mentioned in the paper. 

I might be interested in extending this to actual laypeople instead of the political leaders, but obviously that comes with the problem that political alignment is not often available or stated, and would instead be mainly inferred or assumed.

## General questions
1. I am supposed to give you this form to fill out before I can register for the undergrad research class (hopefully I have the right one, it is LIN 357)
2. Time commitment per week - do I work on it independently somewhere and just meet w you every once in a while? Or is there a dedicated time slot that I'm supposed to fit it in?

## NOTES

* Clean up the idea some more, present on Thursday to get more perspectives and advice on approaches
* Look closely into the repo of live win probabilities
* Try and replicate the format of the NFL dataset
* Probably scrape from Reddit, not Twitter. And from all teams, by subreddit. 
    * A thought I had just now - some of the smaller clubs may not have very active subreddits, or maybe they don't have subreddits at all, so just try and include the ones that are there