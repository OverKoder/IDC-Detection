# Gathers all images and creates 'train' and 'test' folders separating samples by class
# The zip file must be given as a parameter
# setup.py and the image folder must be in the same directory
import os
import zipfile as zf
from tqdm import tqdm
import shutil
import random
import math

os.chdir("/home/cristobal/Escritorio")

# Create the necesary folders.
# If "data" directory already exists, it is overwritten
data_folder = "./prueba/"
os.makedirs(data_folder,exist_ok=True)
os.makedirs(data_folder + "tmp/",exist_ok=True)
os.chdir(data_folder + "tmp/")
print("Created data folder")
print("Preparing to extract...")
# Extract files from zip file
with zf.ZipFile('../../archive.zip','r') as arc:
    for member in tqdm(arc.infolist(),desc='Extracting...'):
        try:
            arc.extract(member,'.')
        except:
            pass


os.chdir("../..")
# Train samples
os.makedirs(data_folder + "train/",exist_ok=True)  
# Test samples
os.makedirs(data_folder + "test/",exist_ok=True)  

# Separate train samples by class
train_benign_path = data_folder + "train/benign"
train_malignant_path = data_folder + "train/malignant"
os.makedirs(train_benign_path ,exist_ok=True)  
os.makedirs(train_malignant_path,exist_ok=True)   

# Separate test samples by class
test_benign_path = data_folder + "test/benign"
test_malignant_path = data_folder + "test/malignant"
os.makedirs(test_benign_path,exist_ok=True)  
os.makedirs(test_malignant_path,exist_ok=True)   

img_dir = data_folder + "tmp/"

# There is a folder named 'IDC_regular_ps50_idx5' in the zip file
# However it is not necesary, so we just remove it
for i in tqdm(os.listdir(img_dir + 'IDC_regular_ps50_idx5/'),desc = 'Removing unnecesary files...'):
    shutil.rmtree(img_dir + 'IDC_regular_ps50_idx5/' + i)

# Once files have been removed, we delete the directory   
os.rmdir(img_dir + 'IDC_regular_ps50_idx5/')

dirs = os.listdir(img_dir)   
train_data_benign_list = []
# The dataset has imbalaced data. In this case we fix this issue 
# by under-sampling (removing benign samples)
for fold in tqdm(dirs, desc= 'Collecting files...'):

   # Class 0 samples
    for img in os.listdir(img_dir + str(fold) + "/0/" ):
        train_data_benign_list.append(img)

    # Class 1 samples are moved directly
    for img in os.listdir(img_dir + str(fold) + "/1/" ):
        shutil.move(img_dir + str(fold) + "/1/" + img , train_malignant_path)

# Benign train samples are randomly selected
random.shuffle(train_data_benign_list) 
train_data_benign_list = train_data_benign_list [:78786]

# A dictionary is built with the train samples as keys for efficiency
train_data_benign = {}.fromkeys(train_data_benign_list)

for fold in tqdm(dirs, desc= 'Moving files...'):

    for img in os.listdir(img_dir + str(fold) + "/0/" ):

        try:
            train_data_benign[img]
            shutil.move(img_dir + str(fold) + "/0/" + img , train_benign_path)
            del train_data_benign[img]
        except:
            os.remove(img_dir + str(fold) + "/0/" + img)

# Generation of test samples is done randomly            
test_data_benign = os.listdir(train_benign_path)
random.shuffle(test_data_benign) 
test_data_benign = test_data_benign [ : math.floor(0.1 * len(test_data_benign)) ]

name = 1
for test_sample in tqdm(test_data_benign, desc= 'Generating test samples (benign)...'):
    shutil.move(train_benign_path + '/' + str(test_sample), test_benign_path)
    os.rename(test_benign_path + '/' + str(test_sample), test_benign_path + '/test_' + str(name) + '_class0.png' )
    name +=1

del train_data_benign
del test_data_benign

# Generation of test samples is done randomly   
test_data_malignant = os.listdir(train_malignant_path)
random.shuffle(test_data_malignant) 
test_data_malignant = test_data_malignant [ : math.floor(0.1 * len(test_data_malignant)) ]
name = 1

for test_sample in tqdm(test_data_malignant, desc= 'Generating test samples (malignant)...'):
    shutil.move(train_malignant_path + '/' + str(test_sample), test_malignant_path)
    os.rename(test_malignant_path + '/' + str(test_sample), test_malignant_path + '/test_' + str(name) + '_class1.png' )
    name += 1

# Temporary folder is deleted 
shutil.rmtree(data_folder + 'tmp/')

name = 1
for train_sample in tqdm(os.listdir(train_benign_path), desc = 'Renaming benign files...'):
    os.rename(train_benign_path + '/' + str(train_sample), train_benign_path +  '/train_'  + str(name) + '_class0.png')
    name += 1

name = 1
for train_sample in tqdm(os.listdir(train_malignant_path), desc = 'Renaming malignant files...'):
    os.rename(train_malignant_path + '/' + str(train_sample), train_malignant_path + '/train_' + str(name) + '_class1.png')
    name += 1


print("train/benign now has", len(os.listdir(train_benign_path)), "images")
print("train/malignant now has", len(os.listdir(train_malignant_path)), "images")  
print("test/benign now has", len(os.listdir(test_benign_path)), "images")
print("test/malignant now has", len(os.listdir(test_malignant_path)), "images")  
print("Everything done!")


