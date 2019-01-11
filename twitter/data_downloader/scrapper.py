import twint


def scrap(hashtag, since, until, output):
    c = twint.Config()
    c.Count = True
    c.Store_json = True
    c.Search = hashtag
    c.Since = since
    c.Until = until
    c.Output = output
    twint.run.Search(c)


scrap("#cryptocurrency", "2016-12-31", "2016-01-01", "cryptocurrency-2016.json")
