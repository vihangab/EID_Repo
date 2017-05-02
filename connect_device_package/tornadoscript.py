#!/usr/bin/env python
import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import datetime
import time
import json

#class IndexHandler(web.RequestHandler):
#    def get(self):
#        self.render("/var/www/index.php")

class WSHandler(tornado.websocket.WebSocketHandler):
  def get(self):
	#self.render("/var/www/index.php")
	#print('Incoming message:', message)
    	self.write_message("You said: " + message)
   	if message =="get":
        	datenow = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        	json_data = json.dumps(datenow)
       	 	print(json_data)
        	print ('Incoming message:', message)
        	self.write_message("You said: " + message)
        	self.write_message(json_data)

  def check_origin(self, origin):
	return True
  def open(self):
	print ('New connection was opened')
	self.write_message("Welcome to my websocket!")

  def on_message(self, message):
	print ('Incoming message:', message)
	self.write_message("You said: " + message)
	if message =="get":
        	datenow = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        	json_data = json.dumps(datenow)
        	print(json_data)
        	print('Incoming message:', message)
        	self.write_message("You said: " + message)
        	self.write_message(json_data)
  def on_close(self):
	print ('Connection was closed...')

application = tornado.web.Application([
  (r'/ws', WSHandler),
])

if __name__ == "__main__":
  http_server = tornado.httpserver.HTTPServer(application)
  http_server.listen(8888)
  tornado.ioloop.IOLoop.instance().start()
