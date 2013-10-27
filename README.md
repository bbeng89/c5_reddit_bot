# concrete5 Deal of the Day Reddit Bot #

This is a simple python script that pulls the deal of the day from http://www.concrete5.org/marketplace/deal/ 
and posts it to http://reddit.com/r/concrete5.

Since there is no RSS or any other kind of feed for the DotD, I currently have to just scrape the HTML. 
In the future if a feed is added it should be easy to just swap the DotD class.

__Todo__
* exception handling

__Libraries Used__
*PRAW - https://github.com/praw-dev/praw
*Requests - https://github.com/kennethreitz/requests
*Beautiful Soup - http://www.crummy.com/software/BeautifulSoup/
