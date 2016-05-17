import email
from os import walk

base_path = "gmail-mbox/"

messages = []
for (dirpath, dirnames, filenames) in walk(base_path):
    messages.extend(filenames)
    break

print messages[:10]
