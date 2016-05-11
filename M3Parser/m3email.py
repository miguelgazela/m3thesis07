import re

class M3Email(object):

    def __init__(self, path, content):
        self.path = path
        self.content = content
        self.message_id = None
        self.date = None
        self.sender = None
        self.receiver = None
        self.cc = []
        self.bcc = []
        self.subject = None

    def __repr__(self):
        return self.sender

    def __eq__(self, other):
        return self.message_id == other.message_id

    def __hash__(self):
        return hash(('message_id', self.message_id, 'date', self.date))

    def safe(self, object):
        if object is None:
            return ""

        return object

    def assemble(self):

        for line in self.content:

            line = line.strip()

            # ignore message body, for now
            if not line:
                break

            if re.search("^Message-ID:", line):
                self.message_id = line[11:].strip()
            elif re.search("^Date:", line):
                self.date = line[5:].strip()
            elif re.search("^From:", line):
                self.sender = line[5:].strip()
            elif re.search("^To:", line):
                self.receiver = line[3:].strip()
            elif re.search("^Cc:", line):
                self.cc = [email.strip() for email in line[3:].strip().split(",")]
            elif re.search("^Subject:", line):
                self.subject = line[8:].strip()
