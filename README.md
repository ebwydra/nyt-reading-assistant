# nyt-reading-assistant
This project is a sort of New York Times reading assistant that provides some articles and contextual information relating to a given topic.

## FINAL PROJECT for SI 506 W18

### In ~2-3 sentences, what does your project do?

This project is a sort of New York Times reading assistant that provides some articles and contextual information relating to a given topic. When you run the program, you will be asked what you want to look up in the New York Times. The program will retrieve NYT news articles with headlines relating to your search term, then use the keywords associated with those articles to search for related topics on Wikipedia, and produce a text document containing up to ten articles (headlines, bylines, dates, snippets, and links) and up to six definitions from Wikipedia (article titles, article excerpts, and links to the full articles).

### What Python modules must be pip installed in order to run your submission? List them ALL (e.g. including requests, requests_oauthlib... anything someone running it will need!). Note that your project must run in Python 3.

The program requires the following Python modules: requests, json, codecs, and sys.

### Explain SPECIFICALLY how to run your code.

Before running the program, a New York Times API key should be entered on line 11 of the SI506W18_finalproject.py file, although I have included my key for the purposes of this assignment submission. (If you attempt to run the program but nothing has been entered on line 11, a print statement will ask you to enter your NYTimes API key in the program file, and then the program ends.)

When you run the SI506W18_finalproject.py file, there will be a prompt asking you what you would like to search for in the New York Times. Topics that are likely to appear in New York Times news articles (e.g. "Paul Ryan," "women's health," "MRSA") are recommended, but any reasonable English-language query will do. Avoid non-substantive queries such as "and" or "what," which tend to return nonsense. Quotation marks are not necessary for multi-word search terms. Apostrophes should not cause problems.

If this particular query has not been made before, the user will experience some dead time while the program obtains data from the internet via three API requests, and it will look like nothing is happening. (If the query has been made before, retrieving the appropriate data from the local cache file will not take as much time.) When the data have been obtained and the output file has been written, the user will see a print statement that says "The information you requested is in a file called [whatever the search term was]_info.txt!" An output file with that name will have been created in the same directory as the program file.

Occasionally, if an error occurs, usually as a result of a nonsensical search term (e.g., from keyboard mashing, other arbitrary alphanumeric strings, exclusively punctuation), the user will get an error message reading "Oops, something went wrong... Please restart program and try a different search." It is also possible to end up with an output file that reads "Hmm, I couldn't find any New York Times news articles about '[whatever the search term was].' Are you sure you spelled it right?" (Notably, this happens every time I search for "World War I.")

### Explain in a couple sentences what should happen as a RESULT of your code running: what CSV or text file will it create? What information does it contain? What should we expect from it in terms of approximately how many lines, how many columns, which headers...?

The output of this program is a .txt file with a name based on the user's search term, with spaces replaced by underscores. At the beginning of the file, there is a sentence that reads "Here are some headlines and snippets from news articles that mention '[whatever the search term was].'" Below that, there are up to 10 articles from the New York Times, sorted from newest (top) to oldest (bottom), presented in the following format:

[Title]
[Byline] (published on [date published])
[blank line]
[Snippet of article, as provided by NYT]
[blank line]
Link: [link to complete article].

Individual article results are divided by a horizontal divider: "---------". Below the New York Times article, there is text that reads "Enjoy your articles! Here's some information from Wikipedia on topics related to '[whatever the search term was]' that might be useful." There are then up to 6 results from Wikipedia, presented in the following format:

[Page title]: [first 500 characters from the Wikipedia article]... (Read more at: [link to Wikipedia article])

Wikipedia results are separated with line breaks. Note that the first (topmost) Wikipedia article listed should directly correspond to the user's search term.
