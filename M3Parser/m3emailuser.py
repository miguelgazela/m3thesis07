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

                    if email_filename == "all.mbox":

                        mbox = mailbox.mbox(email_path)
                        for message in mbox:

                            email = M3Email(message)
                            email.path = email_path

                            self.emails.append(email)

                    else:
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
            writer.writerow(('from', 'to', 'date', 'cc', 'bcc', 'is-reply'))

            for email in self.emails:

                is_reply = email.in_reply is not None
                writer.writerow((email.sender, ",".join(email.to), email.date, ",".join(email.cc), ",".join(email.bcc), is_reply))

        finally:
            f.close()
