# fbgroupscraper
A Python script that pull texts from every post and comments in a Facebook group using Facebook's Graph API and display the most common words in a Word Cloud

## Instructions
1. Clone the repo and create a virtualenv and activate it
2. Install the following packages using `pip`:
  - `pip install facebook-sdk`
  - `pip install wordcloud` 
 3. Get an extended Facebook Access Token (for more instructions refer to this article: https://towardsdatascience.com/how-to-use-facebook-graph-api-and-extract-data-using-python-1839e19d6999)
4. Run `python fbscraper.py` and enter Access Token and the groupID of the Facebook group you are interested in. The groupID is usually indicated in url on Facebook when you visit the page. If not you can always view the html source code and `ctrl-f` for pageID thats starts with numerics

### Disclaimer:
1. This will work for any public group or page provided you don't cross the rate limits. It you want to pull post and comments from closed group, you will need to have admin permissions of that group



