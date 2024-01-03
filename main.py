# Import libraries
import os
import shutil
import random
from kaggle.api.kaggle_api_extended import KaggleApi

# Paths
KAGGLE_DATASET = 'charuchaudhry/plantvillage-tomato-leaf-dataset'

MAIN_PATH = os.path.abspath(os.path.join(os.getcwd(), '..', 'data'))
RAW_PATH = os.path.join(MAIN_PATH, 'raw_data', '')
TEST_PATH = os.path.join(MAIN_PATH, 'test_split', '')
TRAIN_PATH = os.path.join(MAIN_PATH, 'train_split', '')
PLANTVILLAGE = os.path.join(MAIN_PATH, 'plantvillage', '')

# Create Data folder structure
if not os.path.exists(MAIN_PATH):
    os.makedirs(MAIN_PATH, exist_ok=True)

    for path in [RAW_PATH, TRAIN_PATH, TEST_PATH]:
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)

    # Instantiate Kaggle API (requires local API Key)
    print('Authenticating...', end=' ')
    api = KaggleApi()
    api.authenticate()

    # Download the dataset to the local folder and unzip
    print('Downloading...', end=' ')
    api.dataset_download_files(KAGGLE_DATASET, path=MAIN_PATH, unzip=True)

    print('Unzipping...', end=' ')
    for folder in os.listdir(PLANTVILLAGE):
        if folder == 'Tomato___healthy' or folder == 'Tomato___Early_blight' or folder == 'Tomato___Late_blight':
            source_path = os.path.join(PLANTVILLAGE, folder)

            # Rename folder
            new_folder = folder.replace('Tomato___', '').lower()
            new_path = os.path.join(PLANTVILLAGE, new_folder)
            os.rename(source_path, new_path)

            # Move the subfolder to the destination folder
            shutil.move(new_path, RAW_PATH)

    shutil.rmtree(PLANTVILLAGE)

    # Define split ratio of 80% train and 20% test
    print('Splitting...')
    split_ratio = 0.8

    for class_folder in os.listdir(RAW_PATH):
        class_path = os.path.join(RAW_PATH, class_folder)
        if os.path.isdir(class_path):
            files = os.listdir(class_path)
            random.shuffle(files)

            # Separating raw data into train and test splits
            split_index = int(len(files) * split_ratio)
            train_files = files[:split_index]
            test_files = files[split_index:]

            # Creating folders for each class of the train split
            dest_train_folder = os.path.join(TRAIN_PATH, class_folder)
            if not os.path.exists(dest_train_folder):
                os.makedirs(dest_train_folder, exist_ok=True)
            else:
                continue

            # Creating folders for each class of the test split
            dest_test_folder = os.path.join(TEST_PATH, class_folder)
            if not os.path.exists(dest_test_folder):
                os.makedirs(dest_test_folder, exist_ok=True)
            else:
                continue

            # Move train split files to train folder
            for file in train_files:
                source_file = os.path.join(class_path, file)
                dest_file = os.path.join(dest_train_folder, file)
                shutil.copy(source_file, dest_file)

            # Move test split files to test folder
            for file in test_files:
                source_file = os.path.join(class_path, file)
                dest_file = os.path.join(dest_test_folder, file)
                shutil.copy(source_file, dest_file)
    print('✅ Dataset successfully downloaded!')
else:
    print('✅ Dataset already downloaded!')
