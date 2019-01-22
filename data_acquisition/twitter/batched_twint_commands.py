import math
import os

HANDLES_BATCH_SIZE = 15

with open("unique_twitter_handles.csv") as twitter_handles_file:
    all_handles = twitter_handles_file.read().splitlines()

    for i in range(int(math.ceil(len(all_handles) / HANDLES_BATCH_SIZE))):
        handles_batch = all_handles[i * HANDLES_BATCH_SIZE:(i + 1) * HANDLES_BATCH_SIZE]
        user_list_arg = ','.join(handles_batch)
        output_file_name = '../../output/batched_tweets/tweets_batch{}.csv'.format(i + 1)
        since_arg = '2018-01-01'
        os.system('twint --userlist {} --csv -o {} --since {}'.format(user_list_arg, output_file_name, since_arg))
