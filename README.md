# GPU_Crawler

## When you can't beat them - join them.
-------------------------------------------

This is a python bot that I wrote to monitor the availability of new GPUs in German online retailers during the 2020 pandemic. Since I had troubles with my previous GPU and I had to return it, I was in need of a new one. The whole scalper situation really pissed me off, because pleople that really needed new cards weren't able to get their hands on one, including me. Since I do not need this software anymore, I'm now releasing it to the public. 

The bot works as follows:
In a given URL, the script makes a request and extracts the website's HTML code. Should that fail (e.g. because of bot protection), it uses Selenium to open a new browser tab and access the webpage (basically doing what a human would) and then extracts its contents with the help of the BeautifulSoup library. Then it searches a user-defined class inside the HTML Code to extract the Name, Price, Availability, Buy Link and Chip Name of each GPU on sale in the current URL. Finally it exports an up to date Excel table to your desktop that is sorted by availability and price. You can also set price thresholds, so that once an affordable GPU is available, Selenium opens the Buy Link and notifies you by playing a sound.
(Do note, that you'll require a driver for the webbrowser you're using [e.g. Chrome -> chromedriver.exe]. Google it.)

This is an open source software and is completely free for all uses. Some minor tweaks and changes are required to make it run for your custom case, so that some basic Python programming skills will be necessary. At best you can use this as a reference for your own projects.

When you use this piece of software there is no need to credit me or anything. Please just use this responsibly and only for your own needs. Be contious of others.


## Copyright
by Petar Hristov, licensed under [Apache License 2.0](https://opensource.org/licenses/Apache-2.0).

