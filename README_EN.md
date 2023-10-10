# Telegram bot for searching hotels on hotels.com 

The goal of the project was to create a convenient telegram bot for quickly hotels finding.
The bot implements the following commands:
- Search for the lowest price hotels
- Search for the highest price hotels 
- Hotels searching based on specified parameters: maximum prices and maximum distance from the downtown.
- Search history (displays the results of the last five queries)

Mechanics of hotel search commands:
- users can select the number of hotels that need to be withdrawn (up to 10)
- users can indicate the city, date of arrival and duration of stay
- users can choose whether to display hotel photos in search results or not
- the search result always contains basic information about the hotel, a link to the hotel on the website, and the cost of accommodation.

### My contribution
This project was completely implemented by me.

### Used stack
Python 3.9

Libraries: 
- pyTelegramBotAPI
- requests
- mysql.connector


Database - mysql


Connection to the api of hotels.com implemented via singleton

The following files have been prepared to deploy the project:
- env.template
- requirements.txt
- dump of DB with small query of test data