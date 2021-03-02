# StonksBot
 A stock scraping bot for Reddit

This bot uses the web scraping python framework Scrapy to search for
stock tickers from the base url "https://www.reddit.com/r/wallstreetbets/"
and aggregate the number of mentions in a .csv file, where
various charts can be produced from the data.

The current build does not support infinitely scrolling pages and uses an
ignore filter that is not sustainable. Tickers of the form "$[A-Z]{2,4}"
as well as those without the "$" are collected, resulting in various junk data
that has not been fully filtered out.
