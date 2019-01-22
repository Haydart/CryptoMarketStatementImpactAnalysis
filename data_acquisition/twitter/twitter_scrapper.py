import twint


def scrap_hashtag(hashtag, since, until, output):
    c = twint.Config()
    c.Count = True
    c.Store_json = True
    c.Search = hashtag
    c.Since = since
    c.Until = until
    c.Output = output
    twint.run.Search(c)


def scrap_single_user(username, output):
    c = twint.Config()
    c.Username = username
    c.User_full = True
    c.Store_json = True
    c.Output = output
    twint.run.Lookup(c)


def scrap_multiple_users(users_file_path, output_file_path):
    pass
