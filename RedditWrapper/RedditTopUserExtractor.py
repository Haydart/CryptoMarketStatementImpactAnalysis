import praw
import time
import pandas as pd
import datetime
from praw.models import Comment

considered_subreddits = ['crypto', 'Bitcoin', 'litecoin', 'btc', 'Cryptocurrency',
                         'CryptoMarkets', 'ethereum']





print(reddit.user.me())
submissions_per_subreddit = [reddit.subreddit(subreddit).top(limit=None) for subreddit in considered_subreddits]

crypto_submissions = submissions_per_subreddit[0] ### FOR TESTING PURPOSES ###

topics_dict = {"title": [],
               "score": [],
               "id": [],
               "url": [],
               "comms_num": [],
               "created": [],
               "body": [],
               "comment": []}

n_sub = 0
for submission in crypto_submissions:

    print("[INFO][" + str(n_sub) + "] " + submission.title + " - created: " + str(submission.created) + ", " + str(len(submission.comments)) + " comments.")
    n_sub = n_sub + 1
    topics_dict["title"].append(submission.title)
    topics_dict["score"].append(submission.score)
    topics_dict["id"].append(submission.id)
    topics_dict["url"].append(submission.url)
    topics_dict["comms_num"].append(submission.num_comments)
    topics_dict["created"].append(submission.created)
    topics_dict["body"].append(submission.selftext)

    # Comments may contain  nested comments as MoreComments object
    # Each replace_more replaces up to 32 MoreComments with comments from within
    # Each MoreComment requires 1 request to Reddit
    #
    # who the fuck came up with this idea O.o - RL

    # done_replaces = 0
    # while done_replaces < 3:
    #     try:
    #         submission.comments.list().replace_more()
    #         done_replaces = done_replaces + 1
    #     except Exception:
    #         time.sleep(1)

    sub_comments = []
    for comment in submission.comments.list():
        if isinstance(comment, Comment):
            sub_comments.append(comment)
    topics_dict["comment"].append(sub_comments)


topics_data = pd.DataFrame(topics_dict)


def get_date(input):
    return datetime.datetime.fromtimestamp(input)


timestamps = topics_data["created"].apply(get_date)
topics_data = topics_data.assign(timestamp=timestamps)

topics_data.info()
print("[INFO] Finished")
topics_data.to_csv("reddit_data", sep='\t')

