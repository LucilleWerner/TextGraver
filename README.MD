# TextGraver
Welcome to our textmining web application. The application is divided in two directories, the web application which is running on a flask framework and a textmining analysis pipeline.

We'll shortly explain how to navigate through the coding and where everything can be found. We will do this for the web application as for the textmining pipeline

# Webapplication
The web application can be found in the Webapp directory. A few directories can be ignored for reviewing the code: 

-The Flask directory is a virtual environment which will be active on the server, the virtual environment makes it possible to install the required dependencies and packages for the Webapp without interfering with the rest of the server. 

-The .idea directory is part of the flask frame work and doesn't contain any coding done by us.

When we move to the app directory only the __pycache__ is to be ignored. A short description of what the other directories contain:

-static: css, fonts, images, javascript, json files 
-templates: contains all the HTML of the web application
-main.py: all the python that is used for the web app can be found here (besides the run.py and init.py but these are only for starting the webapp)

# Textmining pipeline
The texmining pipeline can be found in the Textgraver/Textminer directory. There are only 2 more nested directory here which are __pycache__ and .idea both can be ignored. The rest of the files are either coded by us or generated or used by the pipeline.

coded by us:

-main.py (our suggestion for reviewing the code is to follow the pipeline via the main function.)

-entrez_api.py

-id_mapper_eggnog.py

-mongo_retrieval.py

-ncbi_ccb_api.py

-orthodb_api.py

-regex_genes.py

-search_terms.py

-sunburst.py


Generated or used by the pipeline:

-all_plants.txt

-articles_doc.json

-articles_doc_ncbi_api_1024.p

-cooccurence_doc.json

-cooccurence_doc10.json

-speclist.txt

-sunburst_doc.json

-sunburst_doc10.json

-wanted_plants.txt




