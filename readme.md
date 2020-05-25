# UFC Fight Scraper
Scraper.py currently scrapes the UFC fight statistics website and writes fight information to a csv titled fights.py

There are a few bugs that need to be sorted out:
1. It counts ultimate fighter tournament bouts as title fights because the current method of determining a championship bout is by if the belt icon appears on the site.
2. It doesn't have any error handling, so for the early fights that have no statistics it hits an index out of range error.

## TODO:
1. Write it so that it saves to a database.
2. Create a script to export database contents to a csv in same format as it currently does.
3. Change the scraper to only scrape fight cards that are missing from said database.