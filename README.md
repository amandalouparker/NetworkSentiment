# NetworkSentiment
Performs sentiment analysis on twitter data collected with [TAGS](https://tags.hawksey.info/get-tags/) and outputs edge and node lists for graphing in [Gephi](https://gephi.org/)

#### Instructions
Navigate to the repo folder and run the twitter-graphing.py script
When prompted enter the name of a csv file that contains 'from_user' and 'text' columns. The 'from_user' column should contain the twitter user name of the account that posted the tweet, and the 'text' field should contain the full text of the tweet, including the @accountnames of accounts the tweet is directed at (there can be more than one account per tweet)

After entering the csv file name the script will calculate sentiment scores for each tweet and account (by averaging the sentiment scores for all the tweets made by each particular account) and then formats the data into an edgelist and nodelist csv file for loading into Gephi. Gephi is a free network graphing software with excellent graph customisation features, including the ability to collour notes and edges per additional variables like the sentiment scores added in this script. Open gephi and be sure to import the spreadsheets in node or edge formats accordingly to the same workspace.

#### Example network graph
Below is an example Gephi network graph generated from the example data included in this repo. The data was collected with the [TAGS google spreadsheet](https://tags.hawksey.info/get-tags/) and includes all tweets using the hashtrag #IBelieveChristineFord in the past week. This hashtag relates to a topical controversy in US politics about a Supreme court judge nomination. 

![Example Graph](/images/ChristineFord.png)

This graph has been formated to highlight *who* the hashtag activisim is lobbying (Jeff Flake is the most prominent in this example), by increasing the size of account nodes that are recieving the most tweets.  The number of outgoing tweets per node is visualised with wider edges (lines). Sentioment is depicted with a colour gradient that goes from red (negative), grey (neutral or missing) through to green (positive)


