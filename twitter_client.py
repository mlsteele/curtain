import twitter, ConfigParser, threading, time


config = ConfigParser.ConfigParser()
config.read(["twitter_config.ini"])


class Tweet(object):
    def __init__(self, text, name = None):
        self.text = text.encode('utf-8', 'ignore')
        self.name = name.encode('utf-8', 'ignore')

    def __repr__(self):
        return "Tweet ('%s', '%s')" % (self.text, self.name)


class TwitterCrawler(threading.Thread):
    """
    This class searches twitter for a string and calls callback when new tweets
    matching it arrive.

    Example:

        def print_tweet(tweet):
            print tweet

        t = TwitterCrawler(term = "#eastcampus", callback = print_tweet, interval = 5)
        t.start()

    """

    def _init_twitter(self):
        self.consumer_key        = config.get('Twitter', 'consumer_key')
        self.consumer_secret     = config.get('Twitter', 'consumer_secret')
        self.access_token_key    = config.get('Twitter', 'access_token_key')
        self.access_token_secret = config.get('Twitter', 'access_token_secret')

        self.api = twitter.Api(consumer_key          = self.consumer_key ,
                  consumer_secret       = self.consumer_secret,
                  access_token_key      = self.access_token_key,
                  access_token_secret   = self.access_token_secret)

    def __init__(self, term = "from:eastcampusrush OR @eastcampusrush OR #eastcampus",
                 callback = None,
                 interval = 5,
                 count = 1):
        self.callback = callback
        self.count = count
        self.interval = interval
        self.term = term
        self._init_twitter()
        self.since_id = 0

        threading.Thread.__init__(self)
        self.setDaemon(True)

    def update(self):
        search = self.api.GetSearch(self.term, since_id = self.since_id, count = self.count)
        search = (x.AsDict() for x in search)
        search = sorted(search, cmp = lambda x, y: x['id'] - y['id'])
        for tweet in search:
            self.since_id = tweet['id']
            tweet = Tweet(tweet['text'], tweet['user']['name'])
            if self.callback:
                self.callback(tweet)
            else:
                print tweet

    def run(self):
        self.running = True

        while self.running:
            self.update()
            time.sleep(self.interval)

    def stop(self):
        self.running = True

        return self.join()


if __name__ == '__main__':

    t = TwitterCrawler()
    t.start()

    while True:
        time.sleep(0.1)
