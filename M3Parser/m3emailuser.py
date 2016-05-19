import os
import csv
from m3email import M3Email
import mailbox

class M3EmailUser(object):

    def __init__(self, folder, mailboxes):
        self.folder = folder
        self.mailbox_paths = mailboxes
        self.emails = []
        self.email = ""

    def __repr__(self):
        return self.folder + " - " + str(len(self.mailbox_paths)) + " mailboxes"

    def analyse_emails(self):

        for mailbox_path in self.mailbox_paths:

            initial_email_count = len(self.emails)

            email_filenames = []

            for (dirpath, dirnames, filenames) in os.walk('email_dataset/' + self.folder + "/" + mailbox_path):
                email_filenames.extend(filenames)
                break

            for email_filename in email_filenames:

                if email_filename != ".DS_Store":

                    email_path = "email_dataset/" + self.folder + "/" + mailbox_path + "/" + email_filename

                    with open(email_path, 'r') as content_file:
                        email_content = content_file.read()

                    self.emails.append(M3Email(email_path, email_content))

            print "      " + self.folder + " has " + str(len(self.emails) - initial_email_count) + " emails in mailbox " + mailbox_path

            counter = 1
            for email in self.emails:
                counter += 1
                email.get_vital_info()

    def create_analysis_files(self):

        # build first analysis csv file
        if not os.path.exists("analysis/" + self.folder):
            os.makedirs("analysis/" + self.folder)

        print "      Saving csv file with superficial analysis for " + self.folder

        f = open("analysis/" + self.folder + "/analysis_1.csv", "wt")
        try:
            writer = csv.writer(f)
            writer.writerow(('id', 'from', 'to', '#tos', 'date', 'cc', '#cc', 'bcc', 'is-reply', 'ranking', 'sender_domain'))

            for email in self.emails:

                labels = email.msg.get('X-Gmail-Labels', None)
                if labels is not None and "Chat" in labels:
                    continue

                is_reply = email.in_reply is not None

                at_index = email.sender.find('@')
                if at_index != -1:
                    sender_domain = email.sender[at_index+1:]
                else:
                    sender_domain = ""

                writer.writerow((email.path, email.sender, ",".join(email.to), len(email.to) , email.date, ",".join(email.cc), len(email.cc), ",".join(email.bcc), is_reply, email.ranking, sender_domain))

        finally:
            f.close()
