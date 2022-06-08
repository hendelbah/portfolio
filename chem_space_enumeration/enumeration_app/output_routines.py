from pathlib import Path

import pandas as pd
from rdkit import Chem
from rdkit.Chem import MolFromSmiles, Descriptors
from rdkit.Chem.Draw import MolsToGridImage


def chunks(seq, size):
    """
    Split sequence into chunks of given size? return generator
    """
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))


def draw_many_mols(smiles_list, mols_per_col=4, mols_per_row=6, img_size=(200, 200)):
    """
    Draw 2D images of molecules from SMILES list on grid.
    :param smiles_list: list of molecular SMILES
    :param mols_per_col: height of grid
    :param mols_per_row: width of grid
    :param img_size: size tuple of single molecule
    :return: list of images
    """
    images = []
    for smiles_batch in chunks(smiles_list, mols_per_col * mols_per_row):
        mols = [MolFromSmiles(smiles) for smiles in smiles_batch]
        img = MolsToGridImage(mols, mols_per_row, img_size, smiles_batch)
        images.append(img)
    return images


def save_images(images: list, directory: str):
    """
    Save list of images in given directory, clearing all existing images before.
    """
    [f.unlink() for f in Path(directory).glob("*") if f.is_file() and f.suffix == '.png']
    directory = Path(directory)
    for index, image in enumerate(images):
        image.save(directory / f'molecules-{index:0>3}.png')


def create_properties_table(smiles_list, ring_sizes) -> pd.DataFrame:
    """
    Calculate properties (logP, MolWeight) for molecules in smiles list and create
    DataFrame with this data.
    :param smiles_list: molecular SMILES list
    :param ring_sizes: list of ring size pairs for each mol
    :return:
    """
    df = pd.DataFrame(index=range(1, len(smiles_list) + 1),
                      columns=['SMILES', 'cycles size', 'logP', 'Mr'])
    df.index.names = ['id']
    for i, smiles in enumerate(smiles_list, 1):
        mol = Chem.MolFromSmiles(smiles)
        df['SMILES'][i] = smiles
        df['cycles size'][i] = f'{ring_sizes[i - 1][0]}/{ring_sizes[i - 1][1]}'
        df['logP'][i] = Descriptors.MolLogP(mol)
        df['Mr'][i] = Descriptors.ExactMolWt(mol)
    return df


def save_to_excel(dataframe, file_path):
    """
    Save dataframe to exel file.
    """
    with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
        dataframe.to_excel(writer)
