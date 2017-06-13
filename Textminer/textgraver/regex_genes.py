#Funtion to find genes in abstracts with regex additional to the genes from the Uniprot CBB API
import simplejson as json
import re

def get_regex_genes(articles_doc):
    #Loading the articles from the json file for gene analysis
    articles_doc = json.loads(articles_doc)
    articles_doc = articles_doc
    #splitting the article (for every article) in seperate words and check if the word is a gene or not
    #based on a regular expression.

    for article in articles_doc:

        abstract = article['abstract']
        words = abstract.split()
        for word in words:
            split = split_chars(word)
            for word in split:
                #Checking if a word has untwanted charachters, if they do they'll be removed
                if len(word) > 1 and (word[-1] == "," or word[-1] == "-"):
                    word = word[:-1]
                if len(word) > 1 and word[0] == "-":
                    word = word[1:]
                #Checking if a word meets the demands of being a gene if the word does and it isnt allready in the list of genes from the api_genes
                # it will be added to the list of genes.
                if (hasNumbers(word) or hasLowerUpper(word)) and upperLimit(word) and unwanted(word):
                    api_genes = [x['name'].lower() for x in article['genes']]
                    if word.lower() not in api_genes:
                        genes = article['genes']
                        genes.append({'name': word, 'orthologs': {}, 'eggnog': ''})
    #adding the gense to the json format
    articles_doc = json.dumps(articles_doc)
    #returning the json format of genes
    return articles_doc

#Function to check if a word contains numbers, returns a boolean
def hasNumbers(inputString):
    boolean = False
    if re.search(r'\d', inputString) and (re.search(r'([A-Za-z])', inputString)):
        boolean = True
    return boolean

#Function to check if a word contains lower and upper case characters, returns a boolean
def hasLowerUpper(inputString):
    boolean = False
    if re.search(r'([A-Za-z])+([A-Z])+([a-z])*(.)*', inputString):
        boolean = True
    return boolean

#Function to check when a word contains only uppercase characters it is within the range of 3-5, returns a boolean
def upperLimit(inputString):
    boolean = False
    if inputString.isupper():
        if re.match(r'[A-Z]{3,5}$', inputString):
            boolean = True
    else:
        boolean = True
    return boolean

def split_chars(inputString):
    output = re.findall(r'[\w\',-]+', inputString)
    return output

#Function to check if a word is an unwanted one, returns a boolean
def unwanted(inputString):
    boolean = True
    unwanted = ['induced', 'targeted', 'treated', 'involved', 'pretreated', 'negative', 'positive', 'insensitive',
                'dependent', 'independent', 'involved', 'control','scavenging', 'derived', 'protein', 'related', 'like',
                'mediated', 'related', 'responsive', 'enriched', 'overexpressing', 'governed', 'sensitive', 'absorbing',
                'produced', 'producing', 'associated', 'attributed', 'inflicted', 'ínitiated', 'elicited', 'activated',
                'supplemented', 'supplemental', 'repeat', 'enriched', 'damaging', 'signaling', 'deficient', 'guided']
    words = inputString.split('-')
    for word in words:
        if word.lower() in unwanted:
            boolean = False

    return boolean