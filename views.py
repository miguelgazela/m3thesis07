import web

t_globals = dict(
	datestr=web.datestr,
)

render = web.template.render('templates/', globals=t_globals)
render._keywords['globals']['render'] = render

def home(context):
	return render.index(context)

def messages(context):
	return render.messages(context)
