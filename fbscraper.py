import facebook
import re
import json
from itertools import chain
import csv
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import requests
from six.moves import input 

#recursively get all the postIDs and its texts and then get text comments for each of those postIDs
def recursePosts(pagingUrl): 
    flag = True
    while flag == True:
        var = requests.get(pagingUrl)
        contentBytes = var.content
        contentBlob = json.loads(contentBytes)
        contentMessage = contentBlob["data"]

        for i in range(0, len(contentMessage)):
            if(DictQuery(contentMessage[i]).get("message") is not None):
                postID.append(DictQuery(contentMessage[i]).get("id"))
                myFeed.append(DictQuery(contentMessage[i]).get("message"))

        nextPage = DictQuery(contentBlob).get("paging/next")
        if nextPage is not None:
            return recursePosts(nextPage)
        else:
            flag = False
            break

def grabComments():
    for j in range(0, len(postID)):
        comments = graph.get_object(id=postID[j],fields='comments')
        stringComments = json.dumps(comments)
        replacedComments = re.sub('u\'','', stringComments)
        outputComments = json.loads(replacedComments)

        #check if post has at least a comment
        if(DictQuery(outputComments).get("comments/data/message") is not None):
            myComments.append(DictQuery(outputComments).get("comments/data/message"))
        
#helper function to retrive data within nested JSON
class DictQuery(dict):
    def get(self, path, default = None):
        keys = path.split("/")
        val = None
        for key in keys:
            if val:
                if isinstance(val, list):
                    val = [ v.get(key, default) if v else None for v in val]
                else:
                    val = val.get(key, default)
            else:
                val = dict.get(self, key, default)
            if not val:
                break
        return val

token = input('Enter Extended User Access Token:')
groupID = input('Enter groupID:')
graph = facebook.GraphAPI(access_token= token, version='2.7')
var = "https://graph.facebook.com/v2.12/" + groupID + "/feed?access_token=" + token
myFeed = [] #initialize empty list to store posts
postID = [] #initialize empty list to store postID to use in comments API call
myComments = [] #initialize empty list to store comments within posts
recursePosts(var)
grabComments()
merged = list(chain(*myComments)) #flattens the nested list
totalFeed = myFeed + merged

#cleaning the words
textInitial = ' '.join(totalFeed) #converting list to string to input into wordcloud
text = textInitial.lower() #ensures that same words but with different cases are not counted as two separate words
#setting stopwords
stopwords = set(STOPWORDS)
stopwords.add("https") #ensures that links in post do not show as top words

#constructing the wordcloud
wordcloud = WordCloud(width=480, height=480, max_font_size=50, min_font_size=5, max_words=30, normalize_plurals=True, stopwords=stopwords).generate(text)
#if you want to print the words and its associated frequency use the function wordcloud.words_
#print(wordcloud.words_)
plt.figure()
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.margins(x=0, y=0)
plt.show()


