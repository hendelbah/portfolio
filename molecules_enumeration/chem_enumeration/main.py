from enumeration import generate_spiro_cycles_smiles, generate_atom_sequences
from output_routines import draw_many_mols, make_properties_table, save_images, save_to_excel

if __name__ == '__main__':
    chains = generate_atom_sequences(4, 2)
    smiles_list = generate_spiro_cycles_smiles(chains)
    print(len(smiles_list))
    mol_images = draw_many_mols(smiles_list, 5, 5, (150, 120))
    save_images(mol_images, 'images')

    prop_table = make_properties_table(smiles_list)
    save_to_excel(prop_table, './properties.xlsx')
