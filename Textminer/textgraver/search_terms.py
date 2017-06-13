#Module for searcing correlation terms, stress terms and cultivation terms in abstracts and computing the cooccurence
#of all the terms for a visualisation in a cooccurence graph
import simplejson as json
import re

correlation_terms = {"increase": "increase", "enhance": "increase", "induce": "increase", "rise": "increase",
                     "increase": "accumulation",
                     "reduction": "decrease", "decrease": "decrease", "lessen": "decrease", "decline": "decrease",
                     "declining": "decrease",
                     "positive correlated": "positive", "positively": "positive", "positively regulated": "positive",
                     "positive association": "positive",
                     "negatively": "negative", "negatively correlated": "negatative",
                     "negatively regulated": "negative", "negative association": "negative"}
stress_terms = {"drought": "drought", " dry ": "drought", "dehydrate": "drought", "osmotic": "osmotic",
                "water": "osmotic",
                "salinity": "salinity", "salin": "salinity", "acidity": "acidity", "salt": "salinity",
                "high temperature": "high temperature", "high-temperature": "high temperature",
                "heat": "high temperature",
                "low temperature": "low temperature",
                "low-temperature": "low temperature", "chilling": "low temperature", "cold": "low temperature",
                "freezing":
                    "low temperature",
                "high-light": " high light", "high light": " high light", "low-light": "low light",
                "dark-treatment": "low light", "dark exposure": "low light",
                "darkness": "low light", "oxidative": "oxidative", "ultraviolet": "ultraviolet", "UV": "ultraviolet"}
cultivation_terms = {"in vivo": "in vivo", "cultivar": "cultivar", "green-house": "cultivar", "in vitro": "in vitro",
                     "in-vitro":
                         "in vitro", "ornamental": "house plant"}

#Function for searching all the terms in the abstract and appending info to articles doc (all info)
def search_terms(articles_doc):

    articles_doc = json.loads(articles_doc)
    cooccurence_doc = []

    #for entry in articles_doc, get abstract
    for article in articles_doc:
        abstract = article['abstract']
        correlations = list()
        #for every abstract, find correlation terms
        for correlation in correlation_terms:
            found = abstract.find(correlation)
            if found != -1:
                correlations.append(correlation_terms.get(correlation))
        # for every abstract, find stress terms
        stresses = list()
        for stress in stress_terms:
            found = abstract.find(stress)
            if found != -1:
                stresses.append(stress_terms.get(stress))
        # for every abstract, find cultivation terms
        cultivations = list()
        for condition in cultivation_terms:
            found = abstract.find(condition)
            if found != -1:
                cultivations.append(cultivation_terms.get(condition))
        #append to articles doc json
        article['correlation'] = correlations
        article['stress'] = stresses
        article['cultivation'] = cultivations

        cooccurence_doc = cooccurence(article, correlations, stresses, cultivations, cooccurence_doc)

    articles_doc = json.dumps(articles_doc)
    cooccurence_doc = json.dumps(cooccurence_doc)

    return articles_doc, cooccurence_doc

#Function for finding cooccurence of all the terms combined
def cooccurence(article, correlations, stresses, cultivations, cooccurence_doc):

    #get a list of the complete genes in articles doc
    genes = []
    for s, species in enumerate(article['species']):
        for gene in article['species'][s]['genes']:
            genes.append(gene['name'])
    species = [x['name'] for x in article['species']]

    abstract = article['abstract']
    #split on dot followed by a space and a capital or a number to split all the abstracts into lines
    lines = re.split(r' *[\.\?!] [A-Z0-9]', abstract)

    correlation_indices = {}
    stress_indices = {}
    cultivation_indices = {}
    gene_indices = {}
    species_indices = {}

    #get all the indices of the found correlations, stresses, cultivations, genes and species (indices are for determining
    #if two terms occur in the same sentence of only occur in the same abstract
    for n, line in enumerate(lines):
        for cor in correlations:
            cor_index = line.find(cor)
            if cor_index != 0:
                correlation_indices[cor] = n
        for stress in stresses:
            stress_index = line.find(stress)
            if stress_index != 0:
                stress_indices[stress] = n
        for cult in cultivations:
            cultivation_index = line.find(cult)
            if cultivation_index != 0:
                cultivation_indices[cult] = n
        for gene in genes:
            gene_index = line.find(gene)
            if gene_index != 0:
                gene_indices[gene] = n
        for spec in species:
            species_index = line.find(spec)
            if species_index != 0:
                species_indices[spec] = n

    #Check cooccurence of all the terms with all the possible combinations (math: 4!: 4x3x2x1)
    #Pass the indices information to determine score
    for gene in gene_indices:
        for species in species_indices:
            cooccurence_doc = check_cooccurence(cooccurence_doc, gene, species, gene_indices, species_indices, correlation_indices)
        for stress in stress_indices:
            cooccurence_doc = check_cooccurence(cooccurence_doc, gene, stress, gene_indices, stress_indices, correlation_indices)
        for cultivation in cultivation_indices:
            cooccurence_doc = check_cooccurence(cooccurence_doc, gene, cultivation, gene_indices, cultivation_indices, correlation_indices)
    for spec in species_indices:
        for stress in stress_indices:
            cooccurence_doc = check_cooccurence(cooccurence_doc, spec, stress, species_indices, stress_indices, correlation_indices)
        for cultivation in cultivation_indices:
            cooccurence_doc = check_cooccurence(cooccurence_doc, spec, cultivation, gene_indices, cultivation_indices, correlation_indices)
    for stress in stress_indices:
        for cultivation in cultivation_indices:
            cooccurence_doc = check_cooccurence(cooccurence_doc, stress, cultivation, stress_indices, cultivation_indices, correlation_indices)

    return cooccurence_doc

#Check cooccurence of all the terms from all the abstracts, check if it occures in the same sentence (= higher score_
def check_cooccurence(cooccurence_doc, term1, term2, term1_indices, term2_indices, correlation_indices):
    term1_index = term1_indices.get(term1)
    term2_index = term2_indices.get(term2)

    #default score for occuring in the same abstract
    score = 10
    if term1_index == term2_index:
        score = 30
        for correlation in correlation_indices:
            #if terms occur in the same sentence, higher score
            if correlation_indices[correlation] == term1_index:
                #if 'negative' or 'positives' in sentence, higher score
                if correlation_terms.get(correlation) in ['increase', 'positive']:
                    score += 1
                #if 'decrease' or 'negative' occurs in the sentence, lower score
                elif correlation_terms.get(correlation) in ['decrease', 'negative']:
                    score -= 5
    type = determine_type(score)

    #if the cooccurence between two terms is already present in json cooccurence doc, as the first term of second term,
    #dont add, else add to json cooccurence doc
    present = False
    for cooccurence in cooccurence_doc:
        if cooccurence['source'] == term1 and cooccurence['target'] == term2 or \
           cooccurence['source'] == term2 and cooccurence['target'] == term1:
            cooccurence['type'] = type
            present = True
    if not present:
        cooccurence_doc.append({'source': term1, 'target': term2, 'type': type})

    return cooccurence_doc

#Function for determining color of edges in json cooccurence graph based on score
def determine_type(score):

    if score < 50:
         type = "gray"
    elif score in range(50,100):
        type = "green"
    elif score in range(100,200):
        type = "blue"
    elif type in range(200,300):
        type = "purple"
    else:
        type = "red"

    return type




