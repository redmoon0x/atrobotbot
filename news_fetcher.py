import feedparser
import random

class NewsFetcher:
    def __init__(self):
        self.rss_feeds = {
            "top": "https://timesofindia.indiatimes.com/rssfeedstopstories.cms",
            "tech": "https://timesofindia.indiatimes.com/rssfeeds/66949542.cms",
            "science": "https://timesofindia.indiatimes.com/rssfeeds/-2128672765.cms",
            "india": "https://timesofindia.indiatimes.com/rssfeeds/-2128936835.cms",
            "business": "https://timesofindia.indiatimes.com/rssfeeds/1898055.cms"
        }
        
    def get_random_news(self, category: str = None) -> dict:
        try:
            if category and category in self.rss_feeds:
                feed_url = self.rss_feeds[category]
            else:
                feed_url = random.choice(list(self.rss_feeds.values()))
                
            feed = feedparser.parse(feed_url)
            if feed.entries:
                article = random.choice(feed.entries)
                return {
                    "title": article.title,
                    "description": article.description,
                    "link": article.link
                }
            
            return {
                "title": "No news found",
                "description": "Sorry, couldn't fetch any news right now."
            }
        except Exception as e:
            return {
                "title": "Error fetching news",
                "description": f"Sorry, something went wrong: {str(e)}"
            }

# Make class available for import
__all__ = ['NewsFetcher']
