#Module for getting a list containing the PUBMED ID's with a hit on anthocyanin and stress
import simplejson as json
from Bio import Entrez
from Bio import Medline

def pm_ids():
    Entrez.email = "severin@student.han.nl"     # Always tell NCBI who you are
    #searching pubmed with specific 'terms', entrez will retrieve pubmed id's which will be parsed.
    handle = Entrez.egquery(term="anthocyanin stress")
    record = Entrez.read(handle)

    # for row in record["eGQueryResult"]:
    #     if row["DbName"]=="pubmed":
    #          print(row["Count"])
    #searching pubmed with specific 'terms', entrez will retrieve pubmed id's which will be parsed.
    handle = Entrez.esearch(db="pubmed", term="anthocyanin stress", retmax=8000)
    #parsing of the entrez request
    record = Entrez.read(handle)
    idlist = record["IdList"]

    #medline is used to retrieve an easy readable format of the articles, which will be used for the json format
    handle = Entrez.efetch(db="pubmed", id=idlist, rettype="medline",
                           retmode="text")
    #parsing the medline request
    records = Medline.parse(handle)

    records = list(records)

    articles = list()

    #get the Pubmed ID, title, authors, source and date from Medline records
    for record in records:
        pmid = record.get("PMID", "?")
        title = record.get("TI", "?")
        author = record.get("AU", "?")
        source = record.get("SO", "?")
        date = record.get("EDAT", "?")

        # creating a json format for storing the article data.
        articles.append({
            'pmid': pmid,
            'title': title,
            'author': author,
            'source': source,
            'date': date,
            'abstract': '',
            'genes': [],
            'species': [],
            'chemicals': [],
            'stress': [],
            'correlation': [],
            'cultivation': []
        })

    articles = json.dumps(articles)
    #returning the list of pubmed id's and the information about the articles in a json format.
    return idlist, articles