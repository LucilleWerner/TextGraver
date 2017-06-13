#Defining parameters for the uniprot api

def fetch_eggnog_id():
    payload_to_eggnog = {
    'from': 'ID',
    'to': 'EGGNOG_ID',
    'format': 'list',
    'query': x
    }
    #Uses the predefined parameters to request uniprot to translate an uniprot id to an eggnog id
    eggnog_id_request = requests.get(uni_url, params = payload_to_eggnog)

    #Builds a list based on the uniprot api results
    eggnog_id_text = eggnog_id_request.text
    eggnog_id_list = eggnog_id_text.split()

    #Checks if the list with eggnog id's isn't empty.
    if eggnog_id_list:
        #writes the results to a file, should be replaced by JSON logic
        eggnog_id = eggnog_id_list[0]
        update_json_record(eggnog_id, gene, species, article)
        #makes sure only 1 eggnog id is saved per genename.