from pymongo import MongoClient
import pickle
import simplejson as json

def fill_database():
    #Opening connection to the local mongo database
    client = MongoClient()
    #selecting the database, or when it doesnt exist create one
    db = client.TextGraver2

    #preprocessing the json file for writing to the database
    articles_doc = open("../articles_doc.json")
    articles_doc_buffer = articles_doc.read()
    articles_doc_json = json.loads(articles_doc_buffer)
    #creating a collection in the datase
    collection_articles = db.articles
    #Clearing the collection before filling it with the new analysis
    db.collection_articles.delete_many({})

    #preprocessing the json file for writing to the database
    graaf_doc = open("../cooccurence_doc10.json")
    graaf_doc_buffer = graaf_doc.read()
    graaf_doc_json = json.loads(graaf_doc_buffer)

    #creating a collection in the datase
    collection_graaf = db.graaf
    #Clearing the collection before filling it with the new analysis
    db.collection_graaf.delete_many({})

    #preprocessing the json file for writing to the database
    sunburst_doc = open("../sunburst_doc10.json")
    sunburst_doc_buffer = sunburst_doc.read()
    sunburst_doc_json = json.loads(sunburst_doc_buffer)

    #creating a collection in the datase
    collection_sunburst = db.sunburst
    #Clearing the collection before filling it with the new analysis
    db.collection_sunburst.delete_many({})

    #The next three loops are for exporting the files into the corresponding collections
    for article in articles_doc_json:
        collection_articles.insert(article, check_keys = False)

    for graaf in graaf_doc_json:
        collection_graaf.insert(graaf, check_keys = False)

    for sunburst in sunburst_doc_json:
        collection_sunburst.insert(sunburst, check_keys = False)

def main():
    fill_database()

main()
