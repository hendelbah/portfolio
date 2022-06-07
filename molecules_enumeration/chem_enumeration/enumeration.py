from rdkit import Chem
from rdkit.Chem.EnumerateStereoisomers import EnumerateStereoisomers


def create_spiro_mol(chain_1: tuple[int], chain_2: tuple[int]):
    """
    Combine 2 atom chains, linking their ends to spiro-carbon atom and create RDKit `Mol` object
    :param chain_1:
    :param chain_2:
    :return: Mol object
    """
    mol = Chem.RWMol()
    atom_indices = [mol.AddAtom(Chem.Atom(atom)) for atom in (6,) + chain_1 + chain_2]
    for i, idx1 in enumerate(atom_indices):
        idx2 = atom_indices[i - 1]
        if i == len(chain_1) + 1:
            mol.AddBond(0, idx2, Chem.rdchem.BondType.SINGLE)
            idx2 = 0
        mol.AddBond(idx1, idx2, Chem.rdchem.BondType.SINGLE)
    mol = mol.GetMol()
    mol.UpdatePropertyCache()
    return mol


def generate_atom_sequences(max_len: int, max_hetero: int, heteroatoms=(7, 8, 16)) -> list:
    """
    Generate all possible unique atom sequences with length from 2 to `max_len`,
    containing up to `max_hetero` certain heteroatoms. Basic atom is carbon.
    If reversed sequence copies another it is eliminated\n
    :param max_len: max number of atoms in sequence
    :param max_hetero: max number of heteroatoms
    :param heteroatoms: tuple of available heteroatoms as atom numbers
    :return: sequences list
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


def generate_spiro_cycles_smiles(chains_1: list, chains_2: list = None) -> list[str]:
    """
    Combine atom chains from 2 lists, creating spirocycles, enumerate stereoisomers and generate
    SMILES strings for them
    :return: SMILES list
    """
    chains_2 = chains_1 if chains_2 is None else chains_2
    spiro_cycles_smiles = []

    for idx_a, chain_a in enumerate(chains_1):
        for idx_b, chain_b in enumerate(chains_2):
            terminal_atoms = (chain_a[0], chain_a[-1], chain_b[0], chain_b[-1])
            if (chains_1 is chains_2 and idx_a < idx_b) or 6 not in terminal_atoms:
                continue
            mol = create_spiro_mol(chain_a, chain_b)
            Chem.FindMolChiralCenters(mol, includeUnassigned=True)
            for isomer in EnumerateStereoisomers(mol):
                smiles = Chem.MolToSmiles(isomer)
                spiro_cycles_smiles.append(smiles)
    return spiro_cycles_smiles
