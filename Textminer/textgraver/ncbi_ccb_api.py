#Functions for making request to NCBI CBB for the gene, chemical and organism indices for the corresponding PMID
#NCBI CBB consists of textmining web services for annotating pubmed articles, these services are machine learning programs
#for identifying chemicals(tmChem), species(SR4GN), disease(DNorm), mutation(tmVar) and genes/proteins(GNormplus)
#a GET request retrieves preannoted data from the database, a POST request executes a new analysis of text
import simplejson as json
import requests
from time import sleep

#logfile to track any connection errors that may occur during runtime while connecting to NCBI
logfile = open('logfile_ncbi_api.txt', 'a')
def ncbi_gene(idlist, articles_doc):

    #load the articles_doc dictionary containing all the abstract info to a json format
    articles_doc = json.loads(articles_doc)
    articles_doc_update = list()

    for a, article in enumerate(articles_doc):
        #print counter for every article in the loop
        print(a)
        attempts = 0
        go = True
        method = 'get'
        #while no exception occured or while there were more than 3 attemps to fetch the data from NCBI
        while go:
            try:
                pmid = article['pmid']
                #request for preannoted data on the pubmed CBB database for a certain article (pubmed id)
                custom_url = "https://www.ncbi.nlm.nih.gov/CBBresearch/Lu/Demo/RESTful/tmTool.cgi/bioconcept/{}/JSON".format(pmid)
                if method == 'get':
                    r = requests.get(custom_url)
                #not functional: do a POST request when preannotad data is not present on the server
                else:
                    r = requests.post(custom_url)
                json_article = r.json()
                article_update = parse_json(json_article, article)
                articles_doc_update.append(article_update)
                go = False
            except json.JSONDecodeError:
                    go = False
            except requests.ConnectTimeout:
                attempts += 1
            except requests.ConnectionError:
                attempts += 1
            except requests.HTTPError:
                attempts += 1
            finally:
                if attempts > 2:
                    sleep(3)
                if attempts > 3:
                    logfile.write('Connection ERROR getting orthologs for ' + '\n')
                    go = False

    logfile.close()
    articles_doc_update = json.dumps(articles_doc_update)
    return articles_doc_update

#Function for parsing json format response from NCBI CBB
def parse_json(json_article, article):

    genes = []
    chemicals = []
    abstract = ""

    abstract = json_article['text']
    #parse embedded denotation for indices of genes and chemicals, indices are from abstract where the annotations originate from
    for denot in json_article['denotations']:
        if denot['obj'].split(":")[0] == 'Gene':
            genes.append([denot['span']['begin'],denot['span']['end']])
        if denot['obj'].split(":")[0] == "Chemical":
            chemicals.append([denot['span']['begin'],denot['span']['end']])

    #if genes or chemicals not present, return empty list
    if len(genes) == 0:
        genes.append([])
    if len(chemicals) == 0:
        chemicals.append([])

    indices = [genes, chemicals]

    article_update = pull_info_abstract(indices, abstract, article)

    return article_update

#Function to pull info (genes and chemicals) out of abstract with indices from the json format
def pull_info_abstract(indices, abstract, article):

    genes = indices[0]
    chemicals = indices[1]

    #for every gene indices, get gene from abstract and append to full info json document
    genes_doc = []
    for gene in genes:
        if len(gene) != 0:
            gene_doc = {}
            start = gene[0]
            end = gene[1]
            gene_doc['name'] = abstract[start:end]
            gene_doc['orthologs'] = []
            gene_doc['eggnog'] = ''
            genes_doc.append(gene_doc)
    # for every chemical indices, get chemical from abstract and append to full info json document
    chemicals_doc = []
    for chemical in chemicals:
        if len(chemical) != 0:
            start = chemical[0]
            end = chemical[1]
            chemicals_doc.append(abstract[start:end])
    #update full info json doc with abstract, genes and chemicals
    article['abstract'] = abstract
    article['genes'] = genes_doc
    article['chemicals'] = chemicals_doc

    return article



