import os
import re
from shutil import move
import shutil


def count_folders(directory_path):
    items = os.listdir(directory_path)
    folders = [item for item in items if os.path.isdir(os.path.join(directory_path, item))]
    return len(folders)


def create_folder(directory_path, folder_name):
    new_model_folder = os.path.join(directory_path, folder_name)
    if not os.path.exists(new_model_folder):
        os.makedirs(new_model_folder)
        print(f"Folder '{folder_name}' created")
    else:
        print(f"Folder '{folder_name}' already exists")


def organize_files(directory_path, model_path):
    folder_count = count_folders(directory_path)

    files_by_digits = {}

    for file_name in os.listdir(model_path):
        file_path = os.path.join(model_path, file_name)

        if os.path.isfile(file_path):
            match = re.search(r'\d{3}', file_name)

            if match:
                original_digits = match.group()
                print(original_digits)

                new_digits = f"{folder_count + int(original_digits) - 1:03d}"

                new_folder_path = os.path.join(directory_path, "organized_files")

                create_folder(directory_path, "organized_files")

                new_file_name = file_name.replace(original_digits, new_digits)
                new_file_path = os.path.join(new_folder_path, new_file_name)

                shutil.copy(file_path, new_file_path)

                if original_digits in files_by_digits:
                    files_by_digits[original_digits].append(new_file_path)
                else:
                    files_by_digits[original_digits] = [new_file_path]

    print(files_by_digits)
    #    print('Files organized successfully.')

    print("Files grouped by digits:")
    for digits, filenames in files_by_digits.items():
        print(f"{digits}: {filenames}")


def process_filename(filename):
    match = re.search(r'\d{3}', filename)
    if match:
        return match.group()
    else:
        return None


def remove_leading_zeros(number):
    try:
        result = str(int(number))
        return result
    except ValueError:
        return None


def distribute_files(organized_path,directory_path):
    folders = {}
    for file_name in os.listdir(organized_path):
        number = process_filename(file_name)

        if number is not None:
            if number in folders:
                print(number)
                destination_folder = folders[number]
            else:

                destination_folder = os.path.join(directory_path, remove_leading_zeros(number))
                os.makedirs(destination_folder)
                folders[number] = destination_folder

            source_path = os.path.join(organized_path, file_name)
            destination_path = os.path.join(destination_folder, file_name)

            if not os.path.exists(destination_path):
                move(source_path, destination_path)
            else:
                print(f"File '{file_name}' already exists in folder '{destination_folder}'")


# Example usage
directory_path = 'C:\\Users\\Administrator\\PycharmProjects\\pythonProject\\AudioToTextTranscription\\files\\sv_folders'
organized_path = 'C:\\Users\\Administrator\\PycharmProjects\\pythonProject\\AudioToTextTranscription\\files\\sv_folders\\organized_files'
models_path = 'C:\\Users\\Administrator\\PycharmProjects\\pythonProject\\AudioToTextTranscription\\files\\new_models'
organize_files(directory_path, models_path)
distribute_files(organized_path,directory_path)
