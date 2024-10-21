import h5py

def print_h5_structure(h5file, level=0):
    """
    Recursively prints the structure of an HDF5 file, including groups and datasets.
    """
    indent = "  " * level
    for key in h5file.keys():
        item = h5file[key]
        if isinstance(item, h5py.Group):
            print(f"{indent}Group: {key}")
            print_h5_structure(item, level + 1)  # Recursively go through subgroups
        elif isinstance(item, h5py.Dataset):
            print(f"{indent}Dataset: {key}, Shape: {item.shape}, Data type: {item.dtype}")
        else:
            print(f"{indent}Unknown item: {key}")

try:
    with h5py.File(r'C:\Users\bicha\Desktop\Plant-RX-main\Plant-RX-main\Backend\updated_plant_classification_model.h5', 'r') as f:
        print("HDF5 file structure:")
        print_h5_structure(f)
except Exception as e:
    print(f"File error: {e}")
