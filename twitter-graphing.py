# Twitter conversation graphing
# makes a network graph file format of tweets replying to or reposting another account
# useds TAGs google doc to scrape tweets including keywords
# Formats as an edge and node list for Gephi

# Python script to take csv of twitter scrape and format it as a multi-level network graph
# import libraries
import pandas as pd
import numpy as np
import re
import nltk
from nltk.sentiment import SentimentAnalyzer
from nltk.sentiment.vader import SentimentIntensityAnalyzer

print "++++++++++++++++ WELCOME ++++++++++++++++"
print "++++++++++++++++ To The  ++++++++++++++++"
print "++++++++++++++++ TWITTER ++++++++++++++++"
print "++++++++++++++++ GRAPHER ++++++++++++++++"
print "++++++++++++++++++++++"
print "++++++++++++++++++"
print "+++++++++++++++"
print "+++++++++++++"
print "+++++++++++"
print "+++++++++"
print "+++++++"
print "+++++"
print "+++"
print "+"
print "This python script takes a csv file with" 
print "from_user and text columns ..."
print "performs a sentiment analysis, and ... "
print "outputs an edgelist and nodelist csv file"
print "for importing into the graphing software Gephi "


# import the csv file
fileNm = raw_input('Enter a filename: ')
fileNmStr = fileNm.split(".csv")[0]
df1 = pd.read_csv(fileNm, usecols=["time", "from_user", "text"])
print "++++++++++++++++++++++"
print "++++ File loaded  ++++"
print "++++++++++++++++++++++"
# duplicate/format/label columns
df1.rename(columns={"from_user": "source"})
df1['datetime'] = pd.to_datetime(df1['time'])

# convert tweet into text format
temp = df1['text'].copy()
df1['target'] = df1.text.copy()
df1['source'] = df1.from_user.copy()

def count_letters(word, char):
  count = 0
  for c in word:
    if char == c:
      count += 1
  return count

def clean_tweet(tweet):
    '''
    Utility function to clean the text in a tweet by removing 
    links and special characters using regex.
    '''
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

def analize_sentiment(tweet):
    '''
    Utility function to classify the polarity of a tweet
    using textblob.
    '''
    ss1 = sid.polarity_scores(clean_tweet(tweet))
    return ss1['compound']

# make edge list from source and users in @s and RTs in the text
# Source, Target, Type, Id, Label, Interval, Weight

newedgelist = pd.DataFrame(columns={'Source', 'Target', 'Text'})
x = 0
for i in range(0,len(df1)):
    text = df1.text[i]
    try:
        atN = count_letters(text, '@')
        if atN >= 1:
            try:  
                for N in range(atN):
                    try:
                        val = "@".join(text.split('@')[N+1:N+2]).replace(" ", ",")
                        v2 = val.split(",")[0].replace(":", "")
                        v3 = v2.replace(".", "")
                        newedgelist.Source.loc[x] = df1.source[i]
                        newedgelist.Target.loc[x] = v3
                        newedgelist.Text.loc[x] = df1.text[i]                     
                        x = x + 1
                    except:
                        print 'error 0'
            except:
                print 'error step 1'
        elif atN <= 0:
            try:
                df1.target[i] = ""
                x = x + 1
            except:
                print 'error step 2'
    except:
        print 'no at symbol found' 

# format columns and check
edgelist = pd.DataFrame(newedgelist.Source)
edgelist['Target'] = newedgelist.Target
edgelist['Type'] = 'Directed'
edgelist['Id'] = newedgelist.Source
edgelist['Label'] = newedgelist.Source
edgelist['timeset'] = df1['time']
edgelist['Weight'] = 1
edgelist['Text'] = newedgelist.Text # td= remove user names
print "++++++++++++++++++++++"
print "Edgelist created"
print "++++++++++++++++++++++"
# Add sentiment score for each edge
sid = SentimentIntensityAnalyzer()
edgelist['sscore'] = np.array([ analize_sentiment(tweet) for tweet in edgelist['Text'] ])
print "++++++++++++++++++++++"
print "Sentiment scores calculated"
print "++++++++++++++++++++++"
# create node df -Id -Label, -Type
targetnodes = [edgelist['Source'], edgelist['Target']]
result = pd.concat(targetnodes)
data = {'Label': result.unique(),
       'Id': "",
       'avgsscore': ""}
dfnodesunique = pd.DataFrame(data)
dfnodesunique['Id'] = dfnodesunique.index
print "++++++++++++++++++++++"
print "Nodelist created"
print "++++++++++++++++++++++"
# Get average sentiment score per node
data = edgelist
for NOD in data['Source'].unique():
    try:
        locs = edgelist.loc[edgelist['Source'] == NOD]
        res = locs.sscore.mean()
        dfnodesunique.avgsscore.loc[dfnodesunique['Label'] == NOD] = res
    except:
        dfnodesunique.avgsscore.loc[dfnodesunique['Label'] == NOD] = 0
        print 'error'

newedgelist = edgelist.copy()
print "++++++++++++++++++++++"
print "Node average sentiment calculated"
print "++++++++++++++++++++++"
# Substitute Id numbers from nodelist in source edgelist
data = edgelist
for NOD in data['Source'].unique():
    lid = dfnodesunique.Id[dfnodesunique['Label'] == NOD]
    try:
        newedgelist.Source.loc[newedgelist['Source'] == NOD] = int(lid)
    except:
        print "no entry in source"        


# Substitute Id numbers from nodelist in target edgelist
data = edgelist
for NOD in data['Target'].unique():
    lid = dfnodesunique.Id[dfnodesunique['Label'] == NOD]
    try:
        newedgelist.Target.loc[newedgelist['Target'] == NOD] = int(lid)
    except:
        print "no entry in target"
print "++++++++++++++++++++++"
print "Data formated... last step"   
print "++++++++++++++++++++++"
cutedgelist = newedgelist[['Source', 'Target', 'Label', 'sscore']]
# save
EfileNm = str(fileNmStr) + "-edgelist.csv"
NfileNm = str(fileNmStr) + "-nodelistlist.csv"
cutedgelist.to_csv(EfileNm, index=False)
dfnodesunique.to_csv(NfileNm, index=False)
print "++++++++++++++++++++++"
print "Edge and nodelist files saved!"
print "++++++++++++++++++++++"
print "++++++++++++++++++++++"
print "+++++++++THE++++++++++"
print "+++++++++END++++++++++"