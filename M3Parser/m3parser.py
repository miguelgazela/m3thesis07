import os
from os import walk
import csv
from m3emailuser import M3EmailUser


def executeHousePartyProtocol():
    print "   Executing House Party Protocol..."

    # get all user folders
    user_folders = []
    for (dirpath, dirnames, filenames) in walk('email_dataset'):
        user_folders.extend(dirnames)
        break

    print "   Found " + str(len(user_folders)) + " users"

    # get mailboxes for each user
    users = []
    for user_folder in user_folders:

        mailboxes = []

        for (dirpath, dirnames, filenames) in walk('email_dataset/' + user_folder):
            mailboxes.extend(dirnames)
            break

        users.append(M3EmailUser(user_folder, mailboxes))

    for user in users:
        print "   Analysing " + user.folder
        user.suit_up()

    # create csv file with general statistics

    if not os.path.exists("analysis/"):
        os.makedirs("analysis")

    print "   Saving csv file with statistics "

    f = open("analysis/statistics.csv", "wt")
    try:
        writer = csv.writer(f)
        writer.writerow(('counter', 'username', '#mailboxes', '#emails'))

        counter = 1
        for user in users:
            writer.writerow((counter, user.folder, len(user.mailbox_paths), len(user.emails)))
            counter += 1

    finally:
        f.close()
