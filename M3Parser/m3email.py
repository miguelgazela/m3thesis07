import email
import re
from validate_email import validate_email

class M3Email(object):

    def __init__(self, path, content):
        self.path = path
        self.msg = email.message_from_string(content)

    def __init__(self, message):
        self.msg = message

    def __repr__(self):
        return self.sender

    def __eq__(self, other):
        return self.message_id == other.message_id

    def __hash__(self):
        return hash(('message_id', self.message_id, 'date', self.date))


    def get_vital_info(self):

        self.message_id = self.msg['message-id']

        self.sender = self.get_from()
        self.get_tos()
        self.get_ccs()
        self.get_bccs()

        self.subject = self.msg['subject']
        self.date = self.msg['date']

        self.get_in_reply()
        self.get_references()


    def get_from(self):

        msg_from = self.msg['from']
        if msg_from:

            address_match = re.search('<.+>', msg_from)
            if address_match:
                return address_match.group(0)[1:-1]

        return ""

    def get_tos(self):

        msg_tos = self.msg['to']
        if msg_tos:
            self.to = self.clear_addresses(msg_tos)
        else:
            self.to = []


    def get_ccs(self):

        msg_ccs = self.msg['cc']
        if msg_ccs:
            self.cc = self.clear_addresses(msg_ccs)
        else:
            self.cc = []


    def get_bccs(self):

        msg_bccs = self.msg['bcc']
        if msg_bccs:
            self.bcc = self.clear_addresses(msg_bccs)
        else:
            self.bcc = []


    def get_in_reply(self):

        in_reply = self.msg['In-Reply-To']

        if in_reply:
            self.in_reply = in_reply.strip()
        else:
            self.in_reply = None


    def get_references(self):

        msg_references = self.msg['References']

        if msg_references:
            self.references = msg_references.split()
        else:
            self.references = []


    def clear_addresses(self, raw_addresses):

        cleared = []
        msg_addresses = raw_addresses.split(',')

        for msg_address in msg_addresses:

            address_match = re.search('<.+>', msg_address)

            if address_match:

                cleared.append(address_match.group(0)[1:-1]) # remove the <> symbols

            else:
                possible_email = msg_address.strip()

                if validate_email(possible_email):
                    cleared.append(possible_email)

        return cleared
