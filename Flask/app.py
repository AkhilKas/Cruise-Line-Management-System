from flask import *
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.schema import Sequence
app = Flask(__name__, static_url_path='/static') #referencing this while
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///App.sqlite3'
app.config['SECRET_KEY'] = "secret key"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Destination(db.Model):
    __tablename__ = "Destination"
    DID = db.Column(db.Integer,primary_key=True,autoincrement=True)
    Pincode = db.Column(db.Integer)
    dod = db.Column(db.String(30))
    doa = db.Column(db.String(30))
    city = db.Column(db.String(50))
    def __init__(self,pin,dod,doa,city):
        self.Pincode=pin
        self.dod=dod
        self.doa=doa
        self.city=city

class Passenger(db.Model):
    __tablename__ = "Passenger"
    PID = db.Column(db.Integer,primary_key=True,autoincrement=True)
    fname = db.Column(db.String(30))
    lname = db.Column(db.String(30))
    noc = db.Column(db.Integer)
    noa = db.Column(db.Integer)
    address = db.Column(db.String(50))
    dob = db.Column(db.String(30))
    DID = db.Column(db.Integer, db.ForeignKey('Destination.DID'))
    Destination = db.relationship("Destination", backref=db.backref("Destination", uselist=False))
    def __init__(self,fname,lname,noc,noa,address,dob,did):
        self.fname=fname
        self.lname=lname
        self.noc=noc
        self.noa=noa
        self.address=address
        self.dob=dob
        self.DID=did

class PassengerMobileNumber(db.Model):
    __tablename__ = 'PassengerMobileNumber'
    id = db.Column(db.Integer, primary_key=True)
    PID = db.Column(db.Integer,db.ForeignKey('Passenger.PID'))
    MobileNumber=db.Column(db.Integer)
    __table_args__ = ( db.UniqueConstraint('PID','MobileNumber'), )
    def __init__(self,pid,phnno):
        self.MobileNumber=phnno
        self.PID=pid

class PassengerDestination(db.Model):
    __tablename__ = 'PassengerDestination'
    id = db.Column(db.Integer, primary_key=True)
    PID = db.Column(db.Integer,db.ForeignKey('Passenger.PID'))
    DID = db.Column(db.Integer,db.ForeignKey('Destination.DID'))
    __table_args__ = ( db.UniqueConstraint('PID','DID'), )
    def __init__(self,pid,did):
        self.DID=did
        self.PID=pid

class Transaction(db.Model):
    __tablename__ = "Transaction"
    TransID = db.Column(db.Integer,primary_key=True,autoincrement=True)
    Amount = db.Column(db.Integer)
    PaymentMode = db.Column(db.String(30))
    PID=db.Column(db.Integer, db.ForeignKey('Passenger.PID'))
    Passenger = db.relationship("Passenger", backref=db.backref("Passenger", uselist=False))
    def __init__(self,Amount,PaymentMode,pid):
        self.Amount=Amount
        self.PaymentMode=PaymentMode
        self.PID=pid

class Room(db.Model):
    __tablename__ = "Room"
    ROOM_NUMBER = db.Column(db.Integer,primary_key=True)
    status = db.Column(db.String(20))
    roomtype = db.Column(db.String(20))
    PID = db.Column(db.Integer,db.ForeignKey('Passenger.PID'))
    def __init__(self,roomtype,Passenger_ID):
        self.status="Occupied"
        self.roomtype=roomtype
        self.PID=Passenger_ID

class Restaurant(db.Model):
    __tablename__="Restaurant"
    Rest_ID = db.Column(db.String(30),primary_key=True)
    No_of_tables = db.Column(db.Integer)
    Cuisine = db.Column(db.String(30))
    def __init__(self,Restid,c):
        self.Rest_ID=Restid
        self.Cuisine=c
        self.No_of_tables=50

class Table(db.Model):
    __tablename__="Table"
    S_No = db.Column(db.Integer,primary_key=True)
    Table_Number = db.Column(db.Integer,nullable=False)
    Rest_ID = db.Column(db.Integer,db.ForeignKey('Restaurant.Rest_ID'),nullable=False)
    People_per_table = db.Column(db.Integer)
    Tstatus = db.Column(db.String(30),default="Vacant")
    PID = db.Column(db.Integer,db.ForeignKey('Passenger.PID'))
    __table_args__ = ( db.UniqueConstraint('Table_Number','Rest_ID'), )
    def __init__(self,id,ppt,pid):
        self.PID=pid
        self.Rest_ID=id
        self.People_per_table=ppt


@app.route('/Destination.html', methods=['POST',"GET"])
def destination():
    return render_template("Destination.html")

@app.route('/Login.html',methods=["POST","GET"])
def login():
    return render_template("Login.html")

@app.route('/Restaurants.html')
def restaurant():
    return render_template("Restaurants.html")

@app.route('/Restaurants1.html')
def Create():
    rest1=Restaurant("ShangPalace","Chinese")
    db.session.add(rest1)
    rest2=Restaurant("LosLobos","Italian")
    db.session.add(rest2)
    rest3=Restaurant("SpiceCrossing","Mexican")
    db.session.add(rest3)
    rest4=Restaurant("LaCucina","Thai")
    db.session.add(rest4)
    rest5=Restaurant("FoodRepublic","Indian")
    db.session.add(rest5)
    db.session.commit()
    return "<h1>Added successfully<h1>"


@app.route('/')
def home_page():
    return render_template("HomePage.html")

@app.route('/About.html')
def about():
    return render_template("About.html")

@app.route('/Casino.html')
def casino():
    return render_template("Casino.html")

@app.route('/CruiseActivities.html')
def cruise_activities():
    return render_template("CruiseActivities.html")

@app.route('/Entertainment.html')
def entertainment():
    return render_template("Entertainment.html")

@app.route('/Fitness.html')
def fitness():
    return render_template("Fitness.html")

@app.route('/index.html')
def index():
    return render_template("index.html")

@app.route('/RestaurantsFoodRepublic.html')
def food_republic():
    return render_template("RestaurantsFoodRepublic.html")

@app.route('/RestaurantsLaCucina.html')
def la_cucina():
    return render_template("RestaurantsLaCucina.html")

@app.route('/RestaurantsLosLobos.html')
def los_lobos():
    return render_template("RestaurantsLosLobos.html")

@app.route('/RestaurantsShangPalace.html')
def shang_palace():
    return render_template("RestaurantsShangPalace.html")

@app.route('/RestaurantsSpiceCrossing.html')
def spice_crossing():
    return render_template("RestaurantsSpiceCrossing.html")

@app.route('/Spa.html')
def spa():
    return render_template("Spa.html")

@app.route('/login', methods = ['POST'])
def login_form():
    Pass_ID=request.form['Pass_ID']
    passenger_obj = db.session.query(Passenger).get(Pass_ID)

    if passenger_obj:
        phn = db.session.query(PassengerMobileNumber).filter_by(PID=passenger_obj.PID).all()

        if len(phn)==1:
            phn1=phn[0].MobileNumber
            phn2="Not entered"

        else:
            phn1=phn[0].MobileNumber
            phn2=phn[1].MobileNumber

        rooms = db.session.query(Room).filter_by(PID=passenger_obj.PID).all()
        rooms_str=""

        for a_room in rooms:
            rooms_str = rooms_str + str(a_room.ROOM_NUMBER) + ","

        trans = db.session.query(Transaction).filter_by(PID=passenger_obj.PID).all()

        return render_template('LoginDisplay.html',psngr=passenger_obj,phn1=phn1,phn2=phn2,room=a_room,rooms_str=rooms_str[0:len(rooms_str)-1],trans_obj=trans[0])

    else:
        return render_template("Warning.html", pid = Pass_ID)

@app.route('/display', methods = ['POST'])
def display():
    dest_obj=Destination(request.form['dest_pin'],request.form['dod'],request.form['doa'],request.form['city'])
    db.session.add(dest_obj)
    db.session.commit()
    passenger_obj=Passenger(request.form['firstname'],request.form['lastname'],request.form['children'],request.form['adults'],request.form['address'],request.form['dob'],dest_obj.DID)
    db.session.add(passenger_obj)
    db.session.commit()
    p_d_obj=PassengerDestination(passenger_obj.PID,dest_obj.DID)
    db.session.add(p_d_obj)
    db.session.commit()
    mob_obj=PassengerMobileNumber(passenger_obj.PID,request.form['phn1'])
    db.session.add(mob_obj)
    db.session.commit()
    mob_obj=PassengerMobileNumber(passenger_obj.PID,request.form['phn2'])
    db.session.add(mob_obj)
    db.session.commit()
    trans_obj=Transaction(request.form['amount'],request.form['payment_mode'],passenger_obj.PID)
    db.session.add(trans_obj)
    db.session.commit()

    no_of_rooms = int(request.form['rooms'])

    for i in range(no_of_rooms):
        room_obj=Room(request.form['roomtype'],passenger_obj.PID)
        db.session.add(room_obj)
        db.session.commit()

    return render_template("Greet.html", obj = passenger_obj)

@app.route('/Restaurant', methods = ['POST'])
def restaurant_booking():
        pid = request.form['PID']
        query_obj = db.session.query(Passenger).get(pid)

        if not query_obj:
            return render_template("Warning.html", pid = pid)

        else:
            query_obj = db.session.query(Restaurant).get(request.form['restaurant'])

            if int(request.form['tables']) > query_obj.No_of_tables:
                return "We don't have "+str(request.form['tables'])+" tables vacant for now. Sorry for the inconvenience"

            else:
                query_obj.No_of_tables -= int(request.form['tables'])

                for i in range(int(request.form['tables'])):
                    table=Table(request.form['restaurant'],request.form['ppt'],pid)
                return str(request.form['tables'])+" tables have been booked for you Mr."+db.session.query(Passenger).get(pid).fname

if __name__ == "__main__":
    db.create_all();
    app.run(debug = True)