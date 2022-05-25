from os import access
from tkinter import *
from tkinter import messagebox
from fileinput import filename
import os.path
from turtle import update
import PySimpleGUI as sg
import webbrowser
import easygui
import json
import base64
from github import Github
from github import InputGitTreeElement

data = {
    "github_access_token": '',
    "repo_name": ''
}


def load_data():
    global data
    with open('data/data.json', 'r') as openfile:
        data = json.load(openfile)


def update_data():
    global data
    json_object = json.dumps(data, indent=4)
    with open("data/data.json", "w") as outfile:
        outfile.write(json_object)


def getFile():
    filepath = easygui.fileopenbox(multiple=True)
    return filepath


def getFileName(filepath):
    filename = []
    for file in filepath:
        name = file.split('\\')
        filename.append(name[-1])

    return filename


def push_to_github(repo_name):
    global data
    TOKEN = data['github_access_token']
    print(TOKEN)
    g = Github(TOKEN)
    repo = g.get_user().get_repo(repo_name)

    file_list = getFile()
    file_names = getFileName(file_list)

    commit_message = 'python commit'
    master_ref = repo.get_git_ref('heads/main')
    master_sha = master_ref.object.sha
    base_tree = repo.get_git_tree(master_sha)

    element_list = list()
    for i, entry in enumerate(file_list):
        with open(entry) as input_file:
            data = input_file.read()
        if entry.endswith('.png'):  # images must be encoded
            data = base64.b64encode(data)
        element = InputGitTreeElement(file_names[i], '100644', 'blob', data)
        element_list.append(element)

    tree = repo.create_git_tree(element_list, base_tree)
    parent = repo.get_git_commit(master_sha)
    commit = repo.create_git_commit(commit_message, tree, [parent])
    master_ref.edit(commit.sha)


def main():
    load_data()

    window = Tk()
    window.title("Beauty Readme")
    window.geometry('500x500')

    # access token UI
    lbl_access_token = Label(window, text="Insert Github Access Token")
    lbl_access_token.grid(column=0, row=0)

    access_token_text = Entry(window, width=40)
    access_token_text.grid(column=1, row=0)

    if (len(data['github_access_token']) > 0):
        access_token_text.insert(0, data['github_access_token'])

    def access_token_button_clicked():
        data['github_access_token'] = access_token_text.get()
        update_data()

    access_token_btn = Button(
        window, text="Save", command=access_token_button_clicked)

    access_token_btn.grid(column=2, row=0)

    lbl_repo_name = Label(window, text="Insert Repository Name To Be Uploaded")
    lbl_repo_name.grid(column=0, row=1)

    repo_nametext = Entry(window, width=40)
    repo_nametext.grid(column=1, row=1)

    if (len(data['repo_name']) > 0):
        repo_nametext.insert(0, data['repo_name'])

    def repo_name_clicked():
        data['repo_name'] = repo_nametext.get()
        update_data()

    repo_name_btn = Button(
        window, text="Save", command=repo_name_clicked)

    repo_name_btn.grid(column=2, row=1)

    def profile_readme_btn_clicked():
        webbrowser.open('https://gprm.itsvg.in/', new=2)

    def project_readme_btn_clicked():
        webbrowser.open('https://readme.so/editor', new=2)

    def upload_btn_clicked():
        try:
            push_to_github(data['repo_name'])
            messagebox.showinfo("Success", "Upload Completed")
        except:
            print('an error occured')
            print('1. check your access token\n2. check your repo name')
            messagebox.showerror(
                "Error", "An error occured\n1. check your access token\n2. check your repo name")

    # Create Readme UI
    profile_readme_btn = Button(
        window, text="Profile Readme", command=profile_readme_btn_clicked)
    project_readme_btn = Button(
        window, text="Project Readme", command=project_readme_btn_clicked)
    upload_btn = Button(
        window, text="Upload To Github", command=upload_btn_clicked)

    profile_readme_btn.grid(column=0, row=2)
    project_readme_btn.grid(column=0, row=3)
    upload_btn.grid(column=0, row=4)

    window.mainloop()


main()
