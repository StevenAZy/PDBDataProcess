import os

from Bio.PDB import is_aa
from Bio.PDB import PDBParser, PDBIO, Select

class ProtSelect(Select):
    def accept_residue(self, residue):
        return 1 if is_aa(residue) == True else 0

class RNASelect(Select):
    def accept_residue(self, residue):
        return 1 if is_aa(residue) == False and residue.id[0] != "W" else 0

# remove heteroatom
class RemoveHeteroatoms(Select):
    def accept_residue(self, residue):
        return 1 if residue.id[0] == " " else 0


# split complex into protein and RNA  
def split_complex(src_path, save_path, complexs):
    for complex in complexs:
        # path = os.path.join(src_path, complex)
        path = os.path.join(save_path, complex.lower())

        if not os.path.exists(path):
            os.makedirs(path)

        pdb = PDBParser().get_structure(complex, f'{src_path}/{complex}.pdb')
        io = PDBIO()
        io.set_structure(pdb)
        io.save(f'{path}/{complex.lower()}_protein.pdb', ProtSelect())
        io.save(f'{path}/{complex.lower()}_ligand.pdb', RNASelect())

# remove heteroatom
def remove_heteroatom(src_path, save_path, complexs):
    for complex in complexs:
        path = os.path.join(src_path, complex)
        dst_path = os.path.join(save_path, complex.lower())

        if not os.path.exists(dst_path):
            os.makedirs(dst_path)

        pdb = PDBParser().get_structure(complex, f'{path}/{complex}_protein.pdb')
        io = PDBIO()
        io.set_structure(pdb)
        io.save(f'{dst_path}/{complex.lower()}_protein.pdb', RemoveHeteroatoms())

        pdb = PDBParser().get_structure(complex, f'{path}/{complex}_ligand.pdb')
        io = PDBIO()
        io.set_structure(pdb)
        io.save(f'{dst_path}/{complex.lower()}_ligand.pdb', RemoveHeteroatoms())
