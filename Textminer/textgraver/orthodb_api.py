#Module for retrieving orthologs for the found genes in the abstracts from the MongoDB servers
import requests
import simplejson as json
from time import sleep

#logfile to track any connection errors that may occur during runtime while connecting to OrthoDB
logfile = open('logfile_ortho.txt', 'a')
#a file containg all the plants wanted by the biology expert
anna_file = open("wanted_plants.txt", 'r')
anna = anna_file.read().splitlines()
anna_file.close()
#url for retrieving a list of entries mapping to a search query in OrthoDB
url_list = "http://www.orthodb.org/v9.1/search?query={}&level=&species=&universal=&singlecopy="
#url for retrieving all the orthologs of a specific gene in OrthoDB
url_ortho = "http://www.orthodb.org/tab?id={}&species="

#Base function for looping over all the genes present in articles_doc and calling functions for fetching orhtologs
def get_orthodb_orthologs(articles_doc):

    for a, article in enumerate(articles_doc):
        #print counter for every article in articles_doc
        print(a)
        pmid = article['pmid']
        species_doc = article['species']
        species = [x['name'] for x in species_doc]
        for s, spec in enumerate(species):
            genes = [x['name'] for x in species_doc[s]['genes']]
            for g, gene in enumerate(genes):
                wanted_orthologs_list = get_hit_list(url_list, gene, pmid)
                if wanted_orthologs_list is not None and len(wanted_orthologs_list) != 0:
                    for wanted in wanted_orthologs_list:
                        #append all wanted orthologs to articles_doc json
                        ortholog = wanted[0]
                        organism = wanted[1]
                        article['species'][s]['genes'][g]['orthologs'][ortholog] = organism
    logfile.close()
    articles_doc = json.dumps(articles_doc)
    return articles_doc

#Function for getting a list of hits for a gene name query in OrhtoDB
def get_hit_list(url, query, pmid):
    go = True
    attempt = 0
    while go:
        try:
            go = False
            r = requests.get(url.format(query))
            r_json = r.json()
            if len(r_json["data"]) > 0:
                #get first hit to continue to retrieving orhtologs from this particular hit
                first_hit = r_json["data"][0]
                wanted_list = get_orthologes(query, pmid, url_ortho, first_hit)
                return wanted_list
        except json.JSONDecodeError:
            print("JSON DECODE ERROR for " + query)
        except requests.ConnectionError:
            go = True
            attempt += 1
        except requests.ConnectTimeout:
            go = True
            attempt += 1
        except requests.HTTPError:
            go = True
            attempt += 1
        finally:
            if attempt > 2:
                sleep(3)
            if attempt > 3:
                logfile.write('Connection ERROR getting hitlist for ' + query + " in: " + pmid + '\n')
                go = False

#Function to retrieve all the orthologs
def get_orthologes(query, pmid, url, gene):
    go = True
    attempts = 0
    while go:
        try:
            r = requests.get(url.format(gene))
            content = r.text
            orthologs = content.split("\n")
            wanted_list = get_wanted_orgs(orthologs)
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
                logfile.write('Connection ERROR getting orthologs for ' + gene + " in: " + pmid + '\n')
                go = False
    return wanted_list

#Function to parse the content returned from OrthoDB
def get_wanted_orgs(orthologs):

    wanted_orthologs = []
    added_species = []

    #for line containing an ortholog, split the line into binominal name, genus and genus_id
    for orth in orthologs[1:len(orthologs)-1]:
        binominal = orth.split('\t')[4]
        genus = binominal.split()[0]
        gene_id = orth.split('\t')[6]
        #if an ortholog of a certain species for a gene is already added or not present in anna_species.txt, skip
        if genus.lower() in anna and binominal not in added_species:
            wanted_orthologs.append([gene_id, binominal])
            added_species.append(binominal)
    #append all wanted orthologs to a list and return
    wanted_orthologs_list = []
    for ort in wanted_orthologs:
        acc = ort[0]
        organism = ort[1]
        wanted_orthologs_list.append([acc, organism])
    return wanted_orthologs_list


