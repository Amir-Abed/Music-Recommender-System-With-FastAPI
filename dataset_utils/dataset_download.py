import warnings
import os
import shutil
import kaggle
import subprocess
from zipfile import ZipFile
import sys
warnings.filterwarnings("ignore")

root_data_folder = "./data"
current_path = "gtzan-dataset-music-genre-classification.zip" 
destination_path = os.path.join(root_data_folder, "gtzan_dataset.zip")
data_path = os.path.join(root_data_folder, "Data")
print(os.path.isfile(destination_path))

if not os.path.isfile(current_path) and not os.path.isfile(destination_path):
    try:
        result = subprocess.run(
            ["kaggle", "datasets", "download", "andradaolteanu/gtzan-dataset-music-genre-classification"],
            capture_output=True,
            text=True,
            check=True
        )
        print("dataset downloaded successfully")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stdout}")
        sys.exit()
    except Exception as e:
        print(f"Error while downloading dataset : {e}")
else:
    print(f"Skipping : file {current_path} or {destination_path} already exists")

if not os.path.isdir(root_data_folder):
    try:
        os.mkdir(root_data_folder)
        print("root directory successfully created")
    except Exception as e:
        print("Error while creating directoy: {e}")
else:
    print(f"Skipping : directory {root_data_folder} already exists")
    
if not os.path.isfile(destination_path):
    try:
        shutil.move(current_path, destination_path)
        print(f"file successfully moved to {destination_path}")
    except Exception as e:
        print(f"there was an error while moving the file : {e}")
else:
    print(f"Skipping : file {destination_path} already exists")

print("Please wait...")

if len(os.listdir(root_data_folder)) == 0 or os.path.isfile(destination_path) and not os.path.isdir(data_path):
    with ZipFile(destination_path, "r") as zip_file:
        try:
            zip_file.extractall(root_data_folder)
        except FileNotFoundError as e:
            print(f"zipfile not found : {e}")
        except Exception as e:
            print(f"Error while extracting file : {e}")
else:
    print(f"{root_data_folder} is not empty")
