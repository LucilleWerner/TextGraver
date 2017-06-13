#Module for retrieving a list of Uniprot IDsassociated with a gene name, this functionalty enables the retrieval \
#of EggNOG IDs for showing an EggNOG phylogenetic tree in the webapp
import requests
from time import sleep
import simplejson as json

#logfile to track any connection errors that may occur during runtime while connecting to Uniprot
logfile = open('idmapper_logfile.txt', 'a')
#list containing all the plant species present in the Uniprot database
file = open('speclist.txt', 'r')
spec_file = file.read().splitlines()
# Loading the all plants file which contains all (by uniprot) known abbrevations for plants.
species_file = open("all_plants.txt")
species_lines = species_file.read().splitlines()


#Function for translating gene names to Uniprot ID's
def species_identifier(articles_doc):
    #Defining the api URL
    uni_url = 'http://www.uniprot.org/uploadlists/'
    #Loading the gene file, should be replaced by JSON logic
    articles_doc = json.loads(articles_doc)

    #Loops over the list of genes and requests uniprot to translate the genename to uniprot IDs
    for a, article in enumerate(articles_doc):
        print(a)
        genes = [x['name'] for x in article['genes']]
        for n, gene in enumerate(genes):
            attempt = 0
            go = True
            while go:
                try:
                    counter = n
                    #Defining parameters for the uniprot api
                    payload = {
                    'from': 'GENENAME',
                    'to': 'ID',
                    'format': 'list',
                    'query': gene
                    }
                    uniprot_id_request = requests.get(uni_url, params= payload)
                    text1 = uniprot_id_request.text
                    textsplit = text1.split()
                    #check is used to check if a result needs to be saved or not.

                    #Loops over the list of uniprot IDsand checks if it is in the list of plants
                    #if it is in the list of plants it wil request uniprot to translate the uniprot id to an EggNOG id and save this result.
                    #It will only save the first result which is a plant and has a EggNOG id.

                    if textsplit is not None or len(textsplit) != 0:
                        uniprot_ids = []
                        for x in textsplit:
                            #second part of the Uniprot ID contains a species mnemonic (often a abbreviation)
                            species = x.split("_")[1]
                            #Checks if it is a plant by comparing with the speclist.txt file
                            if species in species_lines:
                                uniprot_ids.append(x)
                        update_json_record(uniprot_ids, gene, species, article)

                    go = False
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
                        logfile.write('ERROR for ' + gene + " in: " + article['pmid'] + '\n')
                        go = False
    logfile.close()
    return articles_doc

#Function for updating the json record with the full information from the articles
def update_json_record(uniprot_ids, gene, species, article):

    #Fetch bionominal name for mnemonic
    binominal = fetch_full_species(species)

    #gene document compatible with json format with substructures for orthologs and Uniprot IDs
    gene_doc = {'name': gene, 'orthologs':{}, 'uniprot_ids': uniprot_ids}
    species = article['species']
    all_species = [x['name'] for x in species]
    # Checks if the species name is already present in the json record for a certain article
    if binominal in all_species:
        for n, spec in enumerate(species):
            if species[n]['name'] == binominal:
                species_doc = species[n]
    #Else: create a new record for the species name with a substructure for genes
    else:
        species_doc = {'name': binominal, 'genes': []}
        species.append(species_doc)
    genes = species_doc['genes']
    all_genes = [x['name'] for x in genes]
    #If the gene is not already present in the articles_doc json for this particular species, append to the doc
    if gene not in all_genes:
        genes.append(gene_doc)


#Function for retrieving the full (binominal) name for a Uniprot mnemonic by scanning speclist.txt
def fetch_full_species(species):

    #binominal name is in the same line as mnemonic
    for line in spec_file:
        if species and "N=" in line:
            binominal = line.split("N=")[1].strip()
        #if the full species name is not present in the file, return the name as the mnemonic
        else:
            binominal = species

    return binominal
