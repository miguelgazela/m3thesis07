import mailbox
import sys
import uuid

mbox_filename = sys.argv[1]

mbox = mailbox.mbox(mbox_filename)

if mbox:
    for message in mbox:

        message_id = message['message-id']

        if message_id:

            filename = uuid.uuid4().hex

            with open(filename, 'w') as f:
                f.write(message.as_string(True))
        else:
            print "No message ID!"
