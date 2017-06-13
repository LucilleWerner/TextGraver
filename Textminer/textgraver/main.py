#Application for textmining of Pubmed articles with the search terms 'anthocyanin' and 'stress' to find relations
#between these two variables in plants, the application retrieves genes, chemicals and organims from the abstracts
#and retrieves additional information such as orthologs from the genes.
#Information is pushed to a MongoDB, a webapplication visualises the data in a sunburst and a cooccurence graph
#TextGraver version 1.00
#Date: 13/06/2017
#Authors: Jeffrey Hiraki, Jasper de Meijer, Heleen Severin, Sanne Geraerts

import simplejson as json
import pickle
import entrez_api
import ncbi_ccb_api
import regex_genes
import id_mapper_eggnog
import orthodb_api
import search_terms
import sunburst
import mongodb_fill
import mongo_retrieval


def main():


    idlist, articles_doc = entrez_api.pm_ids()

    articles_doc = ncbi_ccb_api.ncbi_gene(idlist, articles_doc)

    articles_doc = regex_genes.get_regex_genes(articles_doc)

    articles_doc = id_mapper_eggnog.species_identifier(articles_doc)

    articles_doc = orthodb_api.get_orthodb_orthologs(articles_doc)

    articles_doc, cooccurence_doc = search_terms.search_terms(articles_doc)

    sunburst_doc = sunburst.construct_stress_sunflare(articles_doc)

    mongodb_fill.fill_database(articles_doc, cooccurence_doc, sunburst_doc)

    mongo_retrieval.retrieval_calls()

    sunburst_doc = json.dumps(sunburst_doc)

    file_articles = open('articles_doc.json', 'w')
    file_articles.write(articles_doc)
    file_articles.close()

    pickle.dump(articles_doc, open('articles_doc_pickle.p', 'wb'))

    file_sunburst = open('sunburst_doc.json', 'w')
    file_sunburst.write(sunburst_doc)
    file_sunburst.close()

    pickle.dump(sunburst_doc, open('sunburst_doc_pickle.p', 'wb'))

    file_cooccurence = open('cooccurence_doc.json', 'w')
    file_cooccurence.write(cooccurence_doc)
    file_cooccurence.close()

    pickle.dump(cooccurence_doc, open('cooccurence_doc_pickle.p', 'wb'))


main()


"""
sample json format 'articles_doc'

articles = [
   {  "pmid":"28534253",
      "title":"High throughput ST08 gene..",
      "author":["Lucas, J", "Salanter, A"],
      "source":"Journal of biomedical, Atlanta, 2008",
      "date":"20170809",
      "abstract":"Transcriptomics, Targeted Metabolomics and Gene Expression of",
      "species":[{"name":"olifant","genes":[{
                  "name":"tnf-a",
                  "eggnog_id":"EGNOG8930",
                  "orthologs":{
                     "tnf-b":"solanum",
                     "tnf-c":"burbur"}}]}
      ],
      "chemicals":[
         "anthocyanin"
      ],
      "stress":[
         "salt",
         "cold"
      ],
      "correlation":[
         "increase"
      ],
      "cultivation":[
         "in vivo"
      ]
   }
]
"""