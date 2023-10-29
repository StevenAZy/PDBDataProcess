import os
import json
import wget
import requests

# get all complex ids
def get_all_complex_ids(url, payload, save_path):
    resp = requests.get(url, params=payload)
    web_content =json.loads(resp.text[42:-2])

    complexs = web_content['response']['docs']
    with open(f'{save_path}/complexs.txt', 'w') as f:
        for complex in complexs:
            f.write(complex['id'] + '\n')

# download complex PDB file
def download_complexs(url, names, save_path):
    for name in names:
        wget_url = f'{url}/{name[:-1]}.pdb'

        if os.path.exists(f'{save_path}/{name[:-1]}.pdb'):
            continue
        
        try:
            wget.download(wget_url, out=f'{save_path}/{name[:-1]}.pdb')
        except:
            print(f'{name} can not be download!')