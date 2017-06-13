import requests
import simplejson as json
from time import sleep

logfile = open('logfile_ortho.txt', 'a')

anna_file = open("wanted_plants.txt", 'r')
anna = anna_file.read().splitlines()
anna_file.close()

url_list = "http://www.orthodb.org/v9.1/search?query={}&level=&species=&universal=&singlecopy="
url_ortho = "http://www.orthodb.org/tab?id={}&species="

def get_orthodb_orthologs(articles_doc):

    for a, article in enumerate(articles_doc):
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
                        ortholog = wanted[0]
                        organism = wanted[1]
                        article['species'][s]['genes'][g]['orthologs'][ortholog] = organism
    logfile.close()
    articles_doc = json.dumps(articles_doc)
    return articles_doc

def get_hit_list(url, query, pmid):
    go = True
    attempt = 0
    while go:
        try:
            go = False
            r = requests.get(url.format(query))
            r_json = r.json()
            if len(r_json["data"]) > 0:
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


def get_orthologes(query, pmid, url, gene):
    go = True
    attempts = 0
    while go:
        try:
            r = requests.get(url.format(gene))
            content = r.text
            orthologs = content.split("\n")
            wanted_list = get_wanted_orgs(query, orthologs)
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


def get_wanted_orgs(query, orthologs):

    wanted_orthologs = []
    added_species = []

    for orth in orthologs[1:len(orthologs)-1]:
        binominal = orth.split('\t')[4]
        genus = binominal.split()[0]
        gene_id = orth.split('\t')[6]
        if genus.lower() in anna and binominal not in added_species:
            wanted_orthologs.append([gene_id, binominal])
            added_species.append(binominal)

    wanted_orthologs_list = []
    for ort in wanted_orthologs:
        acc = ort[0]
        organism = ort[1]
        wanted_orthologs_list.append([acc, organism])
    return wanted_orthologs_list


