import redis

from config import DOWNLOAD_URL, PDB_SAVE_PATH
from download_pdb import download_complexs


redis_conn = redis.Redis(decode_responses=True)
keys = redis_conn.keys()

failure_pdb = []
for key in keys:
    if "failure" in key:
        failure_pdb.append(key.split("_")[-1][0:-1])

download_complexs(DOWNLOAD_URL, failure_pdb, PDB_SAVE_PATH, redis_conn)
