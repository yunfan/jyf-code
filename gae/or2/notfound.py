import web

urls = (
	'.*','showError'
	)

app = web.application(urls,globals())

class showError():
    def GET(self):
	return "Sorry,the request page has not complete yet!"

if '__main__' == __name__:
    app.cgirun()
