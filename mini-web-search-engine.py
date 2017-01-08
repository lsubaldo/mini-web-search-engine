import urllib2
import random 


def download_page(pagename):
    '''(str) -> str
    Returns all the text on pagename as a str.
    '''
    fullurl = "http://cs.colgate.edu/cosc101/testweb/" + pagename
    fileobject = urllib2.urlopen(fullurl)
    text = fileobject.read()
    return text

def extract_links(text):
    '''(str) -> list of str
    Returns a list of str that refer to web page names
    that are linked from the current page
    >>> extract_links('abc <a href="a.html">xyz</a> def')
    ['a.html']
    >>> extract_links('A <a href="one.html">B</a> C <a href="two.html">D</a>')
    ['one.html', two.html']
    >>> extract_links('abc <a blah="a.html">xyz</a>')
    []
    '''
    links = []
    text = text.split()
    for i in range(len(text) - 1):
        if '<a' in text[i]  and 'href=' in text[i+1]:
            for j in range(len(text[i+1])):
                if j == 6:          #6, because that is where the link starts
                    links += [text[i+1][j:text[i+1].find('"', j)]] #start at index 6
                                               #and go until the index of the
                                                #second occurence of '"'
    return links
               
def remove_tags(text):
    '''(str) -> str
    Returns a str that is the full text of the web
    page with the HTML tags removed.
    >>> remove_tags('<b>abc</b>')
    'abc'
    >>> remove_tags('A<b>B</b>C')
    'ABC'
    >>> remove_tags('abc <a href="a.html">xyz</a>')
    'abc xyz'
    '''
    no_tags = ''
    i = 0
    while i < len(text):
        tag_start = text.find('<', i)
        if tag_start == -1:
            no_tags += text[i:]
        else:
            no_tags += text[i:tag_start]
            tag_end = text.find('>', tag_start)
            i = 0               #have to reset i so that 
        i += tag_end + 1        #when you increase it by tag_end + 1,
    return no_tags              #it will not go over len(text) 
            
def normalize_word(word):
    '''(str) -> str
    Returns a new word that only contains lowercase
    letters. All non-alphabetic characters in orignal
    word will be removed and uppercase letters will be
    lowercased.
    >>> normalize_word("That's")
    'thats'
    >>> normalize_word('NONE!')
    'none'
    >>> normalize_word('Hello, goodBYE!')
    'hellogoodbye'
    >>>
    '''
    if word.isalpha():
        return word.lower()
    else:
        new_word = ""
        for ch in word:
            if ch.isalpha():
                new_word += ch
        return new_word.lower()

def index_page(pagename, text, myindex):
    '''(str, str, dict) -> NoneType
    Modifies myindex in place by mapping
    words to lists of web pages on which
    those words are found.
    >>> myindex = {}
    >>> index_page('fake.html', '<b>I</b> HearT "CHOcolate!" chocolate', myindex)
    >>> myindex
    {'i' : ['fake.html'], 'heart' : ['fake.html'], chocolate : ['fake.html']}
    >>> index_page('fake2.html', '123 <a href="a.html">chocolate</a>', myindex)
    >>> myindex
    {'i' : ['fake.html'], 'heart' : ['fake.html'], 'chocolate' : ['fake.html', 'fake2.html']}
    '''
    no_tags = remove_tags(text)
    words = no_tags.split()
    for word in words:
        word = normalize_word(word)
        if word.isalpha():
            if word not in myindex:
                myindex[word] = [pagename]
            elif word in myindex:
                if pagename not in myindex[word]:
                    myindex[word] += [pagename]

def crawl_web(pagename, myindex, webgraph):         #written in class
    '''(str, dict, dict) -> NoneType
    Crawls pages reachable from pagename that have
    NOT ALREADY been crawled. Also updates myindex
    and webgraph. 
    '''
    print 'Crawling', pagename
    text = download_page(pagename)
    
    linked_pages = extract_links(text)
    
    webgraph[pagename] = linked_pages
    
    index_page(pagename, text, myindex)
    
    if len(linked_pages) == 0:
        print 'Finished', pagename
    else:
        for page in linked_pages:
            if page in webgraph:
                print 'Skipping', page
            else:
                crawl_web(page, myindex, webgraph)
        print 'Finished', pagename

def random_surfer_simulation(webgraph, p, simulation):  #written in class
    '''(dict, float, int) -> dict
    Returns a new dictionary that contains web page
    names as the keys, and computed page ranks as the values.
    >>> webgraph = {'fake1.html' : ['fake2.html', 'fake3.html'],
                    'fake2.html' : ['fake1.html'],
                    'fake3.html' : ['fake1.html']}
    >>> random_surfer_simulation(webgraph, 0, 10000)
    {'fake2.html' : 0.24903, 'fake3.html': 0.25097, 'fake1.html' : 0.5,}
    '''
    visits = {}
    for page in webgraph:
        visits[page] = 0

    current_page = random.choice(webgraph.keys())
    for num in range(simulation):
        r = random.random()
    
        if r <= p:
            current_page = random.choice(webgraph.keys())
        else:
            links = webgraph[current_page]
            current_page = random.choice(links)
        
        visits[current_page] += 1

    for page in visits:
        visits[page] = float(visits[page])/simulation
    
    return visits

def list_union(list_one, list_two):
    '''(list, list) -> list
    Returns a new list that contains all items
    that were contained in both lists, but
    eliminates duplicates.
    >>> list_union(['a.html', 'c.html'], ['a.html', 'b.html'])
    ['a.html', 'b.html', 'c.html']
    '''
    combined = list_one + list_two
    union = []
    for html in combined:
        if html not in union:
            union.append(html)
    return union

def list_intersection(list_one, list_two):
    '''(list, list) -> list
    Returns a new list that contains the items
    that are found in both lists.
    >>> list_intersection(['a.html', 'c.html'], ['a.html', 'b.html'])
    ['a.html']
    '''
    intersection = []
    for html in list_one:
        if html in list_two:
            intersection.append(html)
    return intersection

def list_difference(list_one, list_two):
    '''(list, list) -> list
    Returns a new list that contains the items
    found in the first list but not in the
    second list.
    >>> list_difference(['a.html', 'c.html'], ['a.html', 'b.html'])
    ['c.html']
    '''
    difference = []
    for html in list_one:
        if html not in list_two:
            difference.append(html)
    return difference

def get_query_hits(word, myindex):
    '''(str, dict) -> list
    Returns a list of all the page names
    that match the word.
    >>> myindex = {'dog' : ['fake.html']}
    >>> get_query_hits('dog', myindex)
    ['fake.html']
    >>> get_query_hits('cat', myindex)
    []
    '''
    pages = []
    for term in myindex:
        if term == word:
            pages += myindex[term]
    return pages

def process_query(query, myindex):              #written in class
    '''(str, dict) -> list
    Returns a list in any order of all
    the page names matching the query.
    >>> myindex = {'cat' : ['fake1.html', 'fake3.html'],
                    'dog': ['fake1.html', 'fake2.html', 'fake3.html'],
                    'android' : ['fake1.html']}
    >>> process_query('CAT dOg!!', myindex)
    ['fake1.html', 'fake2.html', 'fake3.html']
    >>> process_query('AND cat dog', myindex)
    ['fake1.html', 'fake3.html']
    >>> process_query('dog cat -android', myindex)
    ['fake2.html', 'fake3.html']
    '''
    terms = query.split()
    if terms[0] == 'AND':
        intersect = True
        terms.pop(0)                    #get rid of 'AND'
    else:
        intersect = False
        
    hits = get_query_hits(normalize_word(terms[0]), myindex)

    for term in terms[1:]:
        if not term.startswith('-'):
            term = normalize_word(term)
            term_hits = get_query_hits(term, myindex)
            if intersect:
                hits = list_intersection(hits, term_hits)
            else:
                hits = list_union(hits, term_hits)

    for term in terms:
        if term.startswith('-'):
            term = normalize_word(term[1:])
            term_hits = get_query_hits(term, myindex)
            hits = list_difference(hits, term_hits)
    return hits

def print_ranked_results(results, page_rank):
    '''(list, dict) -> NoneType
    Prints out the query results from highest
    to lowest.
    >>> page_rank = {'fake1.html' : 0.26, 'fake2.html' : 0.24, 'fake3.html' : 0.5}
    >>> reults = ['fake3.html', 'fake1.html', 'fake2.html']
    >>> print_ranked_results(results, page_rank)
    1: fake3.html (rank: 0.5)
    2: fake1.html (rank: 0.26)
    3: fake2.html (rank: 0.24)
    '''
    if len(results) == 0:
        print "No matches for search terms."
    else:
        page_ranks = []
        for page in results:
            if page in page_rank:
                page_ranks += [[page_rank[page], page]]
        page_ranks.sort()
        page_ranks.reverse()

        for i in range(len(page_ranks)):
            print str(i+1) + ": " + str(page_ranks[i][1]) + " (rank: " + str(page_ranks[i][0]) + ")"
            
def search_engine(myindex, page_rank):
    '''(dict, dict) -> NoneType
    Asks the user for a search query, processes the
    query to obtain the search results, and then
    prints out the ranked results, in order from
    highest to lowest.
    '''
    search = raw_input("Search terms? (enter 'DONE' to quit): ")
    while search != 'DONE':
        if search == 'DONE':
            break
        results = process_query(search, myindex)
        print_ranked_results(results, page_rank)
        search = raw_input("Search terms? (enter 'DONE' to quit): ")

def main():
    '''() -> NoneType
    Executes the mini search engine.
    '''
    print "Welcome to my mini search engine!"
    webgraph = {}
    myindex = {}
    crawl_web('a.html', myindex, webgraph)
    ranks = random_surfer_simulation(webgraph, 0.15, 100000)
    search_engine(myindex, ranks)
    print "Thanks for searching!"
