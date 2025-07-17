# Web_scraping2
using Selenium 

I wanted to save the links of some Youtube videos (containing lectures of my classes),to an excel sheet so i can have acces to them even if my username and password stopped being active. Because these videos are private and only through the link i can have access to them.

The goal of this project was to get past the authentication wall and get to the page that contained all of the class titles and under each one of them, all of the subunits. The text of the subunit is a link that gets you to another page that contains a Youtube link. After this information is scraped it is stored in a dataframe and then in an excel sheet on your computer.  

So the information that is scrapped is the title of the unit , the title of the subunit and lastly the link of the pdf (for all units and subunits). If one subunit is empty or the page you are redirected doesn't contain a Youtube link then it moves on until it reaches the end of the page.

(The code contains a lot of comments so i think is readable.)
