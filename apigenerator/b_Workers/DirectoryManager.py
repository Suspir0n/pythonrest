# System Imports #
import sys
import os
import shutil
from apigenerator.e_Enumerables.Enumerables import *


# Check if script is running directly or via exe file to get the path
def define_script_path_based_on_run_context():
    # Get the absolute path of the current script
    script_path = os.path.abspath(sys.argv[0])

    # Check if the script is running as an executable
    if getattr(sys, 'frozen', False):
        # If it's an executable, use the '_MEIPASS' attribute
        script_absolute_path = getattr(sys, '_MEIPASS', os.path.dirname(script_path))
    else:
        # If it's a script, use the directory of the script
        script_absolute_path = os.path.dirname(script_path)
    return script_absolute_path


# Method removes all files under a certain directory #
def clean_directory(directory):
    # Iterating over working tree #
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        # Removing files #
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


# Copy base 'Project' directory to result hierarchy #
def copy_proj_base_dir(result_full_path, symlinks=False, ignore=None):
    directories = get_directory_data()
    script_absolute_path = define_script_path_based_on_run_context()
    src = os.path.join(script_absolute_path, directories['base_proj_path'])
    # Iterating over working tree #
    for item in os.listdir(src):
        src_folder = os.path.join(src, item)
        dst_folder = os.path.join(result_full_path, item)
        if os.path.isdir(src_folder):
            shutil.copytree(src_folder, dst_folder, symlinks, ignore)
        else:
            shutil.copy2(src_folder, dst_folder)


# Method copies domain files into proper folder of result hierarchy #
def copy_domain_files(result_full_path, generated_domains_path, symlinks=False, ignore=None):
    # Accessing domain folder #
    proj_domain_folder = os.path.join(result_full_path, 'src\\c_Domain')
    # Iterating over domain directory #
    for item in os.listdir(generated_domains_path):
        src_folder = os.path.join(generated_domains_path, item)
        dst_folder = os.path.join(proj_domain_folder, item)
        # Copying files #
        if os.path.isdir(src_folder):
            shutil.copytree(src_folder, dst_folder, symlinks, ignore)
        else:
            shutil.copy2(src_folder, dst_folder)

    shutil.rmtree(generated_domains_path)


# Method copies database connection files into proper folder of result hierarchy #
def copy_database_files(db_resources_folder, resources_folder, symlinks=False, ignore=None):
    # Iterating over proper directory #
    for item in os.listdir(db_resources_folder):
        s = os.path.join(db_resources_folder, item)
        d = os.path.join(resources_folder, item)
        # Asssembling files into destination folder #
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore, dirs_exist_ok=True)
        else:
            shutil.copy2(s, d)


def copytree(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)


def mergefolders(root_src_dir, root_dst_dir):
    for src_dir, dirs, files in os.walk(root_src_dir):
        dst_dir = src_dir.replace(root_src_dir, root_dst_dir, 1)
        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir)
        for file_ in files:
            src_file = os.path.join(src_dir, file_)
            dst_file = os.path.join(dst_dir, file_)
            if os.path.exists(dst_file):
                os.remove(dst_file)
            shutil.copy(src_file, dst_dir)


def get_list_of_directories_in_directory(path):
    return os.listdir(path)


def get_domain_files_list(domain_path):
    domain_files_list = [f for f in os.listdir(domain_path)
                         if os.path.isfile(os.path.join(domain_path, f)) and f != '__init__.py']
    return domain_files_list


def append_database_library_to_requirements_file(file_path, new_dependency):
    try:
        # Read the content of the existing requirements.txt file
        with open(file_path, 'r') as file:
            lines = file.readlines()

        # Check if the last line is not empty and does not end with a newline
        if lines and lines[-1].strip() != '':
            # Add a newline if the last line is not empty
            lines.append('\n')

        # Append the new dependency to the list
        lines.append(new_dependency + '\n')

        # Write the updated content back to the requirements.txt file
        with open(file_path, 'w') as file:
            file.writelines(lines)

    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")