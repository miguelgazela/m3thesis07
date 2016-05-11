import os
import csv
from m3email import M3Email

class M3EmailUser(object):

    def __init__(self, folder, mailboxes):
        self.folder = folder
        self.mailbox_paths = mailboxes
        self.emails = []
        self.email = ""

    def __repr__(self):
        return self.folder + " - " + str(len(self.mailbox_paths)) + " mailboxes"

    def suit_up(self):

        for mailbox_path in self.mailbox_paths:

            initial_email_count = len(self.emails)

            email_filenames = []

            for (dirpath, dirnames, filenames) in os.walk('email_dataset/' + self.folder + "/" + mailbox_path):
                email_filenames.extend(filenames)
                break

            for email_filename in email_filenames:

                email_path = "email_dataset/" + self.folder + "/" + mailbox_path + "/" + email_filename
                email_content = [line for line in open(email_path, 'r')]

                self.emails.append(M3Email(email_path, email_content))

            print "      " + self.folder + " has " + str(len(self.emails) - initial_email_count) + " emails in mailbox " + mailbox_path

            for email in self.emails:
                email.assemble()

        # build first analysis csv file
        # if not os.path.exists("analysis/" + self.folder):
        #     os.makedirs("analysis/" + self.folder)
        #
        # print "      Saving csv file with superficial analysis for " + self.folder
        #
        # f = open("analysis/" + self.folder + "/analysis_1.csv", "wt")
        # try:
        #     writer = csv.writer(f)
        #     writer.writerow(('counter', 'message-id', 'from', 'to', 'date', 'subject', 'path'))
        #
        #     counter = 1
        #     for email in self.emails:
        #         writer.writerow((counter, email.message_id, email.sender, email.receiver, email.date, email.subject, email.path))
        #         counter += 1
        #
        # finally:
        #     f.close()
