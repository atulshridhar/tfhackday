from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
import kookoo
import logging
from gaesessions import get_current_session
from google.appengine.ext import db
from google.appengine.ext.webapp import template
import os
import datetime
import random
import urllib2
from google.appengine.api import mail

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

try:
        import json                # Python 2.7.
except ImportError:
        import simplejson as json  # Python 2.5.

from gaesessions import SessionMiddleware

from google.appengine.dist import use_library
use_library('django', '0.96')

class Candidate(db.Model):
        candidateId = db.StringProperty(required=True);
        name = db.StringProperty()
        date = db.DateProperty()
        email = db.EmailProperty();
        resumelink = db.LinkProperty();
        status = db.StringProperty();

def handleNewCall(self,response):
        response.addPlayText("Welcome To Tribal Fusion HR Desk");
        response.addPlayText("Press 1 to record your audio resume");
        response.addPlayText("Press 2 to know your interview status");
        response.addPlayText("Press 3 to know about current opportunites");
        response.addPlayText("Press 4 to speak to HR");

        response.append(kookoo.CollectDtmf(termchar='#'));

def hangupCaller(self,response):
        response.addHangup();
        
def handleWrongInput(self,response):
        response.addPlayText("you have entered wrong choice");
        response.addPlayText("please enter it again");

def handleDisconnectEvent(self,response):
        addAudioCVToDB(self,response);

def recordVoiceCV(self,response):
        response.addPlayText("Please speak about your profile for a minute");
        response.addRecord(str (random.randint(1, 1000)),maxDuration="30",silence="3",format="wav" );
        response.addPlayText("Your audio resume is submitted. your candidates id is 1 2 3 4 5 6");

def addAudioCVToDB(self,response):
        session =  get_current_session();
        state =  session.get('state',"not present");

        if (state == "RecordCV"):
                logging.info("url %s",self.request.get('data'));
                resumeURL = urllib2.unquote(self.request.get('data'));
                if resumeURL == "":
                        resumeURL = "http://tfhackday.appspot.com/static/audionotfound.wav";

                candidateId = random.randint(1, 10000);
                candidate = Candidate(key_name=str(candidateId),candidateId = str(candidateId),date = datetime.datetime.now().date(), resumelink = db.Link(resumeURL),status="InScreen");
                candidate.put();

                htmlBody="<html> <body> Dear Hiring Manager: When: Friday, January 06, 2012 11:00 AM-11:30 AM (UTC+05:30) Chennai, Kolkata, Mumbai, New Delhi.  Where: Banner (on phone) Please let us know if you have any questions.  The HR Team "
                htmlBody += "<a href='http://tfhackday.appspot.com/AcceptCandidate?id=";
                htmlBody += str(candidateId) + "'>ACCEPT</a><br><br>              ";
                htmlBody += "<a href='http://tfhackday.appspot.com/RejectCandidate?id=" + str(candidateId) + "'>    REJECT</a> </body></html>";

                mail.send_mail(sender="TribalHelpDesk.com Support <atulshridhar@gmail.com>",
                                to="HR Desk <helpdesk.tf@issueburner.com>, Vipul Jhawar <vipul.jhawar@gmail.com>",
                                subject="Candidate ID:" + str(candidateId) + "Interview Schedule",
                                body = "My Body",
                                html=htmlBody);

def getCandidateStatus(self,response):
        pass;

def getCurrentPositions(self,response):
        pass;

def handleHangup(self,response):
        pass;

class HRMenu(webapp.RequestHandler):
    def get(self):

        candidates_list = db.GqlQuery("SELECT * FROM Candidate");

        template_values = {
                'candidates_list': candidates_list,
        }

        path = os.path.join(os.path.dirname(__file__), 'templates/candidate.html');
        self.response.out.write(template.render(path, template_values))

class AcceptCandidate(webapp.RequestHandler):
      def get(self):
        id = urllib2.unquote(self.request.get('id'));
        strQuery = "SELECT * FROM Candidate WHERE candidateId='" + str(id) + "'";
        query = db.GqlQuery(strQuery);
        candidate = Candidate(key_name=query[0].candidateId,candidateId = query[0].candidateId,date = query[0].date, resumelink = query[0].resumelink,status="Accept");
        candidate.put();
        
        #candidate.get_by_key_name(key_name='candidateId');

class RejectCandidate(webapp.RequestHandler):
      def get(self):
        id = urllib2.unquote(self.request.get('id'));
        strQuery = "SELECT * FROM Candidate WHERE candidateId='" + str(id) + "'";
        query = db.GqlQuery(strQuery);
        candidate = Candidate(key_name=query[0].candidateId,candidateId = query[0].candidateId,date = query[0].date, resumelink = query[0].resumelink,status="Reject");
        candidate.put();

class CandidateStatus(webapp.RequestHandler):
      def get(self):
        id = urllib2.unquote(self.request.get('id'));
        txtweb = self.request.get('txtweb-mobile');
        txtmessage = self.request.get('txtweb-message');
        strQuery = "SELECT * FROM Candidate WHERE candidateId='" + txtmessage + "'";
        query = db.GqlQuery(strQuery);
        #print 'Interview Status:' + query[0].status;

        self.response.out.write("<html> <head> <meta name='txtweb-appkey' content='2331c057-7c40-4868-86a3-e276e158ec3e' /> </head> <body>" 
             +  query[0].status + "</body> </html>");

def getCandidateStatus(self,response):
        pass;

def getCurrentPositions(self,response):
        pass;

def handleHangup(self,response):
        pass;

class HRMenu(webapp.RequestHandler):
    def get(self):

        candidates_list = db.GqlQuery("SELECT * FROM Candidate");

        template_values = {
                'candidates_list': candidates_list,
        }

        path = os.path.join(os.path.dirname(__file__), 'templates/candidate.html');
        self.response.out.write(template.render(path, template_values))


class MainHandler(webapp.RequestHandler):
    def get(self):
        requestSid = self.request.get("sid");
        requestCallerNumber = self.request.get("cid");
        requestCalledNumber = self.request.get('called_number');
        requestData =  self.request.get('data');

        session =  get_current_session();
        state =  session.get('state',"not present");
        logging.info("STATE: %s",state);                        

        response = kookoo.Response(filler='yes');

        if(self.request.get('event') == "NewCall"):
                handleNewCall(self,response);
                session['state'] = "MainMenu";

        elif (self.request.get('event') == "GotDTMF"):
                if (state == "MainMenu"):
                        if (requestData == "1"):
                                recordVoiceCV(self,response);
                                session['state'] = "RecordCV";
                        elif (requestData == "2"):
                                getCandidateStatus(self,response);
                        elif (requestData == "3"):
                                getCurrentPositions(self,response);

        elif (self.request.get('event') == "Hangup"):
                handleHangup(self,response);

        elif (self.request.get('event') == "Record"):
                addAudioCVToDB(self,response);
                hangupCaller(self,response);

        elif (self.request.get('event') == "Disconnect"):
                handleDisconnectEvent(self,response);
                hangupCaller(self,response);
        else:
                pass;

        self.response.out.write(response);

def main():
        logging.getLogger().setLevel(logging.DEBUG)
        application = webapp.WSGIApplication([ ('/', MainHandler),
                                               ('/HRMenu',HRMenu),
                                               ('/AcceptCandidate',AcceptCandidate),
                                               ('/RejectCandidate',RejectCandidate),
                                               ('/CandidateStatus',CandidateStatus),
                                               ('/.+',MainHandler)
                                             ], debug=True);
        util.run_wsgi_app(application);

if __name__ == '__main__':
        main();
