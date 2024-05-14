import os
import re
from shutil import move
import shutil


def process_filename(filename):
    match = re.search(r'\d{3}', filename)
    if match:
        return match.group()
    else:
        return None


# This function removes leading zeros from a number
def remove_leading_zeros(number):
    try:
        result = str(int(number))
        return result
    except ValueError:
        return None


# this function will loop into ClothingFemale and Retrieve all item Names necessaries . CHANGE ONLY THE PATH
def test():
    clothingPackFemaleStreamFolderPath = "C:\\Users\\Administrator\\Desktop\\ToXxXika\\clothingpackfemale\\stream"
    accessories = {}
    for file in os.listdir(clothingPackFemaleStreamFolderPath):
        regex = re.search(r'\^([^_]+)_\d+', file)
        if regex:
            accessories[regex.group(1)] = regex.group(1)

    
    return accessories


# This function extracts the items from the model folder
def extract_items(model_path):
    accessories = test()

    # Create folders for each accessory
    for accessory_key, accessory_folder in accessories.items():
        accessory_folder_path = os.path.join(model_path, accessory_folder)
        if not os.path.exists(accessory_folder_path):
            os.makedirs(accessory_folder_path)

    # Move files to their corresponding folders
    for file in os.listdir(model_path):
        for key, accessory_folder in accessories.items():
            if f'^{key}' in file:
                shutil.copy(os.path.join(model_path, file), os.path.join(model_path, accessory_folder))


def count_folders(directory_path):
    items = os.listdir(directory_path)
    folders = [item for item in items if os.path.isdir(os.path.join(directory_path, item))]
    return len(folders)


def create_folder(directory_path, folder_name):
    new_model_folder = os.path.join(directory_path, folder_name)
    if not os.path.exists(new_model_folder):
        os.makedirs(new_model_folder)
    else:
        print(f"Folder '{folder_name}' already exists")


def OrganizeClothingInTheServerDirectory(directory_path, model_path):
    extract_items(model_path)
    new_folder_path = os.path.join(directory_path, "organized_files")
    create_folder(directory_path, "organized_files")
    for file in os.listdir(model_path):
        for folder in os.listdir(directory_path):
            if os.path.isdir(os.path.join(directory_path, folder)):
                if file in folder:
                    # print(file)
                    folder_path = os.path.join(directory_path, folder)
                    folder_count = count_folders(folder_path)
                    files_by_digits = {}
                    model_accessories_path = os.path.join(model_path, file)
                    for folder_file_name in os.listdir(model_accessories_path):
                        folder_file_path = os.path.join(model_accessories_path, folder_file_name)
                        # print(folder_file_path)
                        if os.path.isfile(folder_file_path):
                            match = re.search(r'\d{3}', folder_file_name)

                            if match:
                                original_digits = match.group()
                                new_digits = f"{folder_count + int(original_digits) :03d}"
                                if original_digits.__eq__("000"):
                                    new_digits = f"{folder_count + 1 :03d}"

                                new_file_name = folder_file_name.replace(original_digits, new_digits)
                                new_file_path = os.path.join(new_folder_path, new_file_name)
                                shutil.copy(folder_file_path, new_file_path)
                                if original_digits in files_by_digits:
                                    files_by_digits[original_digits].append(new_file_path)
                                else:
                                    files_by_digits[original_digits] = [new_file_path]
                            else:
                                print(file + " No Match")
                        else:
                            print("Not a file")


def FolderAttributionByTypeInOrgranizedFiles(organized_path):
    accessories = test()

    # Create folders for each accessory
    for accessory_key, accessory_folder in accessories.items():
        accessory_folder_path = os.path.join(organized_path, accessory_folder)
        if not os.path.exists(accessory_folder_path):
            os.makedirs(accessory_folder_path)

    # Move files to their corresponding folders
    for file in os.listdir(organized_path):
        for key, accessory_folder in accessories.items():
            if f'^{key}' in file:
                shutil.move(os.path.join(organized_path, file), os.path.join(organized_path, accessory_folder))


def SortingFilesInCorrespondingFolderByNamesAndTypes(organized_path):
    for folder in os.listdir(organized_path):
        folder_path = os.path.join(organized_path, folder)
        file_tables = {}
        for file_name in os.listdir(folder_path):
            match = re.search(r'^([^-^]+)', file_name)
            if match:
                base_filename = match.group(1)
                if base_filename not in file_tables:
                    file_tables[base_filename] = []

                file_tables[base_filename].append(file_name)
        for base_filename, files in file_tables.items():
            base_folder_path = os.path.join(folder_path, base_filename)
            if not os.path.exists(base_folder_path):
                os.makedirs(base_folder_path)
                print(f"Folder '{base_folder_path}' created")

          
            for file in files:
                print(f"File: {file}")
                source_file_path = os.path.join(folder_path, file)
                destination_file_path = os.path.join(base_folder_path, file)
                if not os.path.exists(destination_file_path):
                    print(f"Moving file {file} to {base_folder_path}")
                    move(source_file_path, destination_file_path)
                else:
                    print(f"File {file} already exists in {base_folder_path}")

            


def delete_unecessarry_folders(organized_path):
    for folder in os.listdir(organized_path):
        folder_path = os.path.join(organized_path, folder)
        for subfolder in os.listdir(folder_path):
            if subfolder != "mp_f_freemode_01":
                try:
                    shutil.rmtree(os.path.join(folder_path, subfolder))
                except OSError as e:
                    print("Error: %s : %s" % (folder_path, e.strerror))


def clothesDistributionperAccs(organized_path, directory_path):
    folders = {}
    sv_directories = [item for item in os.listdir(directory_path) if os.path.isdir(os.path.join(directory_path, item))]
    for folder in os.listdir(organized_path):
        folder_path = os.path.join(organized_path, folder)
        for subfolder in os.listdir(folder_path):
            subfolder_path = os.path.join(folder_path, subfolder)
            for file in os.listdir(subfolder_path):
                number = process_filename(file)
                if number is not None:
                    x = re.search(r'\^([^_]+)_', file)
                    for item in sv_directories:
                        if x.group(1) in item:
                            variable = item
                            addon_folder = os.path.join(directory_path, item)
                            destination_folder = os.path.join(addon_folder, remove_leading_zeros(number))

                            # Check if the destination folder exists
                            if os.path.exists(destination_folder):
                                print(f"Folder '{destination_folder}' already exists")
                            else:
                                os.makedirs(destination_folder)
                                folders[number] = destination_folder

                            destination_file = os.path.join(destination_folder, file)
                            source_file = os.path.join(os.path.join(folder_path, subfolder), file)

                            if not os.path.exists(destination_file):
                                print(f"Copying file: {file} to {destination_folder}")
                                shutil.copy(source_file, destination_file)
                            else:
                                print(f"File {file} already exists in folder {destination_folder}")


def updateFilesNumber(directory_path, subfolder, variable):
    files_by_digits = {}
    SF = os.path.join(directory_path, subfolder)
    for file in os.listdir(SF):
        filepath = os.path.join(SF, file)
        if os.path.isfile(filepath):
            match = re.search(r'\d{3}', file)

            if match:
                countfolder = count_folders(variable)
                original_digits = match.group()
                new_digits = f"{countfolder + 1:03d}"
                if original_digits.__eq__("000"):
                    new_digits = f"{countfolder + 1:03d}"

                new_file_name = file.replace(original_digits, new_digits)
                new_file_path = os.path.join(SF, new_file_name)
                shutil.move(filepath, new_file_path)
                if original_digits in files_by_digits:
                    files_by_digits[original_digits].append(new_file_path)
                else:
                    files_by_digits[original_digits] = [new_file_path]
            else:
                print(file + " No Match")


def distributeClothes(directory_path, organized_path):
    folders = {}
    sv_directories = [item for item in os.listdir(directory_path) if os.path.isdir(os.path.join(directory_path, item))]

    for file_name in os.listdir(organized_path):
        number = process_filename(file_name)
        if number is not None:
            x = re.search(r'\^([^_]+)_', file_name)

            for item in sv_directories:
                if x.group(1) in item:
                    addon_folder = os.path.join(directory_path, item)
                    destination_folder = os.path.join(addon_folder, remove_leading_zeros(number))

                    # Check if the destination folder exists
                    if os.path.exists(destination_folder):
                        print(f"Folder '{destination_folder}' already exists")
                    else:
                        os.makedirs(destination_folder)
                        folders[number] = destination_folder

                    destination_file = os.path.join(destination_folder, file_name)
                    source_file = os.path.join(organized_path, file_name)

                    if not os.path.exists(destination_file):
                        move(source_file, destination_file)
                    else:
                        print(f"File {file_name} already exists in folder {destination_folder}")

#Server Directory Path
directory_path = 'C:\\Users\\Administrator\\Desktop\\New Limitless\\Server Data\\resources\\[clothes]\\azurapackv2\\stream'
# change only C:\\Users\\Administrator\\Desktop\\ToXxXika\\
organized_path = 'C:\\Users\\Administrator\\Desktop\\New Limitless\\Server Data\\resources\\[clothes]\\azurapackv2\\stream\\organized_files'
models_path = 'C:\\Users\\Administrator\\Desktop\\New Limitless\\Server Data\\resources\\[later]\\clothingpackfemale\\stream'
OrganizeClothingInTheServerDirectory(directory_path, models_path)
FolderAttributionByTypeInOrgranizedFiles(organized_path)
SortingFilesInCorrespondingFolderByNamesAndTypes(organized_path)
delete_unecessarry_folders(organized_path)
clothesDistributionperAccs(organized_path, directory_path)
