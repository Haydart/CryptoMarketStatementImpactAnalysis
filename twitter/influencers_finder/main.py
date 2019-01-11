from twitter.influencers_finder.top_influencers import find_influencers_in_tweets, find_influencers_in_stats
import subprocess


USER_STATS_FILE_PATH = './data/BTC/users-stats.json'


def get_user_stats(files, number):
    top_users = list(find_influencers_in_tweets(files, number)['username'])
    users_stats = []
    for idx in range(0, number):
        command = "twint -u " + top_users[idx] + " --user-full -o " + USER_STATS_FILE_PATH + "--json"
        users_stats.append(subprocess.call(['C:\\windows\\system32\\cmd.exe', '/C', command]))


def get_top_influencers(number):
    top_influencers = find_influencers_in_stats(USER_STATS_FILE_PATH, number)['username']
    with open('./data/BTC/influencers.txt', 'x') as f:
        for user in top_influencers:
            f.write(user + "\n")


get_user_stats('./data/BTC', 100)
get_top_influencers(10)
