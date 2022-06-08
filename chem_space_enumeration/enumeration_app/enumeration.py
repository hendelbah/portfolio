from rdkit import Chem
from rdkit.Chem.EnumerateStereoisomers import EnumerateStereoisomers


def create_spiro_mol(seq1: tuple[int], seq2: tuple[int]) -> Chem.rdchem.Mol:
    """
    Create spirocycle, combining 2 sequences of atoms with spiro-carbon.
    In each sequence atoms are connected in series, then terminal atoms
    are bonded to spiro-carbon.\n
    :param seq1: first atom sequence
    :param seq2: second atom sequence
    :return: Mol object, spirocycle
    """
    mol = Chem.RWMol()
    atoms = (6,) + seq1 + seq2
    atom_indices = [mol.AddAtom(Chem.Atom(atom)) for atom in atoms]
    for i, idx1 in enumerate(atom_indices):
        idx2 = atom_indices[i - 1]
        if i == len(seq1) + 1:
            # when current atom is first from seq2, instead of bonding it
            # to previous(last from seq1), bond them both to spiro-carbon(first in atoms)
            mol.AddBond(0, idx2, Chem.rdchem.BondType.SINGLE)
            idx2 = 0
        mol.AddBond(idx1, idx2, Chem.rdchem.BondType.SINGLE)
    mol = mol.GetMol()
    mol.UpdatePropertyCache()
    return mol


def generate_atom_sequences(max_len: int, max_hetero: int,
                            heteroatoms=(7, 8, 16)) -> list[tuple[int]]:
    """
    Generate all possible unique combinations(sequences) of carbon and given heteroatoms
    with restrictions of size(max is given, min is 2) and max number of heteroatoms.
    If sequence in reverse matches already generated one(e.g. 123-321),
    it is considered not unique and is skipped.\n
    :param max_len: max number of atoms in sequence
    :param max_hetero: max number of heteroatoms
    :param heteroatoms: tuple of available heteroatoms as atom numbers
    :return: sorted list of atomic number tuples
    """
    sequences = set()

    def recursively_enumerate(sequence=tuple(), hetero_count=0):
        if len(sequence) > 1 and hetero_count > 0 and sequence[::-1] not in sequences:
            sequences.add(sequence)
        if len(sequence) < max_len:
            recursively_enumerate(sequence + (6,), hetero_count)
            if hetero_count < max_hetero and (not sequence or sequence[-1] == 6):
                for het in heteroatoms:
                    recursively_enumerate(sequence + (het,), hetero_count + 1)

    recursively_enumerate()
    sequences = sorted(sequences)
    sequences.sort(key=len)
    return sequences


def generate_spiro_cycles_smiles(seq_list1: list, seq_list2: list = None) -> list[str]:
    """
    Create spirocycles, combining atom sequences from 2 lists with and using
    `create_spiro_mol` function, then enumerate stereo isomers and generate
    SMILES strings for them. Different sequence lists allow to control atoms in
    separate rings of spirocycle, though second list is optional.\n
    :return: list of SMILES strings
    """
    seq_list2 = seq_list1 if seq_list2 is None else seq_list2
    spiro_cycles_smiles = []

    for idx_a, seq1 in enumerate(seq_list1):
        for idx_b, seq2 in enumerate(seq_list2):
            terminal_atoms = (seq1[0], seq1[-1], seq2[0], seq2[-1])
            if (seq_list1 is seq_list2 and idx_a < idx_b) or 6 not in terminal_atoms:
                continue
            mol = create_spiro_mol(seq1, seq2)
            Chem.FindMolChiralCenters(mol, includeUnassigned=True)
            for isomer in EnumerateStereoisomers(mol):
                smiles = Chem.MolToSmiles(isomer)
                spiro_cycles_smiles.append(smiles)
    return spiro_cycles_smiles
