# -*- coding: utf-8 -*-
"""Cloning_Repo_Threading.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1yJUrb6TIfHc6oTNycJJAt-yxt-0M_0te
"""

# Install the necessary libraries
!pip install GitPython

# Connect to Google drive
from google.colab import drive
drive.mount('/content/gdrive')

# Import the necessary libraries
import requests
import threading
from git import Repo
import pandas as pd

# Read repositories metadata extracted from SEART GitHub search tool
path = '' #@param { type: "string" }
repo_metadata = pd.read_excel(path)

counter = 0
clone_progress = pd.DataFrame(columns=['id', 'name', 'url', 'clone result'])

print(repo_metadata.shape[0])

# Create the helper functions - The cloning process
def clone_ssh(ssh, dir):
    try:
        Repo.clone_from(ssh, dir)
        return True
    except Exception as e:
        print(f"An exception occurred: {str(e)}")
        return False

# Multithreading medhod
def clone_all_ssh_multithreading(repo):
    contents = pd.DataFrame(columns=['id', 'name', 'url','ssh', 'clone result', 'path'])
    threads = []

    # Define a function to download the contents of a URL in a thread
    def download_thread(ssh, dir, id, name, url,indx):
      if clone_ssh(ssh, dir):
        result = True
      else:
        result = False
      clone_result = [id, name, url, ssh, result, dir]
      contents.loc[len(contents)] = clone_result
      print(f"Index: {indx} - Result: {result}")

    # Create a thread for each URL and start it
    for index in repo.index:
      ssh = repo['SSH'][index]
      project_name = repo['Project name'][index]
      dir = repo_dir + project_name
      name = repo['name'][index]
      id = repo['id'][index]
      url = repo['URL'][index]
      thread = threading.Thread(target=download_thread, args=(ssh, dir, id, name, url, index,))
      threads.append(thread)
      thread.start()

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    return contents

# creating SSH key
!ssh-keygen -t rsa -b 4096

!ssh-keyscan -t rsa github.com >> ~/.ssh/known_hosts

!cat /root/.ssh/id_rsa.pub

!ssh -T git@github.com

!git config --global user.email "youremail@domain.com"
!git config --global user.name "Full Name"

clone_progress = clone_all_ssh_multithreading(repo_metadata)
output_path = '' #@param { type: "string" }
clone_progress.to_excel(output_path)
print(clone_progress.shape[0])

