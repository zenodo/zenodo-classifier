import json
import wget
import os
import zipfile


zip_url = "https://zenodo.org/record/800494/files/zenodo_open_metadata_06_04_2017.zip"
zipped_data = "zenodo_open_metadata_06_04_2017.zip"
json_data = "zenodo_open_metadata_06_04_2017.json"
clean_json_data = "zenodo_open_metadata_06_04_2017_cleaned_20_08_17.json"
data_dir = 'data'

if not os.path.exists(data_dir):
    os.mkdir(data_dir)
if os.path.isfile(data_dir):
    raise Exception("Directory '{0}' needs to be created (file found instead)"
                    .format(data_dir))
if not os.path.isfile(os.path.join(data_dir, zipped_data)):
    print("Downloading data.")
    wget.download(zip_url, out=data_dir)
else:
    print("Data file already found, skipping downloading.")

# Extract the ZIP
if not os.path.isfile(os.path.join(data_dir, json_data)):
    print("Extracting data.")
    zip_ref = zipfile.ZipFile(os.path.join(data_dir, zipped_data), 'r')
    zip_ref.extractall(data_dir)
    zip_ref.close()
else:
    print("File already extracted, skipping extracting.")

if not os.path.isfile(os.path.join(data_dir, clean_json_data)):

    with open(os.path.join(data_dir, json_data), "r") as fp:
        data = json.load(fp)
    spams = [33787, 166754, 32807, 17229, 400865, 19031, 285825, 440002, 292995, 221828, 18818, 160518, 32519, 437895, 22211, 290571, 438157, 44942, 33550, 246800, 51728, 398866, 400531, 60051, 50704, 32918, 164886, 164888, 495001, 165784, 34331, 321818, 60828, 346531, 399268, 18045, 27942, 35364, 30632, 202291, 47155, 293045, 47286, 290359, 224947, 29113, 375738, 20539, 17596, 293053, 439998, 439997, 290237, 49089, 440001, 440003, 440004, 440005, 440006, 440007, 154696, 440009, 440008, 290123, 35276, 284358, 398797, 32076, 33365, 249942, 290134, 344537, 166752, 291812, 18281, 46445, 51054, 290685, 34287, 28271, 439999, 32439, 232944, 47174, 290157, 23155, 290166, 440000, 249981]
    maybe_spams = [153959, ]
    # maybe_spams2 = [12846, 13138, 13385, 398764, 400012]
    for d in data:
        if d['recid'] in (spams + maybe_spams):
            d['spam'] = True
    print("Writing cleaned data.")
    with open(os.path.join(data_dir, clean_json_data), "w") as fp:
        data = json.dump(data, fp)
else:
    print("Cleaned data present, skipping.")
