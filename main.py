import os
import redis
import threading

from config import *
from download_pdb import get_all_complex_ids, download_complexs
from process_pdb import split_complex, remove_heteroatom


if __name__ == '__main__':
    # get_all_complex_ids(COMPLEX_ID_URL, PAYLOAD, RECORD_FILE_PATH)

    # download all PDB
    complexs = []
    with open(RECORD_FILE_PATH, 'r') as f:
        complexs = f.readlines()

    complex_list = [[] for i in range(10)]
    # step = len(complexs) // 10
    for i in range(len(complexs)):
        complex_list[i % 10].append(complexs[i])
        # complex_list.append(complexs[i * step : (i + 1) * step]) # last element in i group is first element in i+1 group
    
    redis_conn = redis.Redis()
    for i in range(10):
        t = threading.Thread(target=download_complexs, args=(DOWNLOAD_URL, complex_list[i], PDB_SAVE_PATH, redis_conn))
        t.start()

    # split complexs
    downloaded_complexs = os.listdir(PDB_SAVE_PATH)
    downloaded_complexs_lsit = [[] for i in range(10)]
    for i in range(len(download_complexs)):
        downloaded_complexs_lsit[i % 10].append(downloaded_complexs[i])

    for i in range(10):
        t = threading.Thread(target=split_complex, args=(PDB_SAVE_PATH, SPLIT_PDB_SAVE_PATH, downloaded_complexs_lsit[i]))
        t.start()

    # remove heteroatom
    remove_heteroatom_complexs = os.listdir(SPLIT_PDB_SAVE_PATH)
    remove_heteroatom_complexs_lsit = [[] for i in range(10)]
    for i in range(len(remove_heteroatom_complexs)):
        remove_heteroatom_complexs_lsit[i % 10].append(downloaded_complexs[i])

    for i in range(10):
        t = threading.Thread(target=remove_heteroatom, args=(SPLIT_PDB_SAVE_PATH, NOHETEROATOM_PDB_SAVE_PATH,  remove_heteroatom_complexs_lsit[i]))
        t.start()



    