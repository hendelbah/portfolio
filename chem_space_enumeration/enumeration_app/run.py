from enumeration import generate_spiro_cycles_smiles, generate_atom_sequences
from output_routines import draw_many_mols, create_properties_table, save_images, save_to_excel

if __name__ == '__main__':
    # enumeration and SMILES generation
    # note: sequence with length of 4 corresponds to 5-membered ring in spirocycle
    sequence_list = generate_atom_sequences(max_len=4, max_hetero=2)
    smiles_list, ring_info = generate_spiro_cycles_smiles(sequence_list)
    print(len(smiles_list))
    # create images of 2D structures from SMILES
    mol_images = draw_many_mols(smiles_list, mols_per_col=5, mols_per_row=5, img_size=(150, 120))
    save_images(mol_images, directory='images')
    # calculate properties and create DataFrame table
    prop_table = create_properties_table(smiles_list, ring_info)
    save_to_excel(prop_table, './properties.xlsx')
