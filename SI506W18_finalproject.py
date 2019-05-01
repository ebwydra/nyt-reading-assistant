# Import statements
import requests
import json
import codecs
import sys
sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer) # Encoding...

# Credentials for NYTimes API go here (The Wikipedia API doesn't require any form of authorization.)
nyt_key = ""
if nyt_key == "" or not nyt_key:
    print("Please enter your NYTimes API on line 11 of the SI506W18_finalproject.py file.")
    exit()

# Cache setup and try to read data from cache file
CACHE_FNAME = "SI506W18finalproject_cache.json"
try:
    f = open(CACHE_FNAME, 'r')
    f_contents = f.read()
    f.close()
    CACHE_DICTION = json.loads(f_contents)
except:
    CACHE_DICTION = {}

# Class definition for NYTArticle:
class NYTArticle(object):
    def __init__(self, nyt_diction):
        self.headline = nyt_diction['headline']['main']
        self.snippet = nyt_diction['snippet']
        byline = ""
        try:
            if nyt_diction['byline']['original'] == None:
                byline = 'No author listed'
            else:
                byline = nyt_diction['byline']['original']
        except:
            byline = 'No author listed'
        self.byline = byline # A string, e.g. 'By NATALIA V. OSIPOVA'
        self.date = nyt_diction['pub_date'] # String representing date, e.g. '2016-11-09T16:58:09+0000'
        list_of_keywords = []
        for keyword in nyt_diction['keywords']:
            list_of_keywords.append(keyword['value'])
        self.keywords_list = list_of_keywords
        self.url = nyt_diction['web_url']

    def make_date_nice(self): # Makes the date more human-readable. I'm sure there's a more elegant way to do this...
        year = self.date[:4]
        month_num = self.date[5:7]
        day = self.date[8:10]
        if month_num == '01':
            month = 'January'
        elif month_num == '02':
            month = 'February'
        elif month_num == '03':
            month = 'March'
        elif month_num == '04':
            month = 'April'
        elif month_num == '05':
            month = 'May'
        elif month_num == '06':
            month = 'June'
        elif month_num == '07':
            month = 'July'
        elif month_num == '08':
            month = 'August'
        elif month_num == '09':
            month = 'September'
        elif month_num == '10':
            month = 'October'
        elif month_num == '11':
            month = 'November'
        elif month_num == '12':
            month = 'December'
        return "{} {}, {}".format(month, day, year)

    def __str__(self):
        return "{}\n{} (published on {})\n\n{}\n\nLink: {}".format(self.headline, self.byline, self.make_date_nice(), self.snippet, self.url)

# Class definition for WikiArticle
class WikiArticle(object):
    def __init__(self, wiki_diction):
        self.page_id = int(wiki_diction['id'])
        self.title = wiki_diction['source']['title']
        self.opening_text = wiki_diction['source']['opening_text']
        self.full_text = wiki_diction['source']['source_text']

    def make_url(self):
        return "https://en.wikipedia.org/wiki/{}".format(self.title.replace(" ", "_"))

    def __str__(self):
        try:
            return "{}: {}... (Read more at {})\n".format(self.title, self.opening_text[:500], self.make_url())
        except:
            return "(Oops, I had trouble printing this result!)"

# Function that generates a unique identifier for API requests
def params_unique_combination(baseurl, params_d, private_keys=["nyt_key"]):
    alphabetized_keys = sorted(params_d.keys())
    res = []
    for k in alphabetized_keys:
        if k not in private_keys:
            res.append("{}-{}".format(k, params_d[k]))
    return baseurl + "_".join(res)

# Function that retreives and caches NYT articles relating to a given term (string)
def get_nyt_data(search_term):
    base_url = "http://api.nytimes.com/svc/search/v2/articlesearch.json"
    params_dict = {}
    params_dict['fq'] = 'type_of_material:("News") AND headline.search:("{}")'.format(search_term)
    # params_dict['begin_date'] = '20000101' # Material since 2000
    params_dict['api-key'] = nyt_key
    unique_ident = params_unique_combination(base_url,params_dict)
    # Check if this search is already in the cache...
    if unique_ident in CACHE_DICTION:
        return CACHE_DICTION[unique_ident]
    else: # Make a new request...
        resp = requests.get(base_url, params=params_dict)
        resp_text = resp.text # Access text attribute of response object and store in a variable
        try:
            python_obj = json.loads(resp_text) # A dictionary
            CACHE_DICTION[unique_ident] = python_obj
            dumped_json_cache = json.dumps(CACHE_DICTION)
            fw = open(CACHE_FNAME, 'w')
            fw.write(dumped_json_cache)
            fw.close()
            return CACHE_DICTION[unique_ident]
        except:
            print("Oops, something went wrong... Please restart program and try a different search.")
            exit()

# Function that accepts a list of NYTArticle instances, and returns the top 5 keywords from the list
def nyt_keywords_from_instances(list_of_instances):
    # Populate dictionary
    keywords_dict = {}
    for article_instance in list_of_instances:
        for keyword in article_instance.keywords_list:
            keyword = keyword.upper() # Sometimes the same keyword shows up with different capitalization
            if keyword not in keywords_dict:
                keywords_dict[keyword] = 1
            else:
                keywords_dict[keyword] += 1
    # Make a list
    list_of_keywords = list (keywords_dict.keys())
    sorted_keywords = sorted(list_of_keywords, reverse=True, key= lambda x: keywords_dict[x])
    # Return top 5
    return sorted_keywords[:5]

# Function that searches for a term (a string) on Wikipedia
def search_wiki(search_term):
    base_url = "https://en.wikipedia.org/w/api.php"
    params_dict = {}
    params_dict['format'] = 'json'
    params_dict['action'] = 'query'
    params_dict['list'] = 'search'
    params_dict['srsearch'] = search_term
    unique_ident = params_unique_combination(base_url,params_dict)
    if unique_ident in CACHE_DICTION:
        return CACHE_DICTION[unique_ident]
    else:
        resp = requests.get(base_url, params=params_dict)
        resp_text = resp.text # Access text attribute of response object and store in a variable
        python_obj = json.loads(resp_text)
        CACHE_DICTION[unique_ident] = python_obj
        dumped_json_cache = json.dumps(CACHE_DICTION)
        fw = open(CACHE_FNAME, 'w')
        fw.write(dumped_json_cache)
        fw.close()
        return CACHE_DICTION[unique_ident]

# # Helper function that takes the dict output of search_wiki, and returns a pageid (int) for the top page
# def first_wiki_pageid(wiki_data):
#     page_id = wiki_data['query']['search'][0]['pageid']
#     return page_id

# Function that takes the dict output from the last function (containing page id numbers) as input, and returns a dictionary corresponding to the Wikipedia article for the first result
def get_wiki_data(wiki_data):
    base_url = "https://en.wikipedia.org/w/api.php"
    params_dict = {}
    params_dict['format'] = 'json'
    params_dict['action'] = 'query'
    params_dict['prop'] = 'cirrusdoc'
    try:
        params_dict['pageids'] = wiki_data['query']['search'][0]['pageid'] #first_wiki_pageid(wiki_data)
    except:
        print("Oops, something went wrong... Please restart program and try a different search.")
        exit()
    unique_ident = params_unique_combination(base_url,params_dict)
    if unique_ident in CACHE_DICTION:
        return CACHE_DICTION[unique_ident]
    else:
        resp = requests.get(base_url, params=params_dict)
        resp_text = resp.text # Access text attribute of response object and store in a variable
        raw_wiki_data_dict = json.loads(resp_text)
        # python_obj = raw_wiki_data_dict['query']['pages'][str(first_wiki_pageid(wiki_data))]['cirrusdoc'][0]
        python_obj = raw_wiki_data_dict['query']['pages'][str(wiki_data['query']['search'][0]['pageid'])]['cirrusdoc'][0]
        CACHE_DICTION[unique_ident] = python_obj
        dumped_json_cache = json.dumps(CACHE_DICTION)
        fw = open(CACHE_FNAME, 'w')
        fw.write(dumped_json_cache)
        fw.close()
        return CACHE_DICTION[unique_ident]

############################################################################

# Here we go!
search_term = input("What would you like to search for in the New York Times? ")

# Search for NYT articles about the provided term, then create a list of NYTArticle instances
nyt_data = get_nyt_data(search_term)
list_of_nyt_instances = []
for article in nyt_data['response']['docs']:
    list_of_nyt_instances.append(NYTArticle(article))

# Sort the list of NYTArticle instances by date (newest to oldest)
sorted_list_of_nyt_instances = sorted(list_of_nyt_instances, reverse = True, key = lambda x: x.date) # NOT the pretty date

# Find the top 5 keywords associated with the above articles
top_keywords = nyt_keywords_from_instances(list_of_nyt_instances)

# Search for Wikipedia articles using the top_keywords list, and create a list of WikiArticle instances
list_of_wiki_instances = []
list_of_wiki_instances.append(WikiArticle(get_wiki_data(search_wiki(search_term)))) # Include result from user input search term...
for keyword in top_keywords:
        wiki_result = get_wiki_data(search_wiki(keyword))
        wiki_instance = WikiArticle(wiki_result)
        if wiki_instance.page_id != WikiArticle(get_wiki_data(search_wiki(search_term))).page_id: # Don't include search_term twice
            list_of_wiki_instances.append(wiki_instance)

# Write the output to a file
clean_search_term = search_term.replace('"','')
clean_search_term = clean_search_term.replace(' ','_')
OUT_FNAME = "{}_info.txt".format(clean_search_term)
outfile = open(OUT_FNAME, 'w', encoding='utf-8')
if len(list_of_nyt_instances) > 0:
    outfile.write("Here are some headlines and snippets from news articles that mention '{}.'\n\n".format(search_term))
    for article in sorted_list_of_nyt_instances:
        outfile.write(article.__str__())
        outfile.write("\n---------\n")
    if len(top_keywords) > 0:
        outfile.write("\nEnjoy your articles! Here's some information from Wikipedia on topics related to '{}' that might be useful.\n".format(search_term))
        for instance in list_of_wiki_instances:
            outfile.write("\n")
            outfile.write(instance.__str__())
    else:
        outfile.write("\nI couldn't find any topics related to '{}.'\n".format(search_term))
else:
    outfile.write("Hmm, I couldn't find any New York Times news articles about '{}.' Are you sure you spelled it right?".format(search_term))
outfile.close()

# Print a statement in the terminal telling the user where to find the information
print("The information you requested is in a file called {}!".format(OUT_FNAME))
