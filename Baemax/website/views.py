from flask import Blueprint, render_template , flash , request , jsonify,session,redirect, url_for
from .models import User , Note , Bio , Qualification
from flask_login import login_required,  current_user
from .import db, socketio 
import json
import uuid
import speech_recognition as sr 
import datetime
import subprocess

import pyttsx3
import webbrowser
import pyttsx3
import speech_recognition
from playsound import playsound
#webchat stuff
from flask_socketio import join_room, leave_room , send, SocketIO 
import random
from string import ascii_uppercase

def speak(audio):
     
    engine = pyttsx3.init()
    # getter method(gets the current value
    # of engine property)
    voices = engine.getProperty('voices')
     
    # setter method .[0]=male voice and 
    # [1]=female voice in set Property.
    engine.setProperty('voice', voices[0].id)
     
    # Method for the speaking of the assistant
    engine.say(audio)  
     
    # Blocks while processing all the currently
    # queued commands
    engine.runAndWait()
def Hello():
    # This function is for when the assistant 
    # is called it will say hello and then 
    # take query
    speak("Hi , my name is Baemax your personal social media companion")



views = Blueprint('views',__name__)

@views.route('/')
def home():
    Hello()
    return render_template("index.html")






@views.route('/editbio', methods=['GET', 'POST'])
@login_required
def editbio():
    if request.method == 'POST':
        print(request.form)
        fullname = request.form.get('fullname')
        print(fullname)
        job = request.form.get('job')
        print(job)
        bio = request.form.get('bio')
        biostring = bio
        print(biostring)
        q = request.form.get('q')
        
        if q != None:
            new_q = Qualification(qualification = q, user_id = current_user.id) #error might happen here
            print(new_q)
                
            db.session.add(new_q)
            db.session.commit()
            flash("qualification added", category='success')
            speak("qualification added")
        

        if len(fullname)<1:
            flash("name is too short", category='error')
        elif len(job)>100:
            flash("job is to long", category='error')
        elif len(biostring)>150:
            flash("bio is to long", category='error')
        elif len(fullname)>50:
            flash("name is to long", category='error')
        else:
            
            
            bio = Bio.query.all()
            for i in bio:
            
                print(i.fullname)
                print(i.job)
                print(i.bio)
                print(i.user_id)
                print("<------------>")
            users = Bio.query.filter_by(user_id=current_user.id) 
            if Bio.query.filter_by(user_id=current_user.id):
                print("True")
                for i in users:
                    i.fullname = fullname
                    db.session.commit()
                    i.job = job
                    db.session.commit()
                    i.bio = biostring
                    db.session.commit()
                    print(i.fullname)
                    print(i.job)
                    print(i.bio)
            
            


            print("wendy zhang")
                
            
            
            
            
            return render_template("editbio.html", user= current_user , bio =biostring , job =job , fullname = fullname)



    return render_template("editbio.html", user= current_user )
    

@views.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note)<1:
            flash("note is too short", category='error')
        else:
            new_note = Note(data = note, user_id= current_user.id)
            print(new_note)
            db.session.add(new_note)
            db.session.commit()
            flash("note added", category='success')

    return render_template("dashboard.html" , user =current_user)

@views.route('/delete-note', methods=['POST'])
def delete_note():
    # Look for noteId that was passed to the function
    # from the deleteNote function in index.js
    # json.loads(request.data) - creates a Python dictionary object.
    note = json.loads(request.data)
    print(note)
    # Access the field noteID
    noteId = note['noteId']
    print(noteId)
    # Find the note from it's note ID
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})

     
    
        

    




@views.route('/study')
@login_required
def study():
    
    
    return render_template("study.html",user =current_user)
    
rooms = {"0": None,"1": None}
clientsinR = []
l_dict = []

@views.route('/resultofsearch', methods=['GET','POST'])
@login_required
def resultofsearch():
    q = request.args.get("q")
    
   
    print("hi")
    if q:
        results =Bio.query.filter(Bio.fullname.icontains(q)).limit(20).all()
        qual =Qualification.query.all()
        for i in results:
            for j in qual:
                if j.user_id == i.user_id:
                    print(j.qualification)
                    print(j.user_id)
            print(i.fullname)
            print(i.user_id)
         
              
        return render_template("resultofsearch.html", user=current_user, results = results , qual = qual)
        
    else:
        results =[]
        qual = []
        print("none")

    return render_template("resultofsearch.html", user=current_user, results = results , qual = qual)
@views.route('/search', methods=['GET','POST'])
@login_required
def search():
    room = session.get("room")
    name = session.get("name")
    users = Bio.query.all() 
    qual = Qualification.query.all()
    
    gen_rand = request.form.get("gen_rand", False)
    
    
            
    if gen_rand != False:
        print("generate_random")
        
        print("generate_random")
        randroom = session.get("randroom")
        
        print(randroom)
        socketio.send({"test":"test recieved", "test2": current_user.username},to=randroom)
        return render_template("room.html", user=current_user, code=str(randroom))
    
        
        
    
    
    return render_template("search.html", user=current_user, code=room, qual =qual , users=users)


def generate_unique_code(length):
    while True:
        code = ""
        for i in range(length):
            code += random.choice(ascii_uppercase)
        
        if code not in rooms: 
            break 
    
    return code


def generate_unique_intcode():
    randnum = uuid.uuid4()

    return(randnum)
@views.route('/room', methods=['GET','POST'])
@login_required
def room():
    room = session.get("room")
    name = session.get("name")
    
    waitingroom = session.get("waitingroom")
    randbtn = session.get("randbtn")
    if waitingroom == True:
        
        return redirect(url_for('views.search',user=current_user, code="waitingroom"))
    if randbtn == True:
        clientsinR.append(current_user.id)
        return render_template("room.html", user=current_user, code="preparing to join...", messages=rooms[room]["messages"])
    if room is None or session.get("name") is None or room not in rooms:
        return redirect(url_for('views.chatroom'))
    return render_template("room.html", user=current_user, code=room, messages=rooms[room]["messages"])


randroomlist = [""]


@socketio.on("connect")
def connect(auth):
    
    room = session.get("room")
    name = session.get("name")
    
    waitingroom = session.get("waitingroom")
    randbtn = session.get("randbtn")
    if room not in rooms:
        leave_room(room)
        return

    join_room(room)
    
    
       
    while randbtn:
        
        if (len(clientsinR)) > 0:
            print("more than 0 users in room")
            print(len(clientsinR))
            if (len(clientsinR) % 2) != 0 or (len(clientsinR)) == 0:
                print("odd")
                randroom = generate_unique_intcode()
                randroomlist.append(str(randroom))
                for i in randroomlist:
                    print(i)
                
                join_room(randroom)
                session["room"] = str(randroom)
                session["name"] = "user1"
                send({"name": str(randroom), "message": current_user.username},to=randroom)
                session["randroom"] = randroom
                print(clientsinR)
                print(f"{current_user.username} joined room: {randroom}")
                
                randbtn = False
                
            else:
                print("even")
                for i in randroomlist:
                    print(i)
                now_room =randroomlist[-1]
                
                
                
                clientsinR.remove(current_user.id)
                print(clientsinR)
                
                join_room(randroomlist[-1])
                send({"name": str(now_room), "message": current_user.username},to=now_room)
                
                print(f"{current_user.username} joined room: {now_room}")
                randroomlist.pop()
                
                randbtn = False

            
                

    
    






    #room just collection of users

    print(f"{name} joined room: {room}")
    send({"name":name, "message": "has entered the room"}, to=room)
    rooms[room]["members"] += 1
    


@socketio.on("disconnect")
def disconnect():#get randbtn
    room = session.get("room")
    name = session.get("name")
    
    waitingroom = session.get("waitingroom")
    
    if current_user.id in clientsinR:
        clientsinR.remove(current_user.id)
        for i in range(len(clientsinR)):
            print(clientsinR[i])


    
    leave_room(room)
    

    users = Bio.query.filter_by(user_id=current_user.id) 
    users.is_online = False  #room just collection of users
    if room in rooms:
        rooms[room]["members"] -=1
        if rooms[room]["members"] <= 0:
            del rooms[room]
    
    send({"name": name, "message": "has left the room"}, to=room)
    speak(f"{name} has left the room {room}")
    print(f"{name} has left the room {room}")


@views.route('/chatroom', methods=['GET','POST'])
@login_required
def chatroom():
    session.clear()
    if request.method=="POST":
        name = request.form.get("name")
        code = request.form.get("code")
        join = request.form.get("join", False)
        create = request.form.get("create", False)
        search = request.form.get("search", False)
        gen_rand = request.form.get("gen_rand", False)
        waitingroom = "waitingroom"
        session["waitingroom"] = False
        session["randbtn"] = False
        if not name:
            name = current_user.username
        if join != False and not code:
            return render_template("chatroom.html", error="Please enter a room code",code=code, name=name, user =current_user)
        room = code

        
        if search != False:
            session["waitingroom"] = True
            room = 0
            rooms[room] = {"members": 0 , "messages": [] }
            
    
            #return redirect(url_for('views.search'))
        elif gen_rand != False:
            room = "prepping...."
            rooms[room] = {"members": 0 , "messages": [] }
            session["randbtn"] = True
        elif create != False:
            room = generate_unique_code(4)
            rooms[room] = {"members": 0 , "messages": []} #where chat data stored

        elif code not in rooms:
            return render_template("chatroom.html", error="room doesnt exist",code=code,name=name ,user =current_user)

        
        session["room"] = room
        session["name"] = name #like cookies might make permanent chats
        
        
        return redirect(url_for('views.room'))
    
    return render_template("chatroom.html",user =current_user)







   
