import os
from Bio import SeqIO


def pdb2fasta(pdb, fasta_path):
    with open(pdb, "r") as pdb_file:
        for record in SeqIO.parse(pdb_file, "pdb-atom"):
            pdb_id = pdb.split("/")[-2]
            with open(os.path.join(fasta_path, f"{pdb_id}.fasta"), "a") as f:
                f.write(">" + pdb_id + ":" + record.id.split(":")[-1] + "\n")
                f.write(str(record.seq) + "\n")


if __name__ == "__main__":
    fasta_path = "datasets/protein_fasta"
    if not os.path.exists(fasta_path):
        os.makedirs(fasta_path)

    pdb_path = "datasets/NOHETEROATOM_NDKB"
    pdbs = os.listdir(pdb_path)
    for pdb in pdbs:
        protein_pdb_path = os.path.join(pdb_path, pdb, f"{pdb}_protein.pdb")
        try:
            pdb2fasta(protein_pdb_path, fasta_path)
        except:
            print(pdb)
            continue
