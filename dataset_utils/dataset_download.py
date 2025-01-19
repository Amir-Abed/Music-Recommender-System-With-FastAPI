import warnings
import os
import subprocess
from zipfile import ZipFile
import sys
warnings.filterwarnings("ignore")


root_data_folder = "./dataset_utils"
file_name = "gtzan-dataset-music-genre-classification.zip"
current_path = os.path.join(root_data_folder, file_name)
root_extraction_path = "./static"
data_extraction_path = os.path.join(root_extraction_path, "dataset")


if not os.path.isfile(current_path):
    try:
        result = subprocess.run(
            ["kaggle", "datasets", "download", "andradaolteanu/gtzan-dataset-music-genre-classification"],
            capture_output=True,
            text=True,
            check=True
        )
        print("dataset downloaded successfully")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stdout}.")
        sys.exit()
    except Exception as e:
        print(f"Error while downloading dataset : {e}.")
else:
    print(f"Skipping : file {current_path} already exists.")

if not os.path.isdir(data_extraction_path):
    try:
        os.mkdir(data_extraction_path)
        print(f"{data_extraction_path} directory successfully created.")
    except Exception as e:
        print(f"Error while creating directoy: {e}.")
else:
    print(f"Skipping : directory {data_extraction_path} already exists.")

print("Extracting...")

if len(os.listdir(data_extraction_path)) == 0:
    with ZipFile(current_path, "r") as zip_file:
        try:
            zip_file.extractall(data_extraction_path)
            print("Extraction completed successfully.")
        except FileNotFoundError as e:
            print(f"zipfile not found : {e}.")
        except Exception as e:
            print(f"Error while extracting file : {e}.")
else:
    print(f"{data_extraction_path} is not empty.")