from google.appengine.ext import ndb
import webapp2,json
import datetime
from hashlib import sha256
import uuid
pepper=""#Implement later
WEB_SOCKET_TEMPLATE="""
<script language="javascript" type="text/javascript">

  var wsUri = "ws://echo.websocket.org/";

  function init()
  {
    testWebSocket();
  }

  function testWebSocket()
  {
    websocket = new WebSocket(wsUri);
    websocket.onopen = function(evt) { onOpen(evt) };
    websocket.onclose = function(evt) { onClose(evt) };
    websocket.onmessage = function(evt) { onMessage(evt) };
    websocket.onerror = function(evt) { onError(evt) };
  }

  function onOpen(evt)
  {
  }

  function onClose(evt)
  {
  }

  function onMessage(evt)
  {
    doSend("WebSocket rocks");
  }

  function onError(evt)
  {
  }

  function doSend(message)
  {
    websocket.send(message);
  }

  window.addEventListener("load", init, false);

  </script>
"""
ALL_PAGES_HEADER_TEMPLATE = """
<style>
h1{
line-height: 90px;
font-style:bold;
display:inline
}
h2{
line-height: 30px;
font-family: "Times New Roman",Times,serif;
font-style:normal;
font-size:0.9em;
display:inline
}
img
{
height:90px;
vertical-align:bottom
}
header
{
    background-color:#0000FF;
}
table {
    font-family: arial, sans-serif;
    border-collapse: collapse;
    width: 100%;
}

td, th {
    border: 1px solid #dddddd;
    text-align: left;
    padding: 8px;
}

tr:nth-child(even) {
    background-color: #dddddd;
}
</style>
<header><div><h1><a href="../"><img src="https://storage.googleapis.com/millburntutorclub.appspot.com/Logo.png" alt="Logo"></a><b><a href="/" style="text-decoration:none;color:white">Millburn High School Tutoring Club</a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</b></h1><h2><a href="/404" style="text-decoration:none;color:white">Who are we?</a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</h2><h2><a href="/404" style="text-decoration:none;color:white">What do we do?</a></h2></div>
<script>
  // Initialize Firebase
  var config = {
    apiKey: "AIzaSyCSm5Q8IF_PDsyJQXmDjiSoDlyhmd-OA5U",
    authDomain: "millburntutorclub.firebaseapp.com",
    databaseURL: "https://millburntutorclub.firebaseio.com",
    projectId: "millburntutorclub",
    storageBucket: "millburntutorclub.appspot.com",
    messagingSenderId: "565270734161"
  };
  firebase.initializeApp(config);
</script>
<script src="https://code.jquery.com/jquery-1.10.2.js"></script>
<script src="//code.jquery.com/jquery-1.12.4.js"></script>
<script src="//code.jquery.com/ui/1.12.1/jquery-ui.js"></script>
<script src="https://www.gstatic.com/firebasejs/4.12.1/firebase.js"></script>
<link rel="stylesheet" href="//code.jquery.com/ui/1.12.1/themes/smoothness/jquery-ui.css">
</header>
"""
MAIN_PAGE_FOOTER_TEMPLATE = """\
        <div id="Tutir"><select id="selecting" name = "POTW">
        <option value='default'>Select Tutor</option>
       """
MAIN_PAGE_FOOTER_TEMPLATE_2 ="""     </select>
        </div>
        Credential:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Availability:
        <div id='Credentials'><textarea rows = '5' cols = '30' readonly></textarea><textarea rows = '5' cols = '30' readonly></textarea></br></br></div></br></br>
        <div><textarea rows = "5" cols = "30" name="content" placeholder="Request"></textarea></div>
        <div><input type="submit" value="Submit Your Tutoring Request"></div>
    </form>
"""
MAIN_2_P ="""     </select>
        </div>
        Credential:
        <div id="Credentials"><textarea rows = '5' cols = '30' readonly></textarea></div>Availability:</br>
"""
MAIN_3_P ="""</br></br>
        <div><textarea rows = "5" cols = "30" name="content" placeholder="Request"></textarea></div>
        <div><input type="submit" value="Submit Your Tutoring Request"></div>
    </form>
"""
MAIN="""
    Your Ongoing Tutoring Requests:<br/>
    Unresolved:<br/>
"""
MAIN_A="""
    <table>
    <tr><th><th>Number<th>Tutor Username<th>Credential<th>Content<th>Time Booked<th>Date Booked
"""
MAIN_PAGE_FOOTER_TEMPLATE_3 ="""
</table>
<input type="submit" name="bleh" value="Delete">
</form>
Accepted:<br/>
"""
MAIN_B="""
<table>
<tr><th><th>Number<th>Tutor Username<th>Credential<th>Content<th>Time Booked<th>Date Booked
"""
MAIN_PAGE_FOOTER_TEMPLATE_4 ="""
</table>
<input type="submit" name="Bleh" value="Delete">
</form>
<script type="text/javascript">
$("#selecting")
  .change(function () {
    $('#user').val($('select[name="POTW"]').val())
    $.post("/ajax/mainselect2",
    JSON.stringify($('select[name="POTW"]').val()),
    function(resp){document.getElementById("Credentials").innerHTML=JSON.parse(resp)}
);
now();
});
  function now(){
    $.post("/ajax/student",
    JSON.stringify({name:$('#user').val(),date:$('#datepicker').datepicker({ dateFormat: 'dd/mm/yy' }).val()}),
    function(resp){document.getElementById("times").innerHTML=JSON.parse(resp)}
    );
  }
  $( function() {
    $( "#datepicker" ).datepicker({dateFormat: 'dd/mm/yy'}).datepicker('setDate', new Date());
    now();
    } );
  $("#datepicker")
  .datepicker({
  onSelect: function () {
    $.post("/ajax/student",
    JSON.stringify({name:$('#user').val(),date:$('#datepicker').datepicker({ dateFormat: 'dd/mm/yy' }).val()}),
    function(resp){document.getElementById("times").innerHTML=JSON.parse(resp)}
    );
    }});
  </script>
</body>
</html>
"""
SIGN_IN_PAGE_FOOTER_TEMPLATE = """\
    <fieldset>
    <legend>Sign in</legend>
    <form action="/handler" method="post">
        <div><input type = "text" name="name" placeholder="Email"></input></div>
        <div><input type = "password" name="pass" placeholder="Password"></textarea ></div>
        <input type="submit" value="Sign In">
    </form>
    </fieldset>
    <form action="/signup" method="post">
        <div><input type="submit" value="Sign Up"></div>
    </form>
  </body>
</html>
"""
SIGN_UP_PAGE_FOOTER_TEMPLATE = """\
    <fieldset>
    <legend>Sign up</legend>
    <form action="/handlesignup" method="post">
        <div><input type = "text" name="email" placeholder="Email"></input></div>
        <div><input type = "password" name="pass" placeholder="Password"></textarea ></div>
        <div><input type = "password" name="pass2" placeholder="Retype Password"></textarea ></div>
        <div><input type="submit" value="Sign Up"></div>
    </form>
    </fieldset>
    <form action="/" method="post">
        <div><input type="submit" value="Sign In"></div>
    </form>
  </body>
</html>
"""
DISPLAY_PAGE_FOOTER_TEMPLATE = """\
        <div><textarea rows = "5" cols = "30" name="POTW" placeholder="Enter credential here"></textarea></div>
        <div><input type="submit" value="Change your Credentials"></div>
    </form>
"""
DISPLAY_PAGE_FOOTER_TEMPLATE_A = """\
        <div><textarea rows = "5" cols = "30" name="Ava" placeholder="Enter availability here"></textarea></div>
        <div><input type="submit" value="Change your Availability"></div>
    </form>
"""
DISPLAY_PAGE_FOOTER_TEMPLATE_N="""
        <div><input type="submit" value="Enter Student View"></div>
    </form>
    <form action="/404" method="post">
        <div><input type="text" name="Filter" placeholder = "Filter"></input></div>
        <div><input type="submit" value="Filter"></div>
    </form>
    Unresolved Requests:
"""
DISPLAY_B="""
    <table>
    <tr><th><th>Number<th>Username<th>Content<th>Time Booked<th>Date Booked
"""
DISPLAY_PAGE_FOOTER_TEMPLATE_1 = """
  </table>
"""
DISPLAY_A="""
  </form>
  Accepted Requests:
"""
DISPLAY_PAGE_FOOTER_TEMPLATE_2="""
  <table>
  <tr><th><th>Number<th>Username<th>Content<th>Time Booked<th>Date Booked
"""
DISPLAY_PAGE_FOOTER_TEMPLATE_3= """
  </table>
  <input type="submit" value="Unaccept">
  </form>
  <script>
  function now(){
    $.post("/ajax/date",
    JSON.stringify({name:$('#user').val(),date:$('#datepicker').datepicker({ dateFormat: 'dd/mm/yy' }).val()}),
    function(resp){document.getElementById("times").innerHTML=JSON.parse(resp)}
    );
  }
  $( function() {
    $( "#datepicker" ).datepicker({dateFormat: 'dd/mm/yy'}).datepicker('setDate', new Date());
    now();
    } );
  $("#datepicker")
  .datepicker({
  onSelect: function () {
    $.post("/ajax/date",
    JSON.stringify({name:$('#user').val(),date:$('#datepicker').datepicker({ dateFormat: 'dd/mm/yy' }).val()}),
    function(resp){document.getElementById("times").innerHTML=JSON.parse(resp)}
    );
    }});
  </script>
  </body>
</html>
"""
ADMIN_A="""
<form action="/404" method="post">
        <div><input type="text" name="Filter" placeholder = "Filter"></input></div>
        <div><input type="submit" value="Filter"></div>
</form>
Users:
"""
ADMIN_B="""
<table>
<tr><th><th>Username<th>Role<th>New Role
"""
ADMIN_C="""
</table>
"""
ADMIN_D="""
</form>
"""
ADMIN_E="""
<div><input type="submit" value="Enter Teacher View"></div>
    </form>
"""
ADMIN_F="""
<div><input type="submit" value="Enter Student View"></div>
    </form>
"""
TO_ADMIN="""
<div><input type="submit" value="Enter Admin View"></div>
    </form>
"""
DEFAULT_GUESTBOOK_NAME = 'default_guestbook'
def form(self,url,session):
    self.response.write("<form action='"+url+"?session="+session+"' method='post'>")
def ridirect(self,url,session):
    if((datetime.datetime.now()-ndb.Key(sessions,session).get().time)<datetime.timedelta(minutes=30)):
        session1=ndb.Key(sessions,session).get()
        self.redirect(url+"?session="+session)
        session1.time=datetime.datetime.now()
        session1.put()
    else:
        ndb.Key(sessions,session).delete()
        self.redirect("/")
def handleadmin(self):
    if(ndb.Key(sessions,self.request.get('session')).get().level=='admins'):
        self.response.write(ALL_PAGES_HEADER_TEMPLATE)
        self.response.write(ADMIN_A)
        form(self,'/',self.request.get('session'))
        self.response.write(ADMIN_B)
        keys = users.query().fetch(1000,keys_only=True)
        j=0
        for i in keys:
            entry = i.get()
            if(entry.role=='teachers'):
                j=j+1
                self.response.write("<tr><td><input type='checkbox' name='"+str(j)+"' value='on'><td>"+ str(entry.username) +"<td>Tutor<td><select name = 'Role"+str(j)+"'><option value='default'>Role</option><option value='Student'>Student</option><option value='Admin'>Admin</option></select>")
            elif(entry.role=='students'):
                j=j+1
                self.response.write("<tr><td><input type='checkbox' name='"+str(j)+"' value='on'><td>"+ str(entry.username) +"<td>Student<td><select name = 'Role"+str(j)+"'><option value='default'>Role</option><option value='Teacher'>Teacher</option><option value='Admin'>Admin</option></select>")
            else:
                self.response.write("<tr><td><td>"+ str(entry.username) +"<td>Admin")
        self.response.write(ADMIN_C)
        self.response.write("<input type='submit' formaction='/delete3?session="+str(self.request.get('session'))+"' value='Delete'>")
        self.response.write("<input type='submit' formaction='/promote?session="+str(self.request.get('session'))+"' value='Promote'>")
        self.response.write(ADMIN_D)
        form(self,'/view',self.request.get('session'))
        self.response.write(ADMIN_E)
        form(self,'/POTW',self.request.get('session'))
        self.response.write(ADMIN_F)
class adminconsole(webapp2.RequestHandler):
    def get(self):
        handleadmin(self)
    def post(self):
        handleadmin(self)
def guestbook_key(guestbook_name=DEFAULT_GUESTBOOK_NAME):
    return ndb.Key('Guestbook', guestbook_name)
class Signuphandler(webapp2.RequestHandler):
    def post(self):
        nameavailable=False
        yes = False
        if(self.request.get('pass2')==self.request.get('pass')):
            yes = True
            nameavailable=True
            keys = users.query().fetch(keys_only=True)
            for i in keys:
                entry = i.get()
                if (entry.username == self.request.get('email')):
                   nameavailable = False
        if(nameavailable == True & yes != False):
            person = users()
            person.exists=True
            person.password = str(sha256(str(self.request.get('pass'))).hexdigest())
            person.username = self.request.get('email')
            person.role='students'
            person.exists=True
            person.put()
            self.redirect('/')
        else:
            self.redirect('/signup')#Same thing but with error message
class Author(ndb.Model):
    """Sub model for representing an author."""
    identity = ndb.StringProperty(indexed=False)
class Construction(webapp2.RequestHandler):
    def get(self):
        self.response.write(ALL_PAGES_HEADER_TEMPLATE)
        self.response.write("<p>This page is under construction. Please try again later.</p>")
    def post(self):
        self.response.write(ALL_PAGES_HEADER_TEMPLATE)
        self.response.write("<p>This page is under construction. Please try again later.</p>")
class Greeting(ndb.Model):
    """A main model for representing an individual Guestbook entry."""
    author = ndb.StringProperty(indexed=False)
    content = ndb.StringProperty(indexed=False)
    date = ndb.DateTimeProperty(auto_now_add=True)
    potw = ndb.StringProperty(indexed=False)
    accepted = ndb.BooleanProperty(indexed=False)
    exists = ndb.BooleanProperty(indexed=False)
    seconds=ndb.StringProperty(indexed=False)
    dateBooked=ndb.StringProperty(indexed=False)
class users(ndb.Model):
    """A main model for representing an individual Guestbook entry."""
    username = ndb.StringProperty(indexed=False)
    password = ndb.StringProperty(indexed=False)
    role = ndb.StringProperty(indexed=False)
    exists = ndb.BooleanProperty(indexed=False)
class sessions(ndb.Model):
    """A main model for representing an individual Guestbook entry."""
    username = ndb.StringProperty(indexed=False)
    level = ndb.StringProperty(indexed=False)
    time=ndb.DateTimeProperty(auto_now_add=True)
class Done(webapp2.RequestHandler):
    def get(self):
        self.response.write(ALL_PAGES_HEADER_TEMPLATE)
        self.response.write("Thank You For Submitting Your Request. It Will Be Displayed In Your Homepage.")
        form(self,"/POTW",self.request.get('session'))
        self.response.write("""
                    <div><input type="submit" value="Back"></div>
                               </form>""")
class Done2(webapp2.RequestHandler):
    def get(self):
        self.response.write(ALL_PAGES_HEADER_TEMPLATE)
        self.response.write("Thank You For Submitting Your Request. It Will Be Displayed In Your Homepage.")
        form(self,"/POTW2",self.request.get('session'))
        self.response.write("""
                    <div><input type="submit" value="Back"></div>
                               </form>""")
class Handler(webapp2.RequestHandler):
    def post(self):
        username = self.request.get('name')
        password = self.request.get('pass')
        keys = users.query().fetch(keys_only=True)
        yes1 = False
        try:
            mykey=keys[0]
        except:
            self.redirect('/signup')
        for i in keys:
            entry = i.get()
            if (entry.username==username):
                if (entry.password==str(sha256(password).hexdigest())):
                    yes1 = True
                    mykey=i
                    break
        if(yes1==True):
            if(mykey.get().role=='admins' or mykey.get().role=='teachers' or mykey.get().role=='students'):
                keys = sessions.query().fetch(keys_only=True)
                for i in keys:
                    entry=i.get()
                    if(entry.username==username):
                        entry.key.delete()
            if(mykey.get().role=='admins'):
                sessioncode=str(uuid.uuid1())
                session=sessions()
                session.username=username
                session.level='admins'
                session.key=ndb.Key(sessions,sessioncode)
                session.time=datetime.datetime.now()
                session.put()
                ridirect(self,'/admin',sessioncode)
            elif(mykey.get().role=='teachers'):
                sessioncode=str(uuid.uuid1())
                session=sessions()
                session.username=username
                session.level='teachers'
                session.key=ndb.Key(sessions,sessioncode)
                session.time=datetime.datetime.now()
                session.put()
                ridirect(self,'/view',sessioncode)
            elif(mykey.get().role=='students'):
                sessioncode=str(uuid.uuid1())
                session=sessions()
                session.username=username
                session.level='students'
                session.key=ndb.Key(sessions,sessioncode)
                session.time=datetime.datetime.now()
                session.put()
                ridirect(self,'/POTW',sessioncode)
            else:
                self.redirect('/')#page same as '/' but with error message.
        else:
            self.redirect('/')#page same as '/' but with error message.
class Putter(webapp2.RequestHandler):    
    def post(self):
        if(self.request.get('POTW')!='default'):
            guestbook_name = self.request.get('guestbook_name',
                                              DEFAULT_GUESTBOOK_NAME)
            greeting = Greeting(parent=guestbook_key(guestbook_name))
            greeting.content = self.request.get('content')
            greeting.author = ndb.Key(sessions,self.request.get('session')).get().username
            greeting.potw=self.request.get('POTW')
            greeting.accepted=False
            greeting.exists=True
            greeting.put()
            ridirect(self,"/done",self.request.get('session'))
        else:
            ridirect(self,"/POTW",self.request.get('session'))
class Putter2(webapp2.RequestHandler):    
    def post(self):
        if(self.request.get('POTW')!='default'):
            guestbook_name = self.request.get('guestbook_name',
                                              DEFAULT_GUESTBOOK_NAME)
            greeting = Greeting(parent=guestbook_key(guestbook_name))
            greeting.content = self.request.get('content')
            greeting.author = ndb.Key(sessions,self.request.get('session')).get().username
            greeting.seconds=self.request.get('timestamps')
            greeting.potw=self.request.get('POTW')
            greeting.dateBooked=self.request.get('datepicker')
            greeting.accepted=False
            greeting.exists=True
            greeting.put()
            ridirect(self,"/done2",self.request.get('session'))
        else:
            ridirect(self,"/POTW2",self.request.get('session'))
class Signup(webapp2.RequestHandler):
    def get(self):
        self.response.write(ALL_PAGES_HEADER_TEMPLATE)
        self.response.write(SIGN_UP_PAGE_FOOTER_TEMPLATE)
    def post(self):
        self.response.write(ALL_PAGES_HEADER_TEMPLATE)
        self.response.write(SIGN_UP_PAGE_FOOTER_TEMPLATE)
class code(ndb.Model):
    username=ndb.StringProperty(indexed=False)
def handleDisplay2(self):
    self.response.write(ALL_PAGES_HEADER_TEMPLATE)
    if(ndb.Key(sessions,self.request.get('session')).get().level=='admins' or ndb.Key(sessions,self.request.get('session')).get().level=='teachers'):
        form(self,"/handleteach",self.request.get('session'))
        self.response.write(DISPLAY_PAGE_FOOTER_TEMPLATE)
        fifteen=datetime.timedelta(minutes=30)
        self.response.write("<form action='/ava?session="+self.request.get('session')+"' method='post'><input type='hidden' id='user' value='"+ndb.Key(sessions,self.request.get('session')).get().username+"'><input id='datepicker' name='datepicker'><div id='times'><table><tr><th><th>Time Slot<th><th>Time Slot")
        for i in range(1,25):
            self.response.write("<tr><td><input type='checkbox' name='"+str(i*fifteen.seconds)+"' value='on'><td>"+str(((i-1)*fifteen.seconds)/3600)+":"+str((((i-1)*fifteen.seconds)/60)%60).zfill(2)+"-"+str((i*fifteen.seconds)/3600)+":"+str(((i*fifteen.seconds)/60)%60).zfill(2)+"<td><input type='checkbox' name='"+str((i+24)*fifteen.seconds)+"' value='on'><td>"+str(((i+23)*fifteen.seconds)/3600)+":"+str((((i+23)*fifteen.seconds)/60)%60).zfill(2)+"-"+str(((i+24)*fifteen.seconds)/3600)+":"+str((((i+24)*fifteen.seconds)/60)%60).zfill(2))
        self.response.write("</table></div><input type='submit' value='Submit your Availability'></form>")
        if(ndb.Key(sessions,self.request.get('session')).get().level=='admins'):
            form(self,"/admin",self.request.get('session'))
            self.response.write(TO_ADMIN)
        form(self,"/POTW",self.request.get('session'))
        self.response.write(DISPLAY_PAGE_FOOTER_TEMPLATE_N)
        form(self,"resolve",self.request.get('session'))
        self.response.write(DISPLAY_B)
        keys = Greeting.query().fetch(1000,keys_only=True)
        j=0
        for i in keys:
            entry = i.get()
            if(entry.potw==ndb.Key(sessions,self.request.get('session')).get().username and entry.accepted==False and entry.exists==True):
                j=j+1
                timesec=int(entry.seconds)
                self.response.write("<tr><td><input type='checkbox' name='"+str(j)+"' value='on'><td>"+ str(j) +"<td>"+str(entry.author) + "<td>" + str(entry.content)+"<td>"+str((timesec-1800)/3600)+":"+str(((timesec-1800)/60)%60).zfill(2)+"-"+str((timesec)/3600)+":"+str(((timesec)/60)%60).zfill(2)+"<td>"+str(entry.dateBooked))       
        self.response.write(DISPLAY_PAGE_FOOTER_TEMPLATE_1)
        self.response.write("<input type='submit' formaction='/resolve?session="+self.request.get('session')+"' value='Accept'><input type='submit' formaction='/delete2?session="+self.request.get('session')+"' value='Delete'>")
        self.response.write(DISPLAY_A)
        form(self,"/unresolve",self.request.get('session'))
        self.response.write(DISPLAY_PAGE_FOOTER_TEMPLATE_2)
        j=0
        for i in keys:
            entry = i.get()
            if(entry.potw==ndb.Key(sessions,self.request.get('session')).get().username and entry.accepted==True and entry.exists==True):
                j=j+1
                timesec=int(entry.seconds)
                self.response.write("<tr><td><input type='checkbox' name='"+str(j)+"' value='on'><td>"+ str(j) +"<td>"+str(entry.author) + "<td>" + str(entry.content)+"<td>"+str((timesec-1800)/3600)+":"+str(((timesec-1800)/60)%60).zfill(2)+"-"+str((timesec)/3600)+":"+str(((timesec)/60)%60).zfill(2)+"<td>"+str(entry.dateBooked))        
        self.response.write(DISPLAY_PAGE_FOOTER_TEMPLATE_3)
class Display2(webapp2.RequestHandler):
    def get(self):
        handleDisplay2(self)
    def post(self):
        handleDisplay2(self)
def handleDisplay(self):
    self.response.write(ALL_PAGES_HEADER_TEMPLATE)
    if(ndb.Key(sessions,self.request.get('session')).get().level=='admins' or ndb.Key(sessions,self.request.get('session')).get().level=='teachers'):
        form(self,"/handleteach",self.request.get('session'))
        self.response.write(DISPLAY_PAGE_FOOTER_TEMPLATE)
        form(self,"/handleteach2",self.request.get('session'))
        self.response.write(DISPLAY_PAGE_FOOTER_TEMPLATE_A)
        if(ndb.Key(sessions,self.request.get('session')).get().level=='admins'):
            form(self,"/admin",self.request.get('session'))
            self.response.write(TO_ADMIN)
        form(self,"/POTW",self.request.get('session'))
        self.response.write(DISPLAY_PAGE_FOOTER_TEMPLATE_N)
        form(self,"resolve",self.request.get('session'))
        self.response.write(DISPLAY_B)
        keys = Greeting.query().fetch(1000,keys_only=True)
        j=0
        for i in keys:
            entry = i.get()
            if(entry.potw==ndb.Key(sessions,self.request.get('session')).get().username and entry.accepted==False and entry.exists==True):
                j=j+1
                self.response.write("<tr><td><input type='checkbox' name='"+str(j)+"' value='on'><td>"+ str(j) +"<td>"+str(entry.author) + "<td>" + str(entry.content))       
        self.response.write(DISPLAY_PAGE_FOOTER_TEMPLATE_1)
        self.response.write("<input type='submit' formaction='/resolve?session="+self.request.get('session')+"' value='Accept'><input type='submit' formaction='/delete2?session="+self.request.get('session')+"' value='Delete'>")
        self.response.write(DISPLAY_A)
        form(self,"/unresolve",self.request.get('session'))
        self.response.write(DISPLAY_PAGE_FOOTER_TEMPLATE_2)
        j=0
        for i in keys:
            entry = i.get()
            if(entry.potw==ndb.Key(sessions,self.request.get('session')).get().username and entry.accepted==True and entry.exists==True):
                j=j+1
                self.response.write("<tr><td><input type='checkbox' name='"+str(j)+"' value='on'><td>"+ str(j) +"<td>"+str(entry.author) + "<td>" + str(entry.content))        
        self.response.write(DISPLAY_PAGE_FOOTER_TEMPLATE_3)
class Display(webapp2.RequestHandler):
    def get(self):
        handleDisplay(self)
    def post(self):
        handleDisplay(self)
class available(ndb.Model):
    username=ndb.StringProperty(indexed=False)
    seconds=ndb.IntegerProperty(indexed=False)
    date=ndb.StringProperty(indexed=False)
class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.write(ALL_PAGES_HEADER_TEMPLATE)
        self.response.write(SIGN_IN_PAGE_FOOTER_TEMPLATE)
    def post(self):
        self.response.write(ALL_PAGES_HEADER_TEMPLATE)
        self.response.write(SIGN_IN_PAGE_FOOTER_TEMPLATE)
def handleGuestbook2(self):
    if(ndb.Key(sessions,self.request.get('session')).get().level=='students' or ndb.Key(sessions,self.request.get('session')).get().level=='admins' or ndb.Key(sessions,self.request.get('session')).get().level=='teachers'):
        form(self,"/processing2",self.request.get('session'))
        self.response.write(MAIN_PAGE_FOOTER_TEMPLATE)
        keys = users.query().fetch(keys_only=True)
        for i in keys:
            j=i.get()
            if(j.role!='students'):
                self.response.write("<option value='"+str(j.username)+"'>"+str(j.username)+"</option>")
        self.response.write(MAIN_2_P)
        fifteen=datetime.timedelta(minutes=30)
        self.response.write("<input type='hidden' id='user' value=''><input id='datepicker' name='datepicker'><div id='times'><table><tr><th><th>Time Slot")
        self.response.write("</table></div>")
        self.response.write(MAIN_3_P)
        if(ndb.Key(sessions,self.request.get('session')).get().level=='admins' or ndb.Key(sessions,self.request.get('session')).get().level=='teachers'):
            form(self,"/view",self.request.get('session'))
            self.response.write(ADMIN_E)
        if(ndb.Key(sessions,self.request.get('session')).get().level=='admins'):
            form(self,"/admin",self.request.get('session'))
            self.response.write(TO_ADMIN)
        form(self,"/delete1",self.request.get('session'))
        self.response.write(MAIN)
        self.response.write(MAIN_A)
        keys = Greeting.query().fetch(keys_only=True)
        k=0
        for i in keys:
            j=i.get()
            if(j.author==ndb.Key(sessions,self.request.get('session')).get().username and j.accepted==False and j.exists==True):
                k=k+1
                timesec=int(j.seconds)
                if(str(ndb.Key(potw,j.potw).get())==None):
                    self.response.write("<tr><td><input type='checkbox' name='"+str(k)+"' value='on'><td>"+str(k)+"<td>"+str(j.potw)+"<td><td>"+str(j.content)+"<td>"+str((timesec-1800)/3600)+":"+str(((timesec-1800)/60)%60).zfill(2)+"-"+str((timesec)/3600)+":"+str(((timesec)/60)%60).zfill(2)+"<td>"+str(j.dateBooked))
                else:
                   self.response.write("<tr><td><input type='checkbox' name='"+str(k)+"' value='on'><td>"+str(k)+"<td>"+str(j.potw)+"<td>"+str(ndb.Key(potw,j.potw).get().potw)+"<td>"+str(j.content)+"<td>"+str((timesec-1800)/3600)+":"+str(((timesec-1800)/60)%60).zfill(2)+"-"+str((timesec)/3600)+":"+str(((timesec)/60)%60).zfill(2)+"<td>"+str(j.dateBooked))
        self.response.write(MAIN_PAGE_FOOTER_TEMPLATE_3)
        form(self,"/delete1",self.request.get('session'))
        self.response.write(MAIN_B)
        k=0
        for i in keys:
            j=i.get()
            if(j.author==ndb.Key(sessions,self.request.get('session')).get().username and j.accepted==True and j.exists==True):
                k=k+1
                timesec=int(j.seconds)
                self.response.write("<tr><td><input type='checkbox' name='"+str(k)+"' value='on'><td>"+str(k)+"<td>"+str(j.potw)+"<td>"+str(ndb.Key(potw,j.potw).get().potw)+"<td>"+str(j.content)+"<td>"+str((timesec-1800)/3600)+":"+str(((timesec-1800)/60)%60).zfill(2)+"-"+str((timesec)/3600)+":"+str(((timesec)/60)%60).zfill(2)+"<td>"+str(j.dateBooked))
        self.response.write(MAIN_PAGE_FOOTER_TEMPLATE_4)
class Guestbook2(webapp2.RequestHandler):
    def get(self):
        if(ndb.Key(sessions,self.request.get('session')).get().username!=None):
            self.response.write(ALL_PAGES_HEADER_TEMPLATE)
            handleGuestbook2(self)
    def post(self):
        if(ndb.Key(sessions,self.request.get('session')).get().username!=None):
            self.response.write(ALL_PAGES_HEADER_TEMPLATE)
            handleGuestbook2(self)
def handleGuestbook(self):
    if(ndb.Key(sessions,self.request.get('session')).get().level=='students' or ndb.Key(sessions,self.request.get('session')).get().level=='admins' or ndb.Key(sessions,self.request.get('session')).get().level=='teachers'):
        form(self,"/processing",self.request.get('session'))
        self.response.write(MAIN_PAGE_FOOTER_TEMPLATE)
        keys = users.query().fetch(keys_only=True)
        for i in keys:
            j=i.get()
            if(j.role!='students'):
                self.response.write("<option value='"+str(j.username)+"'>"+str(j.username)+"</option>")
        self.response.write(MAIN_PAGE_FOOTER_TEMPLATE_2)
        if(ndb.Key(sessions,self.request.get('session')).get().level=='admins' or ndb.Key(sessions,self.request.get('session')).get().level=='teachers'):
            form(self,"/view",self.request.get('session'))
            self.response.write(ADMIN_E)
        if(ndb.Key(sessions,self.request.get('session')).get().level=='admins'):
            form(self,"/admin",self.request.get('session'))
            self.response.write(TO_ADMIN)
        form(self,"/delete1",self.request.get('session'))
        self.response.write(MAIN)
        self.response.write(MAIN_A)
        keys = Greeting.query().fetch(keys_only=True)
        k=0
        for i in keys:
            j=i.get()
            if(j.author==ndb.Key(sessions,self.request.get('session')).get().username and j.accepted==False and j.exists==True):
                k=k+1
                if(str(ndb.Key(potw,j.potw).get())==None):
                    self.response.write("<tr><td><input type='checkbox' name='"+str(k)+"' value='on'><td>"+str(k)+"<td>"+str(j.potw)+"<td><td>"+str(j.content))
                else:
                   self.response.write("<tr><td><input type='checkbox' name='"+str(k)+"' value='on'><td>"+str(k)+"<td>"+str(j.potw)+"<td>"+str(ndb.Key(potw,j.potw).get().potw)+"<td>"+str(j.content))
        self.response.write(MAIN_PAGE_FOOTER_TEMPLATE_3)
        form(self,"/delete1",self.request.get('session'))
        self.response.write(MAIN_B)
        k=0
        for i in keys:
            j=i.get()
            if(j.author==ndb.Key(sessions,self.request.get('session')).get().username and j.accepted==True and j.exists==True):
                k=k+1
                self.response.write("<tr><td><input type='checkbox' name='"+str(k)+"' value='on'><td>"+str(k)+"<td>"+str(j.potw)+"<td>"+str(ndb.Key(potw,j.potw).get().potw)+"<td>"+str(j.content))
        self.response.write(MAIN_PAGE_FOOTER_TEMPLATE_4)
class Guestbook(webapp2.RequestHandler):
    def get(self):
        if(ndb.Key(sessions,self.request.get('session')).get().username!=None):
            self.response.write(ALL_PAGES_HEADER_TEMPLATE)
            handleGuestbook(self)
    def post(self):
        if(ndb.Key(sessions,self.request.get('session')).get().username!=None):
            self.response.write(ALL_PAGES_HEADER_TEMPLATE)
            handleGuestbook(self)
class potw(ndb.Model):
    """A main model for representing an individual Guestbook entry."""
    potw=ndb.StringProperty(indexed=False)
    author=ndb.StringProperty(indexed=False)
class availability(ndb.Model):
    """A main model for representing an individual Guestbook entry."""
    potw=ndb.StringProperty(indexed=False)
    author=ndb.StringProperty(indexed=False)
class logs(ndb.Model):
    text=ndb.StringProperty(indexed=False)
class Handleteach(webapp2.RequestHandler):
    def post(self):
        potww=self.request.get('POTW')
        mypotw=potw()
        mypotw.potw=potww
        username=ndb.Key(sessions,self.request.get('session')).get().username
        mypotw.author=username
        mypotw.key=ndb.Key(potw,username)
        mypotw.put()
        ridirect(self,"/view",self.request.get('session'))
class Handleteach2(webapp2.RequestHandler):
    def post(self):
        potww=self.request.get('Ava')
        mypotw=availability()
        mypotw.potw=potww
        username=ndb.Key(sessions,self.request.get('session')).get().username
        mypotw.author=username
        mypotw.key=ndb.Key(availability,username)
        mypotw.put()
        ridirect(self,"/view",self.request.get('session'))
class Resolverequest(webapp2.RequestHandler):
    def post(self):
        j=0
        keys = Greeting.query().fetch(keys_only=True)
        for i in keys:
            entry = i.get()
            if(entry.potw==ndb.Key(sessions,self.request.get('session')).get().username and entry.exists==True):
                j=j+1
                if(self.request.get(str(j))=='on'):
                    entry.accepted=True
                    entry.put()
        ridirect(self,"/view",self.request.get('session'))
class Unresolverequest(webapp2.RequestHandler):
    def post(self):
        j=0
        keys = Greeting.query().fetch(keys_only=True)
        for i in keys:
            entry = i.get()
            if(entry.potw==ndb.Key(sessions,self.request.get('session')).get().username and entry.exists==True):
                j=j+1
                if(self.request.get(str(j))=='on'):
                    entry.accepted=False
                    entry.put()
        ridirect(self,"/view",self.request.get('session'))
class Delete1(webapp2.RequestHandler):
    def post(self):
        j=0
        if(self.request.get("bleh")=="Delete"):
            keys = Greeting.query().fetch(keys_only=True)
            for i in keys:
                entry = i.get()
                if(entry.author==ndb.Key(sessions,self.request.get('session')).get().username and entry.accepted==False and entry.exists==True):
                    j=j+1
                    if(self.request.get(str(j))=='on'):
                        entry.exists=False
                        entry.put()
        elif(self.request.get("Bleh")=="Delete"):
            keys = Greeting.query().fetch(keys_only=True)
            for i in keys:
                entry = i.get()
                if(entry.author==ndb.Key(sessions,self.request.get('session')).get().username and entry.accepted==True and entry.exists==True):
                    j=j+1
                    if(self.request.get(str(j))=='on'):
                        entry.exists=False
                        entry.put()
        #garbage collection
        keys = Greeting.query().fetch(keys_only=True)
        for i in keys:
            entry = i.get()
            if(entry.exists==False):
                entry.key.delete()
        ridirect(self,"/POTW",self.request.get('session'))
class Delete2(webapp2.RequestHandler):
    def post(self):
        j=0
        keys = Greeting.query().fetch(keys_only=True)
        for i in keys:
            entry = i.get()
            if(entry.potw==ndb.Key(sessions,self.request.get('session')).get().username and entry.accepted==False and entry.exists==True):
                j=j+1
                if(self.request.get(str(j))=='on'):
                    entry.exists=False
                    entry.put()
        #garbage collection
        keys = Greeting.query().fetch(keys_only=True)
        for i in keys:
            entry = i.get()
            if(entry.exists==False):
                entry.key.delete()
        ridirect(self,"/view",self.request.get('session'))
class Delete3(webapp2.RequestHandler):
    def post(self):
        j=0
        keys = users.query().fetch(keys_only=True)
        for i in keys:
            entry = i.get()
            j=j+1
            if(self.request.get(str(j))=='on'):
                entry.exists=False
                entry.put()
        #garbage collection
        keys = users.query().fetch(keys_only=True)
        for i in keys:
            entry = i.get()
            if(entry.exists==False):
                entry.key.delete()
        ridirect(self,"/admin",self.request.get('session'))
class ava(webapp2.RequestHandler):
    def post(self):
        keys = available.query().fetch(keys_only=True)
        for i in keys:
            entry = i.get()
            if(entry.username==ndb.Key(sessions,self.request.get('session')).get().username and entry.date==self.request.get('datepicker')):
                entry.key.delete()
        for i in range(1,48):
            if(self.request.get(str(30*60*i))=='on'):
                avail=available()
                avail.username=ndb.Key(sessions,self.request.get('session')).get().username
                mydate=self.request.get('datepicker')
                avail.date=mydate
                avail.seconds=30*60*i
                avail.put()
        ridirect(self,"/view2",self.request.get('session')) 
class promote(webapp2.RequestHandler):
    def post(self):
        j=0
        keys = users.query().fetch(keys_only=True)
        for i in keys:
            if(i.get().role!='admins'):
                entry = i.get()
                j=j+1
                if(self.request.get(str(j))=='on'):
                    if(self.request.get('Role'+str(j))=='Teacher'):
                        entry.role='teachers'
                        entry.put()
                    elif(self.request.get('Role'+str(j))=='Student'):
                        entry.role='students'
                        entry.put()
                    elif(self.request.get('Role'+str(j))=='Admin'):
                        entry.role='admins'
                        entry.put()
        ridirect(self,"/admin",self.request.get('session'))
class mainselect(webapp2.RequestHandler):
    def post(self):
        stuff="<textarea rows = '5' cols = '30' readonly>"
        value=json.loads(self.request.body)
        if(value=='default'):
            stuff="<textarea rows = '5' cols = '30' readonly></textarea><textarea rows = '5' cols = '30' readonly></textarea></br></br>"
            self.response.write(json.dumps(stuff))
        else:
            if(ndb.Key(potw,value).get()!=None):
                stuff=stuff+ndb.Key(potw,value).get().potw
            stuff=stuff+"</textarea><textarea rows = '5' cols = '30' readonly>"
            if(ndb.Key(availability,value).get()!=None):
                stuff=stuff+ndb.Key(availability,value).get().potw
            stuff=stuff+"</textarea>"
            self.response.write(json.dumps(stuff+"</br></br>"))
class mainselect2(webapp2.RequestHandler):
    def post(self):
        stuff="<textarea rows = '5' cols = '30' readonly>"
        value=json.loads(self.request.body)
        if(value=='default'):
            stuff="<textarea rows = '5' cols = '30' readonly></textarea></br></br>"
            self.response.write(json.dumps(stuff))
        else:
            if(ndb.Key(potw,value).get()!=None):
                stuff=stuff+ndb.Key(potw,value).get().potw
            stuff=stuff+"</textarea>"
            self.response.write(json.dumps(stuff+"</br></br>"))            
class date(webapp2.RequestHandler):
    def post(self):
        value=json.loads(self.request.body)
        username=value.get('name')
        now=value.get('date')
        keys = available.query().fetch(keys_only=True)
        secondvalues=[]
        for i in keys:
            avail=i.get()
            if (now==avail.date and avail.username==username):
                secondvalues.append(str(avail.seconds))
        output="<table><tr><th><th>Time Slot<th><th>Time Slot"
        fifteen=datetime.timedelta(minutes=30)
        for i in range(1,25):
            yes1=False
            yes2=False
            if(str(i*fifteen.seconds) in secondvalues):
                yes1=True
            if(str((i+24)*fifteen.seconds) in secondvalues):
                yes2=True
            if(yes1==True and yes2==True):
                output=output+"<tr><td><input type='checkbox' name='"+str(i*fifteen.seconds)+"' value='on' checked><td>"+str(((i-1)*fifteen.seconds)/3600)+":"+str((((i-1)*fifteen.seconds)/60)%60).zfill(2)+"-"+str((i*fifteen.seconds)/3600)+":"+str(((i*fifteen.seconds)/60)%60).zfill(2)+"<td><input type='checkbox' name='"+str((i+24)*fifteen.seconds)+"' value='on' checked><td>"+str(((i+23)*fifteen.seconds)/3600)+":"+str((((i+23)*fifteen.seconds)/60)%60).zfill(2)+"-"+str(((i+24)*fifteen.seconds)/3600)+":"+str((((i+24)*fifteen.seconds)/60)%60).zfill(2)
            if(yes1==True and yes2==False):
                output=output+"<tr><td><input type='checkbox' name='"+str(i*fifteen.seconds)+"' value='on' checked><td>"+str(((i-1)*fifteen.seconds)/3600)+":"+str((((i-1)*fifteen.seconds)/60)%60).zfill(2)+"-"+str((i*fifteen.seconds)/3600)+":"+str(((i*fifteen.seconds)/60)%60).zfill(2)+"<td><input type='checkbox' name='"+str((i+24)*fifteen.seconds)+"' value='on'><td>"+str(((i+23)*fifteen.seconds)/3600)+":"+str((((i+23)*fifteen.seconds)/60)%60).zfill(2)+"-"+str(((i+24)*fifteen.seconds)/3600)+":"+str((((i+24)*fifteen.seconds)/60)%60).zfill(2)
            if(yes1==False and yes2==True):
                output=output+"<tr><td><input type='checkbox' name='"+str(i*fifteen.seconds)+"' value='on'><td>"+str(((i-1)*fifteen.seconds)/3600)+":"+str((((i-1)*fifteen.seconds)/60)%60).zfill(2)+"-"+str((i*fifteen.seconds)/3600)+":"+str(((i*fifteen.seconds)/60)%60).zfill(2)+"<td><input type='checkbox' name='"+str((i+24)*fifteen.seconds)+"' value='on' checked><td>"+str(((i+23)*fifteen.seconds)/3600)+":"+str((((i+23)*fifteen.seconds)/60)%60).zfill(2)+"-"+str(((i+24)*fifteen.seconds)/3600)+":"+str((((i+24)*fifteen.seconds)/60)%60).zfill(2)
            if(yes1==False and yes2==False):
                output=output+"<tr><td><input type='checkbox' name='"+str(i*fifteen.seconds)+"' value='on'><td>"+str(((i-1)*fifteen.seconds)/3600)+":"+str((((i-1)*fifteen.seconds)/60)%60).zfill(2)+"-"+str((i*fifteen.seconds)/3600)+":"+str(((i*fifteen.seconds)/60)%60).zfill(2)+"<td><input type='checkbox' name='"+str((i+24)*fifteen.seconds)+"' value='on'><td>"+str(((i+23)*fifteen.seconds)/3600)+":"+str((((i+23)*fifteen.seconds)/60)%60).zfill(2)+"-"+str(((i+24)*fifteen.seconds)/3600)+":"+str((((i+24)*fifteen.seconds)/60)%60).zfill(2)       
        output=output+"</table>"
        self.response.write(json.dumps(output))
class student(webapp2.RequestHandler):
    def post(self):
        value=json.loads(self.request.body)
        username=value.get('name')
        now=value.get('date')
        keys = available.query().fetch(keys_only=True)
        secondvalues=[]
        for i in keys:
            avail=i.get()
            if (now==avail.date and avail.username==username):
                secondvalues.append(str(avail.seconds))
        output="<table><tr><th><th>Time Slot"
        fifteen=datetime.timedelta(minutes=30)
        for i in range(1,48):
            if(str(i*fifteen.seconds) in secondvalues):
                output=output+"<tr><td><input type='radio' name='timestamps' value='"+str(i*fifteen.seconds)+"'><td>"+str(((i-1)*fifteen.seconds)/3600)+":"+str((((i-1)*fifteen.seconds)/60)%60).zfill(2)+"-"+str((i*fifteen.seconds)/3600)+":"+str(((i*fifteen.seconds)/60)%60).zfill(2)
        output=output+"</table>"
        self.response.write(json.dumps(output))
app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/POTW', Guestbook2),
    ('/POTW2', Guestbook2),
    ('/done', Done),
    ('/done2', Done2),
    ('/view',Display2),
    ('/view2',Display2),
    ('/handler',Handler),
    ('/404',Construction),
    ('/processing',Putter),
    ('/processing2',Putter2),
    ('/handlesignup',Signuphandler),
    ('/signup',Signup),
    ('/handleteach',Handleteach),
    ('/handleteach2',Handleteach2),
    ('/resolve',Resolverequest),
    ('/unresolve',Unresolverequest),
    ('/delete1',Delete1),
    ('/delete2',Delete2),
    ('/delete3',Delete3),
    ('/admin',adminconsole),
    ('/promote',promote),
    ('/ajax/mainselect',mainselect),
    ('/ajax/mainselect2',mainselect2),
    ('/ajax/date',date),
    ('/ajax/student',student),
    ('/ava',ava)
])
