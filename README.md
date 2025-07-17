# Web_scraping2
using Selenium 

This project automates the process of saving private YouTube lecture links from a password-protected educational platform. Since these videos are only accessible via direct links (and my login credentials will expire at some point), I used Selenium to scrape and store them in an Excel sheet for permanent access.

The script first bypasses the authentication wall to reach the course page, which lists all class titles and their subunits. Each subunit links to a separate page containing an embedded YouTube video. The scraper extracts three key pieces of data: the unit title, subunit title, and YouTube link. If a subunit is empty or lacks a video, the script skips it and continues iterating until the end of the page. The collected data is organized into a pandas DataFrame and exported to an Excel file. The code includes detailed comments to clarify each step of the process.
