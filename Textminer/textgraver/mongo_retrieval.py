#Module for retrieving data from the Mongo Database, writes the result to .json files via command line bash script,
#these files are later used in the webapp for vizualizing a coccurence graph.
import subprocess
from pymongo import MongoClient

#Function for calling the processes to write results to .json file
def fill_graph_files():

    #calling a subprocess to retrieve the data for the sunburst and store it in a json file.
    subprocess.call("mongoexport --db TextGraver2 -c sunburst -o sunburst.json --jsonArray", shell=True)
    #calling a subprocess to retrieve the data for the graph and store it in a json file.
    subprocess.call("mongoexport --db TextGraver2 -c graaf -o graaf.json --jsonArray", shell=True)

#Data retrieval from MongoDB with Mongo queries
def data_retrieval():
    #Connecting to the correct database
    client = MongoClient()
    db = client.TextGraver2

    #selecting the collection with all the data produced by the textmining analysis
    collection = db.articles
    #Retrieving all the genes from the database with Mongo query
    result_genes = collection.find({}, { 'genes': 1})

    #creating a file for the results
    gene_file = open("genes.txt", "w")
    #For every result it will written in the results file.
    for entry in result_genes:
        gene_file.write((str(entry)))
        gene_file.write("\n")
    gene_file.close()

    #Retrieving all the unique stresses from the database with Mongo query
    result_distinct = collection.distinct("stress")
    #Creating a file for the results
    distinct_stresses = open("distinct_stresses.txt", "w")
    #For every result it will written in the results file.
    for entry in result_distinct:
        distinct_stresses.write(entry)
        distinct_stresses.write("\n")
    distinct_stresses.close()

#Base function to call both fill_graph and data_retrieval from main
def retrieval_calls():
    fill_graph_files()
    data_retrieval()
