import pandas as pd


def keep_unique_twitter_handles():
    twitter_handles_df = pd.read_csv("output/direct_twitter_links.csv")
    print(twitter_handles_df.head())


def clean_tweets():
    not_twitter_handles_parts = ["intent", "search", ]

    with open('output/direct_twitter_links.csv', 'r') as raw_twitter_handles:
        for link in raw_twitter_handles:
            link = remove_whitespaces(link)
            after_domain_part = link.split("/")[3]
            if any(after_domain_part.startswith(unwanted_part) for unwanted_part in not_twitter_handles_parts):
                print(after_domain_part)


def remove_whitespaces(line):
    no_whitespace_link = ''.join(line.split())
    return no_whitespace_link


if __name__ == '__main__':
    clean_tweets()
    # keep_unique_twitter_handles()
