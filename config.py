# url getting complex id
COMPLEX_ID_URL = "https://www.nakb.org/node/solr/nakb/select"
# PDB download url
DOWNLOAD_URL = "https://files.rcsb.org/download"
RECORD_FILE_PATH = ""
PDB_SAVE_PATH = ""
SPLIT_PDB_SAVE_PATH = "datasets/SPLIT_NDKB"
NOHETEROATOM_PDB_SAVE_PATH = "datasets/NOHETEROATOM_NDKB"

PAYLOAD = {
    "json.wrf": "jQuery331009641711943862963_1695358912164",
    "wt": "json",
    "q": "only RNA AND Protein",
    "fq": "naclass:RNA",
    "fq": "polyclass:Protein*",
    "fq": "resolution:[0 TO 3.5]",
    "fl": "id,pdbid,ndbid,assembly_nachains,emdbids,bmrbid,status,polyclass,NDBstrand,NDBnasum,NAKBprotsum,NAKBnasum,title,author.name,deposited,released,resolution,method,exptlmethod,molweight,PMID,DOI,spacegroup,cell.*",
    "rows": 2780,
    "sort": "released_sort desc",
    "_": 1695262162168,
}


from local_config import *
