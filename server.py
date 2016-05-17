import web
import views
from views import render
from config import default_config as config
import json
import os
import email

web.config.debug = False

urls = (
	'/', 'index',
	'/messages', 'messages',
	'/messages/(.+)', 'messages'
)

render = web.template.render('templates/')

base_path = 'email_dataset/_miguel/gmail-mbox-'

class index:

	def GET(self):

		return render.base(views.home(session), title='Email Ranker')


class messages:

	def POST(self):

		x = web.input(filename={})

		print "POST REQUEST"
		print x

		filename = x['filename']
		new_ranking = x['ranking']
		msg_path = x['msg_path']

		print filename
		print new_ranking
		print msg_path

		with open(msg_path + filename, 'r+') as f:
			content = f.read()
			msg_email = email.message_from_string(content)
			msg_email.replace_header('X-Mailcube-Ranking', str(new_ranking))
			f.seek(0, 0)
			f.write(msg_email.as_string(True))
			f.truncate()



	def GET(self, page_num):

		path = base_path + page_num + "/"
		print path

		msg_filenames = []

		for (dirpath, dirnames, filenames) in os.walk(path):
		    msg_filenames.extend(filenames)
		    break

		msgs = []

		print "Len: " + str(len(msg_filenames))

		for msg_filename in msg_filenames:

			msg = {
				'filename': msg_filename,
				'path': path
			}

			with open(path + "/" + msg_filename, 'r') as content_file:
				email_content = content_file.read()

				msg['email'] = email.message_from_string(email_content)

				# if msg['email'].is_multipart():
				#
				# 	for part in msg['email'].walk():
				#
				# 		ctype = part.get_content_type()
				#     	cdispo = str(part.get('Content-Disposition'))
				#
				#         if ctype == 'text/plain' and 'attachment' not in cdispo:
				#             msg['body'] = part.get_payload(decode=True)
				#             break
				#
				#
				# else:
				#     msg['body'] = msg['email'].get_payload(decode=True)

			# 	if msg.get('body', None) is None:
			# 	msg['body'] = ''
			#
			# msg['body'] = unicode(msg['body'], 'utf-8')

			current_ranking = msg['email'].get("X-Mailcube-Ranking")
			msg['ranking'] = current_ranking

			labels = msg['email'].get('X-Gmail-Labels', None)

			if labels is not None and "Chat" in labels:
				continue

			msgs.append(msg)

		print "Len: " + str(len(msgs))

		session.msgs = msgs

		return render.base(views.messages(session), title='Messages')


class MyApplication(web.application):

	def run (self, port=3030, *middleware):
		func = self.wsgifunc(*middleware)
		return web.httpserver.runsimple(func, ('0.0.0.0', port))


if __name__ == "__main__":
	app = MyApplication(urls, globals())
	app.internalerror = web.debugerror
	session = web.session.Session(app, web.session.DiskStore('sessions_m3'))
	port = int(os.environ.get('PORT', 3030))
	app.run(port=port)
