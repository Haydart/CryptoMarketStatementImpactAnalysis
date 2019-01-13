from google import google

top_cryptocurrencies_names = ["Bitcoin", "XRP", "Ethereum", "Stellar", "Tether", "EOS", "Litecoin", "Bitcoin Cash",
                              "Bitcoin SV", "TRON", "Cardano", "Monero", "IOTA", "Binance Coin", "NEM", "Dash",
                              "Ethereum Classic", "NEO", "Zcash", "Maker", "Dogecoin", "Waves", "Tezos", "TrueUSD",
                              "USD Coin", "Bitcoin Gold", "VeChain", "OmiseGO", "Basic Attention Token", "Qtum",
                              "Paxos Standard", "0x", "Decred", "Ontology", "Lisk", "Bitcoin Diamond", "Zilliqa",
                              "Nano", "Bytecoin", "BitShares", "DigiByte", "ICON", "Gemini Dollar", "Verge", "Siacoin",
                              "Aurora", "Aeternity", "Pundi X", "Factom", "Chainlink", "Bytom", "Steem", "QASH",
                              "Augur", "Stratis", "Revain", "Populous", "Komodo", "MaidSafeCoin", "Holo", "TenX", "Dai",
                              "Electroneum", "Golem", "Cryptonex", "Huobi Token", "Status", "Decentraland", "IOST",
                              "DEX", "Ardor", "KuCoin Shares", "Bitcoin Private", "Insight Chain", "Polymath",
                              "Elastos", "Waltonchain", "Nexo", "WAX", "Dentacoin", "STASIS EURS", "ODEM", "QuarkChain",
                              "Ark", "MobileGo", "Metaverse ETP", "HyperCash", "Wanchain", "Bancor", "Mixin",
                              "ReddCoin", "Ravencoin", "Mithril", "Aion", "THETA", "aelf", "Crypto.com", "GXChain",
                              "Digitex Futures", "PIVX"]


def fetch_projects_website_links():
    with open("crypto_projects_links.txt", "a") as projects_links:
        for project_id, project_name in enumerate(top_cryptocurrencies_names[24:35], 24):
            search_results = google.search(project_name + " project website")
            if search_results and search_results[0]:
                projects_links.write(search_results[0].link + "\n")
                print(str(project_id) + " Got " + search_results[0].link)
            else:
                print(str(project_id) + " No search results fetched for project " + project_name)


if __name__ == '__main__':
# fetch_projects_website_links()
