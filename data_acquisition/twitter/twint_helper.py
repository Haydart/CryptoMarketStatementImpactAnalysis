import math

HANDLES_BATCH_SIZE = 25

with open("unique_twitter_handles.csv") as twitter_handles_file:
    all_handles = twitter_handles_file.readlines()

    for i in range(int(math.ceil(len(all_handles) / HANDLES_BATCH_SIZE))):
        print(all_handles[i * HANDLES_BATCH_SIZE:(i + 1) * HANDLES_BATCH_SIZE])
