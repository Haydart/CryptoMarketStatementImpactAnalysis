import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class CryptoProjectsSpider(CrawlSpider):
    name = 'crypto_spider'
    allowed_domains = ["bitcoin.org/en",
                       "ripple.com"
                       "www.ethereum.org",
                       "bitcoin.org",
                       "ripple.com",
                       "www.ethereum.org",
                       "www.stellar.org",
                       "tether.to",
                       "eos.io",
                       "litecoin.org/pl",
                       "www.bitcoincash.org",
                       "nchain.com/en/blog/bitcoin-sv-launch",
                       "tron.network",
                       "www.cardano.org",
                       "www.getmonero.org",
                       "www.iota.org",
                       "www.binance.com/en",
                       "nem.io",
                       "www.dash.org",
                       "ethereumclassic.github.io",
                       "neo.org",
                       "z.cash",
                       "makezine.com",
                       "dogecoin.com",
                       "www.wavesproject.org",
                       "tezos.com",
                       "www.trusttoken.com/trueusd",
                       "www.circle.com/en/usd",
                       "bitcoingold.org",
                       "www.vechain.com/#",
                       "omisego.network",
                       "basicattentiontoken.org",
                       "qtum.org/e",
                       "www.paxos.com/standard",
                       "www.decred.org",
                       "0x.org",
                       "lisk.io",
                       "vergecurrency.com",
                       "sia.tech",
                       "steem.com"]

    start_urls = ["https://bitcoin.org/",
                  "https://ripple.com/",
                  "https://www.ethereum.org/",
                  "https://bitcoin.org/",
                  "https://ripple.com/",
                  "https://www.ethereum.org/",
                  "https://www.stellar.org/",
                  "https://tether.to/",
                  "https://eos.io/",
                  "https://litecoin.org/pl/",
                  "https://www.bitcoincash.org/",
                  "https://nchain.com/en/blog/bitcoin-sv-launch/",
                  "https://tron.network/",
                  "https://www.cardano.org/",
                  "https://www.getmonero.org/",
                  "https://www.iota.org/",
                  "https://www.binance.com/en",
                  "https://nem.io/",
                  "https://www.dash.org/",
                  "https://ethereumclassic.github.io/",
                  "https://neo.org/",
                  "https://z.cash/",
                  "https://makezine.com/",
                  "https://dogecoin.com/",
                  "https://www.wavesproject.org/",
                  "https://tezos.com/",
                  "https://www.trusttoken.com/trueusd/",
                  "https://www.circle.com/en/usdc",
                  "https://bitcoingold.org/",
                  "https://www.vechain.com/#/",
                  "https://omisego.network/",
                  "https://basicattentiontoken.org/",
                  "https://qtum.org/en",
                  "https://www.paxos.com/standard/",
                  "https://www.decred.org/",
                  "https://0x.org/",
                  "https://lisk.io/",
                  "https://vergecurrency.com/",
                  "https://sia.tech/",
                  "https://steem.com/"]

    rules = [
        Rule(
            LinkExtractor(
                allow=allowed_domains, unique=True
            )
        )
    ]

    def start_requests(self):
        with open("visited_links.csv", "a") as visited_links:
            with open("direct_twitter_links.csv", "a") as twitter_links:
                urls = self.start_urls
                yield from self.process_urls(twitter_links, urls, visited_links)

    def process_urls(self, twitter_links, urls, visited_links):
        for url in urls:
            if "twitter" in url:
                twitter_links.write(url + "\n")
            visited_links.write(url + "\n")
            if any(allowed_domain in url for allowed_domain in self.allowed_domains):
                yield scrapy.Request(url=url, callback=self.parse_response)

    def parse_response(self, response):
        with open("visited_links.csv", "a") as visited_links:
            with open("direct_twitter_links.csv", "a") as twitter_links:
                link_extractor = LinkExtractor()
                links = link_extractor.extract_links(response)
                urls = [link.url for link in links]
                yield from self.process_urls(twitter_links, urls, visited_links)
