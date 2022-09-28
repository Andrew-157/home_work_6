import os
import shutil
from pathlib import Path
from sys import argv
from locale import normalize


def sort_images(dir_address, name, splitted_name, new_name):
    # function for moving images to a directory "images"
    original = f'{dir_address}\\{name}'
    move_to = f'{dir_address}\\images'
    shutil.move(original, move_to)
    os.rename(f'{dir_address}\\images\\{name}',
              f'{dir_address}\\images\\{new_name}.{splitted_name[-1]}')


def sort_video(dir_address, name, splitted_name, new_name):
    # function for moving video to a directory "video"
    original = f'{dir_address}\\{name}'
    move_to = f'{dir_address}\\video'
    shutil.move(original, move_to)
    os.rename(f'{dir_address}\\video\\{name}',
              f'{dir_address}\\video\\{new_name}.{splitted_name[-1]}')


def sort_documents(dir_address, name, splitted_name, new_name):
    # function for moving documents to a directory "documents"
    original = f'{dir_address}\\{name}'
    move_to = f'{dir_address}\\documents'
    shutil.move(original, move_to)
    os.rename(f'{dir_address}\\documents\\{name}',
              f'{dir_address}\\documents\\{new_name}.{splitted_name[-1]}')


def sort_audio(dir_address, name, splitted_name, new_name):
    # function for moving audio to a directory "audio"
    original = f'{dir_address}\\{name}'
    move_to = f'{dir_address}\\audio'
    shutil.move(original, move_to)
    os.rename(f'{dir_address}\\audio\\{name}',
              f'{dir_address}\\audio\\{new_name}.{splitted_name[-1]}')


def sort_archive(dir_address, name, new_name):
    # function for unpacking an archive in a subfolder
    shutil.unpack_archive(
        f'{dir_address}\\{name}', f'{dir_address}\\archive\\{new_name}')
    os.remove(f'{dir_address}\\{name}')


def sort_files(name):
    # lists that the function will return
    extensions = []
    names_of_files_audio = []
    names_of_files_images = []
    names_of_files_documents = []
    names_of_archives = []
    names_of_files_audio = []
    names_of_files_video = []
    names_of_files_unknown = []
    unknown_extensions = []

    # creating directories for sorting
    directories = ["images", "video", "documents", "archive", "audio"]
    for dir in directories:
        path = os.path.join(name, dir)
        os.mkdir(path)
    dir_address = Path(name)
    for file in dir_address.iterdir():
        if file.name in directories:
            # ignoring directories for sorting
            continue
        else:
            if file.is_dir():

                dir = os.listdir(file)
                if len(dir) == 0:
                    os.rmdir(f'{dir_address}\\{file.name}')

                else:
                    sort_files(f'{dir_address}\\{file.name}')

            elif file.name.endswith(('.jpeg', '.png', '.jpg', '.svg')):

                splitted_name = file.name.split(".")
                new_name = normalize(
                    file.name.replace(f'.{splitted_name[-1]}', ""))
                sort_images(dir_address, file.name, splitted_name, new_name)

                extensions.append(splitted_name[-1])
                names_of_files_images.append(new_name)

            elif file.name.endswith(('.avi', '.mp4', '.mov', '.mkv')):

                splitted_name = file.name.split(".")
                new_name = normalize(
                    file.name.replace(f'.{splitted_name[-1]}', ""))
                sort_video(dir_address, file.name, splitted_name, new_name)

                extensions.append(splitted_name[-1])
                names_of_files_video.append(new_name)

            elif file.name.endswith(('.doc', '.docx', '.txt', '.pdf', '.xlsx', '.pptx')):

                splitted_name = file.name.split(".")
                new_name = normalize(
                    file.name.replace(f'.{splitted_name[-1]}', ""))
                sort_documents(dir_address, file.name, splitted_name, new_name)

                extensions.append(splitted_name[-1])
                names_of_files_documents.append(new_name)

            elif file.name.endswith(('.mp3', '.ogg', '.wav', '.amr')):

                splitted_name = file.name.split(".")
                new_name = normalize(
                    file.name.replace(f'.{splitted_name[-1]}', ""))
                sort_audio(dir_address, file.name, splitted_name, new_name)

                extensions.append(splitted_name[-1])
                names_of_files_audio.append(new_name)

            elif file.name.endswith(('.zip', 'gz', '.tar')):

                splitted_name = file.name.split(".")
                new_name = normalize(
                    file.name.replace(f'.{splitted_name[-1]}', ""))
                sort_archive(dir_address, file.name, new_name)
                sort_files(f'{dir_address}\\archive\\{new_name}\\archive')

                names_of_archives.append(new_name)
                extensions.append(splitted_name[-1])

            else:

                splitted_name = file.name.split(".")
                unknown_extensions.append(splitted_name[-1])
                names_of_files_unknown.append(file.name)
                continue

    return f"Images: {names_of_files_images}\nVideo: {names_of_files_video}\nDocuments: {names_of_files_documents}\nAudio: {names_of_files_audio}\
        \nArchive: {names_of_archives}\nUnknown files: {names_of_files_unknown}\nExtensions: {extensions}\nUnknown extensions: {unknown_extensions}"


print(sort_files(argv[0]))
