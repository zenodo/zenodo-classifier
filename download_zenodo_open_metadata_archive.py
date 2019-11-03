import json
import os
import tarfile
import zipfile

import wget

FILENAMES = [
    (375909, "zenodo_open_metadata_06_03_2017.zip"),
    (800494, "zenodo_open_metadata_06_04_2017.zip"),
    (1249354, "zenodo_open_metadata_17_05_2018.tar.gz")
]

for doi, file_ in FILENAMES:
    zip_url = "https://zenodo.org/record/{}/files/{}".format(doi, file_)
    json_data = "{}.json".format(file_.split('.')[0])
    data_dir = "cleaned_datasets"

    # Download data from Zenodo archive
    if not os.path.isfile(os.path.join(data_dir, file_)):
        print("Downloading data.")
        wget.download(zip_url, out=data_dir)
    else:
        print("Data file already found, skipping downloading.\n")

    # Extract the ZIP
    if not os.path.isfile(os.path.join(data_dir, json_data)):
        print("\nExtracting data.")
        if file_.endswith("zip"):
            zip_ref = zipfile.ZipFile(os.path.join(data_dir, file_), 'r')
            zip_ref.extractall(data_dir)
            zip_ref.close()
        elif file_.endswith("tar.gz"):
            tar = tarfile.open(os.path.join(data_dir, file_), "r:gz")
            tar.extractall(data_dir)
            tar.close()
        else:
          print('Unsupported filetype: {}\n'.format(file_))
    else:
        print("File already extracted, skipping extracting.\n")
