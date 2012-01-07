from gaesessions import SessionMiddleware

# suggestion: generate your own random key using os.urandom(64)
# WARNING: Make sure you run os.urandom(64) OFFLINE and copy/paste the output to
# this file.  If you use os.urandom() to *dynamically* generate your key at
# runtime then any existing sessions will become junk every time you start,
# deploy, or update your app!
import os
COOKIE_KEY = 'D\t\x98\xc4y\x16\x16\x9b).\x10\x8en\xf3\xfd=\xb7/\xc1U\xd6\xbe\xd4\x90F\x92\xab\xf1A@\xa9J#r3w\x11\xf9;\xa5\xfa#@\xb7\x01d\xc4\x88A\xcf\xc3\x80\xd3*(\xb9\x0f\x17\xc0o7_'

def webapp_add_wsgi_middleware(app):
  from google.appengine.ext.appstats import recording
  app = SessionMiddleware(app, cookie_key=COOKIE_KEY)
  app = recording.appstats_wsgi_middleware(app)
  return app
