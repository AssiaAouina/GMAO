
from email.mime import image
from lib2to3.pgen2.token import STRING
from re import template
from sqlite3.dbapi2 import Cursor, Row
import string
from types import MethodDescriptorType

from flask import Flask, render_template,request,flash,redirect,url_for,session,jsonify,json
import sqlite3
from functools import wraps
import os
from flask_wtf.file import FileField, FileSize
from wtforms import SubmitField
import requests,os
# from werkzeug.utils import secure_filename
import urllib.request
from datetime import datetime
import calendar
from psycopg2._psycopg import connection
# from datetime import  datetime
#from resizeimage import resizeimage
# import glob
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gmao.db'

  
app=Flask(__name__,template_folder='appflask/templates')
app.secret_key="123"
con=sqlite3.connect("gmao.db")
app.config['UPLOAD_FOLDER']="static\css\img"

#con.execute("create table if not exists utilisateur(e_maile text ,password text )")
#con.execute("create table if not exists customer(pid integer primary key,name text,address text,contact integer,mail text)")
cur = con.cursor()
cur.execute('SELECT * FROM utilisateur')

print(cur.fetchall())
# con.commit()
# con.close()
#con.execute("create table if not exists customer(pid integer primary key,name text,address text,contact integer,mail text)")
#con.close()

# app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gmao.db'
# db=SQLAlchemy(app)
#login_manager = LoginManager()

#app = Flask(__name__)
# class LoginForm(FlaskForm):
#     email = StringField('email', validators=[InputRequired(), Length(min=4, max=40)])
#     password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
# @app.route('/')
# def index():
#     return render_template('index.html')
# @app.route('/', methods=['GET', 'POST'])
# def index():
#     form = Form()
#     form.country.choices = [(country.id, country.name) for country in Country.query.all()]





@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/')

def index():
    return render_template('index.html')


def get_db_connection():
    conn = sqlite3.connect('gmao.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/login',methods=["GET","POST"])

def login():
    if request.method=='POST':
        e_maile=request.form['e_maile']
        password=request.form['password']
        con=sqlite3.connect("gmao.db")
        con.row_factory=sqlite3.Row
        cur=con.cursor()

        cur.execute("select * from utilisateur where e_maile=? and password=?",(e_maile,password))
        data=cur.fetchone()

        if data:
            session["e_maile"]=data["e_maile"]
            session["password"]=data["password"]
            session['logged_in']=True
            return redirect("dashboard")
        else:
            flash("Please check your login details and try again!")
    return redirect(url_for("index"))


ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
@app.route('/equipement', methods=['POST', 'GET'])
def equipement():
    
   
    conn = get_db_connection()
    
    posts = conn.execute('SELECT  id_eq,code_Equipement,DESIGNATION,Marque,N_de_série,Date_d_acquisition,état,Remarque,type,image FROM Equipement').fetchall()
 
    # items=conn.execute('SELECT * FROM Equipement where id_eq= ?', [id_eq], one=True)
    # if items is None:
    #     print('No such user')
    # else:
    #     print('id_eq',items['id_eq'])
 
    return render_template('equipement.html', posts=posts)
@app.route('/intervenant', methods=['POST', 'GET'])
def intervenant():

    conn = get_db_connection()
     
   
    posts = conn.execute('SELECT id, name,contact,email FROM inter').fetchall()
    conn.close()
    return render_template('intervenant.html', posts=posts)
@app.route('/intervention', methods=['POST', 'GET'])

def intervention():

    conn = get_db_connection()
     
   
    posts = conn.execute('SELECT id, N_fiche_intervention,cd_eq,n_intervenant, id_Intervenant,Date_d_anomalie,date_intervention, organ,Nature_de_panne,Cause_de_panne,Date_de_mise_en_service,Temps_d_arrêt FROM intervention').fetchall()
    conn.close()
    return render_template('intervention.html', posts=posts)
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))
    return wrap
    
@app.route('/dashboard',methods=["GET","POST"])
@is_logged_in
def dashboard():

  return render_template('dashboard.html')
  
def utilisateur():
    return render_template("dashboard.html")

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
  
@app.route('/addequipement', methods=['GET', 'POST'])
@is_logged_in
def add_equipement():
    conn = get_db_connection()
    if request.method == 'POST':
       
        code_Equipement = request.form["code_Equipement"] 
        DESIGNATION = request.form["DESIGNATION"] 
        Marque =request.form["Marque"] 
        N_de_série = request.form["N_de_série"] 
        Date_d_acquisition = request.form["Date_d_acquisition"] 
        état = request.form["état"] 
        Remarque = request.form["Remarque"] 
        type = request.form["type"]
        image=request.files['image']

        if image.filename!='':
            filepath=os.path.join(app.config['UPLOAD_FOLDER'],image.filename)
            image.save(filepath)
        conn.execute("INSERT INTO Equipement ( code_Equipement,DESIGNATION,Marque ,N_de_série ,Date_d_acquisition ,état ,Remarque ,type,image ) VALUES ( ?,?,?,?,?,?,?,?,?)",( code_Equipement,DESIGNATION,Marque ,N_de_série ,Date_d_acquisition ,état ,Remarque ,type,image.filename))
        
        conn.commit()
        flash('equipement Created', 'success')
        return redirect(url_for('equipement'))
    return render_template('addequipement.html', )
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    
@app.route('/editequipement/<code_Equipement>', methods = ['POST', 'GET'])
@is_logged_in
def get_Equipement(code_Equipement):
    conn = get_db_connection()
    cur=conn.cursor()
    cur.execute('SELECT * FROM Equipement WHERE code_Equipement = ?', (code_Equipement,))
    post = cur.fetchall()
    cur.close()
    print(post[0])
    return render_template('editequipement.html', Equipement = post[0])

@app.route('/up/<code_Equipement>', methods=['POST'])
@is_logged_in
def update_equipement(code_Equipement):
    conn = get_db_connection()
    if request.method == 'POST':
    
        DESIGNATION = request.form["DESIGNATION"] 
        Marque =request.form["Marque"] 
        N_de_série = request.form["N_de_série"] 
        Date_d_acquisition = request.form["Date_d_acquisition"] 
        état = request.form["état"] 
        Remarque = request.form["Remarque"] 
        type = request.form["type"] 
        image=request.files['image']

        if image.filename!='':
            filepath=os.path.join(app.config['UPLOAD_FOLDER'],image.filename)
            image.save(filepath) 
      
      
        cur=conn.cursor()
        cur.execute("""
            UPDATE Equipement
            SET DESIGNATION = ?,
                Marque = ?,
                N_de_série = ?,
                Date_d_acquisition=?,
                état =?,
                Remarque=?,
                type=?,
                image=?
            WHERE code_Equipement =?
        """, ( DESIGNATION,Marque ,N_de_série ,Date_d_acquisition ,état ,Remarque ,type,image.filename,code_Equipement ))
        conn.commit()
        return redirect(url_for('equipement'))
@app.route('/delete/<code_Equipement>', methods = ['POST','GET'])
@is_logged_in
def delete_equipement(code_Equipement):
    conn = get_db_connection()
    con.row_factory=sqlite3.Row
    cur=conn.cursor()
    code_Equipement=str(code_Equipement)
    cur.execute('DELETE FROM Equipement WHERE code_Equipement = ?' ,(code_Equipement,))
    conn.commit()
    rows =cur.fetchone()
    flash('Equipement Removed Successfully')
    return redirect(url_for('equipement'))
    
      

  
@app.route('/addintervention', methods=['GET', 'POST'])
@is_logged_in
def add_intervention():
    if request.method == 'POST':
        conn = get_db_connection()
        id=request.form["id"]
        N_fiche_intervention =request.form["N_fiche_intervention"] 
        cd_eq = request.form["cd_eq"] 
        Date_d_anomalie = request.form["Date_d_anomalie"] 
        n_intervenant = request.form["n_intervenant"] 
        id_Intervenant = request.form["id_Intervenant"] 
        date_intervention = request.form["date_intervention"] 
        organ = request.form["organ"] 
        Nature_de_panne = request.form["Nature_de_panne"] 
        Cause_de_panne = request.form["Cause_de_panne"] 
        Date_de_mise_en_service = request.form["Date_de_mise_en_service"]
        Temps_d_arrêt = request.form["Temps_d_arrêt"]
        
     
        conn.execute("INSERT INTO intervention ( id, N_fiche_intervention , cd_eq ,n_intervenant ,id_Intervenant ,Date_d_anomalie ,date_intervention ,organ,Nature_de_panne,Cause_de_panne,Date_de_mise_en_service,Temps_d_arrêt) VALUES (?, ?,?,?,?,?,?,?,?,?,?,?)",(id,N_fiche_intervention,cd_eq ,n_intervenant ,id_Intervenant ,Date_d_anomalie ,date_intervention ,organ,Nature_de_panne,Cause_de_panne,Date_de_mise_en_service,Temps_d_arrêt))
        
        conn.commit()

       
        flash('intervention Created', 'success')
        return redirect(url_for('intervention'))
       

    return render_template('addintervention.html', )


@app.route('/editintervention/<id>', methods = ['POST', 'GET'])
@is_logged_in
def get_intervention(id):
    conn = get_db_connection()
    cur=conn.cursor()
   
    cur.execute('SELECT * FROM intervention WHERE id = ?', (id,))
    
    posts = cur.fetchall()
    cur.close()
    
    print(posts[0])
    return render_template('editintervention.html', intervention = posts[0])

@app.route('/update/<id>', methods=['POST'])
@is_logged_in
def update_intervention(id):
    conn = get_db_connection()
    if request.method == 'POST':
        
        id =request.form["id"] 
        N_fiche_intervention =request.form["N_fiche_intervention"] 
        cd_eq = request.form["cd_eq"] 
        n_intervenant = request.form["n_intervenant"] 
        id_Intervenant = request.form["id_Intervenant"]
        Date_d_anomalie = request.form["Date_d_anomalie"] 
         
        date_intervention = request.form["date_intervention"] 
        organ = request.form["organ"] 
        Nature_de_panne = request.form["Nature_de_panne"] 
        Cause_de_panne = request.form["Cause_de_panne"] 
        Date_de_mise_en_service = request.form["Date_de_mise_en_service"]
        Temps_d_arrêt = request.form["Temps_d_arrêt"]
       
        cur=conn.cursor()
        cur.execute ("UPDATE intervention SET    N_fiche_intervention=?,cd_eq = ?,n_intervenant = ?,id_Intervenant =?,Date_d_anomalie=?,date_intervention=?,organ = ?,Nature_de_panne = ?,Cause_de_panne=?,Date_de_mise_en_service =?,Temps_d_arrêt=? WHERE id=?" ,(N_fiche_intervention,cd_eq,n_intervenant,id_Intervenant, Date_d_anomalie,date_intervention,organ,Nature_de_panne,Cause_de_panne,Date_de_mise_en_service,Temps_d_arrêt,id))
        conn.commit()
        flash('intervention Updated Successfully')
        return redirect(url_for('intervention'))
@app.route('/remove/<id>', methods = ['POST','GET'])
@is_logged_in
def remove_intervention(id):
    conn = get_db_connection()
    con.row_factory=sqlite3.Row
    cur=conn.cursor()
    id=str(id)
    cur.execute('DELETE  FROM intervention WHERE id = ?', (id,))
    conn.commit()
    rows =cur.fetchone()
    flash('intervention Removed Successfully')
    return redirect(url_for('intervention'))
@app.route('/addintervenant', methods=['GET', 'POST'])
@is_logged_in
def add_intervenant():
    if request.method == 'POST':
        conn = get_db_connection()
      
        id =request.form["id"] 
        name = request.form["name"] 
        contact = request.form["contact"] 
        email = request.form["email"] 
     
        
     
        conn.execute("INSERT INTO inter ( id, name , contact , email ) VALUES (?, ?,?,?)",(id,name,contact ,email ))
        
        conn.commit()

       
        flash('intervenant Created', 'success')
        return redirect(url_for('intervenant'))
       

    return render_template('addintervenant.html', )
    
@app.route('/editintervenant/<id>', methods = ['POST', 'GET'])
@is_logged_in
def get_intervenant(id):
    conn = get_db_connection()
    cur=conn.cursor()
   
    cur.execute('SELECT * FROM inter WHERE id = ?', (id,))
    
    posts = cur.fetchall()
    cur.close()
    
    print(posts[0])
    return render_template('editintervenant.html', intervenant = posts[0])

@app.route('/renovate/<id>', methods=['POST'])
@is_logged_in
def renovate_intervention(id):
   
    if request.method == 'POST':
        
        
        
        name = request.form["name"] 
        contact = request.form["contact"] 
        email = request.form["email"] 
     
       
        conn = get_db_connection()
       
        cur=conn.cursor()
        cur.execute ("UPDATE inter SET   name = ?, contact = ?, email =?  WHERE  id=? " ,(name ,contact,email,id))
        conn.commit()
       

        
        
        flash('intervenant Updated Successfully')
        return redirect(url_for('intervenant'))
    
@app.route('/cut_out/<id>', methods = ['POST','GET'])
@is_logged_in
def cut_out_intervenant(id):
    conn = get_db_connection()
    con.row_factory=sqlite3.Row
    cur=conn.cursor()
    id=str(id)
    cur.execute('DELETE  FROM inter WHERE id = ?', (id,))
    conn.commit()
    rows =cur.fetchone()
    flash('intervenant Removed Successfully')
    return redirect(url_for('intervenant'))
# @app.route("/view")
# def view():    
#     con = sqlite3.connect("gmao.db")
#     con.row_factory = sqlite3.Row
#     cur = con.cursor()
#     cur.execute("select * from Equipement")   
#     rows = cur.fetchall()
#     return render_template("view.html",rows = rows,) 

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
@app.route("/view/<code_Equipement>",methods=['GET','POST'])
@is_logged_in
def view(code_Equipement):
    
        items=get_Equipement(code_Equipement)
        con = sqlite3.connect("gmao.db")
        con.row_factory = sqlite3.Row
        cur = con.cursor()
 
        
        posts=cur.execute('Select code_Equipement ,DESIGNATION,Marque,N_de_série,Date_d_acquisition,état,Remarque,type,image FROM Equipement where code_Equipement=?', (code_Equipement,))
        EQPOSTS = cur.fetchall()
        posts = []
      
        for rs in EQPOSTS:
            posts_dict = {
                     'code_Equipement': rs['code_Equipement'],
                     'DESIGNATION': rs['DESIGNATION'],
                     'Marque': rs['Marque'],
                     'N_de_série': rs['N_de_série'],
                     'Date_d_acquisition': rs['Date_d_acquisition'],
                     'N_de_série': rs['N_de_série'],
                     'Date_d_acquisition': rs['Date_d_acquisition'],
                     'état': rs['état'],
                     'Remarque': rs['Remarque'],
                     'type': rs['type'],
                     'image': rs['image'] }
            posts.append(posts_dict) 
      
        return json.dumps(posts,)
            
            
@app.route("/viewinter/<id>",methods=['GET','POST'])
@is_logged_in
def view_intervention(id):
   
            items=get_intervention(id)
            con = sqlite3.connect("gmao.db")
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            posts=cur.execute('SELECT id, N_fiche_intervention,cd_eq,n_intervenant, id_Intervenant,Date_d_anomalie,date_intervention, organ,Nature_de_panne,Cause_de_panne,Date_de_mise_en_service,Temps_d_arrêt FROM intervention where id=?',(id,))
            inter = cur.fetchall()
            posts = []
      
            for rs in inter:
                posts_dict = {
                     'id': rs['id'],
                     'N_fiche_intervention': rs['N_fiche_intervention'],
                     'cd_eq': rs['cd_eq'],
                     'n_intervenant': rs['n_intervenant'],
                     'id_Intervenant': rs['id_Intervenant'],
                     'Date_d_anomalie': rs['Date_d_anomalie'],
                     'Date_d_acquisition': rs['Date_d_acquisition'],
                     'date_intervention': rs['date_intervention'],
                     'organ': rs['organ'],
                     'Nature_de_panne': rs['Nature_de_panne'],
                     'Cause_de_panne': rs['Cause_de_panne'] ,
                     'Date_de_mise_en_service': rs['Date_de_mise_en_service'],
                     'Temps_d_arrêt': rs['Temps_d_arrêt']}
                posts.append(posts_dict) 
      
                return json.dumps(posts,)
           
                
@app.route("/SELECT/<id>",methods=['GET','POST'])
@is_logged_in
def select_intervention(id):
   
   
            items=get_intervention(id)
            con = sqlite3.connect("gmao.db")
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            employee=cur.execute('SELECT id, N_fiche_intervention,cd_eq,n_intervenant, id_Intervenant,Date_d_anomalie,date_intervention, organ,Nature_de_panne,Cause_de_panne,Date_de_mise_en_service,Temps_d_arrêt FROM intervention where id=?',(id,))
            inter = cur.fetchall()
            employee = []
      
            for rs in inter:
               employee_dict = {
                     'id': rs['id'],
                     'N_fiche_intervention': rs['N_fiche_intervention'],
                     'cd_eq': rs['cd_eq'],
                     'n_intervenant': rs['n_intervenant'],
                     'id_Intervenant': rs['id_Intervenant'],
                    
                     'date_intervention': rs['date_intervention'],
                     'organ': rs['organ'],
               }
            employee.append(employee_dict) 
      
            return json.dumps(employee,)
@app.route('/PDR', methods=['POST', 'GET'])
@is_logged_in
def PDR():

    conn = get_db_connection()
     
   
    posts = conn.execute('SELECT id, Nom,Réf,Qt, Marque,Etat FROM PDR').fetchall()
    conn.close()
    return render_template('PDR.html', posts=posts)
@app.route('/addPDR', methods=['GET', 'POST'])
@is_logged_in
def add_PDR():
    if request.method == 'POST':
        conn = get_db_connection()
        id =request.form["id"] 
        Nom=  request.form["Nom"]
        Réf=  request.form["Réf"]
        Qt=  request.form["Qt"]
        Marque=  request.form["Marque"]
        Etat=  request.form["Etat"]


        conn.execute("INSERT INTO PDR (  id, Nom,Réf,Qt, Marque,Etat ) VALUES (?, ?,?,?,?,?)",( id, Nom,Réf,Qt, Marque,Etat))
        
        conn.commit()
        flash('PDR Add', 'success')
        return redirect(url_for('PDR'))
    return render_template('AddPDR.html', )
@app.route('/editPDR/<id>', methods = ['POST', 'GET'])
@is_logged_in
def get_PDR(id):
    conn = get_db_connection()
    cur=conn.cursor()
   
    cur.execute('SELECT * FROM PDR WHERE id = ?', (id,))
    
    posts = cur.fetchall()
    cur.close()
    
    print(posts[0])
    return render_template('editPDR.html', PDR = posts[0])
@app.route('/reno/<id>', methods=['POST'])
@is_logged_in
def renovate_PDR(id):
   
    if request.method == 'POST':
        
        
      
        Nom=  request.form["Nom"]
        Réf=  request.form["Réf"]
        Qt=  request.form["Qt"]
        Marque=  request.form["Marque"]
        Etat=  request.form["Etat"]

        conn = get_db_connection()
       
        cur=conn.cursor()
        cur.execute ("UPDATE PDR SET   Nom = ?, Réf =?,Qt =?,Marque =?,Etat =?  WHERE  id=? " ,(  Nom,Réf,Qt, Marque,Etat,id))
        conn.commit()
       

        
        
        flash('PDR Updated Successfully')
        return redirect(url_for('PDR'))


@app.route('/start', methods=["POST"])

def start():

    id = request.form['id']
    Qt = request.form['Qt']
    qt2 = request.form['qt2']
    con = sqlite3.connect("gmao.db")
    con.row_factory = sqlite3.Row
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("UPDATE PDR SET Qt=?,qt2=? WHERE id=?", (Qt,qt2,id,))

    conn.commit()
    return redirect(url_for('PDR',))

@app.route('/sup/<id>', methods = ['POST','GET'])
@is_logged_in
def sup_PDR(id):
    conn = get_db_connection()
    con.row_factory=sqlite3.Row
    cur=conn.cursor()
    id=str(id)
    cur.execute('DELETE  FROM PDR WHERE id = ?', (id,))
    conn.commit()
    rows =cur.fetchone()
    flash('PDR Removed Successfully')
    return redirect(url_for('PDR'))
@app.route("/viewpdr/<id>",methods=['GET','POST'])
@is_logged_in
def select_PDR(id):
   
   
            items= get_PDR(id)
            con = sqlite3.connect("gmao.db")
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            employee=cur.execute('SELECT id, Nom,Réf,Qt, Marque,Etat FROM PDR where id=?',(id,))
            pdr = cur.fetchall()
            pdr = []
      
            for rs in pdr:
               pdr_dict = {
                     'id': rs['id'],
                     'Nom': rs['Nom'],
                     'Réf': rs['Réf'],
                     'Qt': rs['Qt'],
                     'Marque': rs['Marque'],
                    
                     'Etat': rs['Etat'],
                     
               }
            pdr.append(pdr_dict) 
      
            return json.dumps(pdr,)

# @app.route('/add', methods=['GET', "POST"])
# def add():
#     if request.method == 'POST':
#         con = sqlite3.connect("gmao.db")
#         con.row_factory = sqlite3.Row
#         cur = con.cursor()
#         idcal = request.form['idcal']
#         start_event = request.form['start_event']
#         end_event = request.form['end_event']
#         title = request.form['title']
#
#
#
#         con.execute("INSERT INTO events (  idcal, start_event,end_event,title) VALUES (?, ?,?,?)",
#                      (idcal, start_event,end_event,title,))
#         cur.fetchall()
#
#         flash(' Add', 'success')
#
#
#     return render_template("add.html")
 

@app.route('/calendrier')
@is_logged_in
def calendrier():
    con = sqlite3.connect("gmao.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM events ORDER BY idcal")
    calendar = cur.fetchall()
    return render_template("calendrier.html", calendar=calendar)
@app.route("/insert",methods=["POST","GET"])
@is_logged_in
def insert():
    con = sqlite3.connect("gmao.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    if request.method == 'POST':

        start = request.form['start']
        end = request.form['end']
        title = request.form['title']
        print(title)
        print(start)
        cur.execute("INSERT INTO events (start_event,end_event,title) VALUES (?,?,?)",[start,end,title])
        con.commit()
        cur.close()
        msg = 'success'
        flash('intervention à venir dans la date :'+start+'.')
    return jsonify(msg)

@app.route("/updatecal",methods=["POST","GET"])
@is_logged_in
def updatecal():
    con = sqlite3.connect("gmao.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    if request.method == 'POST':
        idcal = request.form['idcal']

        start = request.form['start']
        end = request.form['end']
        title = request.form['title']
        print(title)
        print(start)
        cur.execute("UPDATE events SET  start_event = %s, end_event = %s, title = %s WHERE idcal = %s ", [title, start, end, idcal])
        con.commit()
        cur.close()
        msg = 'success'
    return jsonify(msg)
@app.route("/ajax_delete", methods=["POST", "GET"])
@is_logged_in
def ajax_delete():
    con = sqlite3.connect("gmao.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    if request.method == 'POST':
        getid = request.form['idcal']
        print(getid)
        cur.execute('DELETE FROM events WHERE idcal = {0}'.format(getid))
        con.commit()
        cur.close()
        msg = 'Record deleted successfully'
    return jsonify(msg)


@app.route('/LesTaches', methods=['POST', 'GET'])
@is_logged_in
def LesTaches():
    conn = get_db_connection()

    posts = conn.execute('SELECT ID,title,Details,Equipement,N_PDR,Date,Fréquance,Etat,Rp_d_intervention,ET_pdr FROM LesTaches').fetchall()
    conn.close()
    return render_template('LesTaches.html', posts=posts)

@app.route('/addtache', methods=['GET', 'POST'])
@is_logged_in
def addtache():
    conn = get_db_connection()
    if request.method == 'POST':
        ID = request.form['ID']
        title = request.form['title']
        Details = request.form['Details']
        Equipement = request.form['Equipement']
        N_PDR = request.form['N_PDR']
        Date = request.form['Date']
        Fréquance = request.form['Fréquance']
        Etat = request.form['Etat']
        Rp_d_intervention = request.form['Rp_d_intervention']
        ET_pdr = request.form['ET_pdr']

        conn.execute("INSERT INTO lesTaches (  ID,title,Details,Equipement,N_PDR,Date,Fréquance,Etat,Rp_d_intervention,ET_pdr) VALUES (?, ?,?,?,?,?,?,?,?,?)",
                     (ID,title,Details,Equipement,N_PDR,Date,Fréquance,Etat,Rp_d_intervention,ET_pdr))

        conn.commit()
        flash('tache Add', 'success')
        return redirect(url_for('LesTaches'))
    return render_template('addtache.html', )
@app.route('/editTache/<ID>', methods=['POST', 'GET'])
@is_logged_in
def get_Taches(ID):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute('SELECT * FROM lesTaches WHERE ID = ?', (ID,))

    posts = cur.fetchall()
    cur.close()

    print(posts[0])
    return render_template('editTache.html', lesTaches=posts[0])
@app.route('/updatetaches/<ID>', methods=["POST"])
@is_logged_in
def updatetaches(ID):

    ID = request.form['ID']
    title = request.form['title']
    Details = request.form['Details']
    Equipement = request.form['Equipement']
    N_PDR = request.form['N_PDR']
    Date = request.form['Date']
    Fréquance = request.form['Fréquance']
    Etat = request.form['Etat']
    Rp_d_intervention = request.form['Rp_d_intervention']
    ET_pdr = request.form['ET_pdr']
    con = sqlite3.connect("gmao.db")
    con.row_factory = sqlite3.Row
    conn = get_db_connection()
    cur=conn.cursor()
    cur.execute("UPDATE lesTaches SET title= ?,Details= ?,Equipement=?,N_PDR=?,Date=?,Fréquance=?,Etat=?,Rp_d_intervention=?,ET_pdr=? WHERE ID=?", (title,Details,Equipement,N_PDR,Date,Fréquance,Etat,Rp_d_intervention,ET_pdr ,ID,))
    conn.commit()
    return redirect(url_for('LesTaches'))


@app.route("/viewtache/<ID>", methods=['GET', 'POST'])
@is_logged_in
def view_tache(ID):
    items = get_Taches(ID)
    con = sqlite3.connect("gmao.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    posts = cur.execute( 'SELECT ID,title,Details,Equipement,N_PDR,Date,Fréquance,Etat,Rp_d_intervention,ET_pdr FROM LesTaches where ID=?',
        (ID,))
    tache = cur.fetchall()
    posts = []

    for rs in tache:
        posts_dict = {
            'ID': rs['ID'],
            'title': rs['title'],
            'cd_eq': rs['cd_eq'],
            'Details': rs['Details'],
            'Equipement': rs['Equipement'],
            'N_PDR': rs['N_PDR'],
            'Date': rs['Date'],
            'Fréquance': rs['Fréquance'],
            'Etat': rs['Etat'],
            'Rp_d_intervention': rs['Rp_d_intervention'],
            'ET_pdr': rs['ET_pdr'],
           }
        posts.append(posts_dict)

        return json.dumps(posts, )

@app.route('/DEL/<ID>', methods = ['POST','GET'])
@is_logged_in
def sup_tache(ID):
    conn = get_db_connection()
    con.row_factory=sqlite3.Row
    cur=conn.cursor()
    ID=str(ID)
    cur.execute('DELETE  FROM LesTaches WHERE ID = ?', (ID,))
    conn.commit()
    rows =cur.fetchone()
    flash('TACHE Removed Successfully')
    return redirect(url_for('LesTaches'))


# @app.route('/plus/<id>', methods=['POST', 'GET'])
# @is_logged_in
# def plus(id):
#
#
#
#     con = sqlite3.connect("gmao.db")
#     con.row_factory = sqlite3.Row
#     conn = get_db_connection()
#
#
#     posts = conn.execute('SELECT Qt=Qt+qt2 FROM PDR WHERE id=? ',(id,))
#     print(posts)
#     conn.commit()
#
#
#     return render_template('plus.html', posts=posts)
#
#     return redirect(url_for('PDR'))
#
# @app.route('/plus', methods = ['POST','GET'])
# @is_logged_in
# def plus():
#     conn = get_db_connection()
#     con.row_factory=sqlite3.Row
#     cur=conn.cursor()
#
#     posts=cur.execute('UPDATE PDR SET Qt = Qt + qt2 WHERE ID =?')
#     conn.commit()
#     rows =cur.fetchone()
#
#     return render_template('plus.html',post=posts)


#
# @app.route('/sup/<ID>', methods = ['POST','GET'])
# @is_logged_in
# def sup_PDR(id):
#     conn = get_db_connection()
#     con.row_factory=sqlite3.Row
#     cur=conn.cursor()
#     id=str(id)
#     cur.execute('DELETE  FROM lesTaches WHERE ID = ?', (ID,))
#     conn.commit()
#     rows =cur.fetchone()
#     flash('Tache Removed Successfully')
#     return redirect(url_for('lesTaches'))



# @app.route("/ajax_delete",methods=["POST","GET"])
# def ajax_delete():
#     con = sqlite3.connect("gmao.db")
#     con.row_factory = sqlite3.Row
#     cur = con.cursor()
#     if request.method == 'POST':
#         idcal = request.form['idcal']
#         print(idcal)
#         cur.execute('DELETE  FROM events WHERE idcal = {0}'.format(idcal))
#         con.commit()
#         msg = 'Record deleted successfully'
#     return jsonify(msg)





# @app.route("/view/<int:id_eq>", methods=("GET", "POST"))
# def view_user(id_eq):
#     row = get_Equipement(id_eq)
#     with sqlite3.connect("gmao.db") as con:
#         cur = con.cursor()
#         filename_or = row["image"]
#         posts =  con.execute("Select code_Equipement ,DESIGNATION,Marque,N_de_série,Date_d_acquisition,état,Remarque,type,image FROM Equipement where id_eq=?", (id_eq)).fetchone()
#         return render_template("view.html",posts=posts,row=row,)

# @app.route("/upload",methods=['GET','POST'])
# def upload():

#     con = sqlite3.connect("gmao.db")
#     con.row_factory = sqlite3.Row
#     cur = con.cursor()
#     cur.execute("select * from image")
#     data = cur.fetchall()
#     con.close()

#     if request.method=='POST':
#         upload_image=request.files['upload_image']

#         if upload_image.filename!='':
#             filepath=os.path.join(app.config['UPLOAD_FOLDER'],upload_image.filename)
#             upload_image.save(filepath)
#             con=sqlite3.connect("gmao.db")
           
#             cur=con.cursor()
#             cur.execute("insert into image(img)values(?)",(upload_image.filename,))
#             con.commit()
#             flash("File Upload Successfully","success")

#             con = sqlite3.connect("gmao.db")
#             con.row_factory=sqlite3.Row
#             cur=con.cursor()
#             cur.execute("select * from image")
#             data=cur.fetchall()
#             con.close()
#             return render_template("upload.html",data=data)
#     return render_template("upload.html",data=data)


  

# @app.route('/register',methods=['GET','POST'])
# def register():
#     if request.method=='POST':
#         try:
#             e_maile=request.form['e_maile']
#             password=request.form['password']
#             con=sqlite3.connect("gmao.db")
#             cur=con.cursor()
#             cur.execute("insert into utilisateur(e_maile,password)values(?,?)",(e_maile,password))
#             con.commit()
#             flash("Record Added  Successfully","success")
#         except:
#             flash("Error in Insert Operation","danger")
#         finally:
#             return redirect(url_for("index"))
#             con.close()

#     return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('you are now logged out','success')
    return redirect(url_for("index"))

if __name__ == '__main__':
    app.run(debug=True)
    # Check if "username" and "password" POST requests exist (user submitted form)
#     if request.method== 'POST'  and 'e_maile' in request.form and 'password' in request.form:
#         e_maile = request.form['e_maile']
#         password = request.form['password']
#         con=sqlite3.connect("gmao.db")
#         con.row_factory=sqlite3.Row
#         Cursor=con.cursor()
#         Cursor.execute("select * from USER where e_maile=? and password=? ",(e_maile,password))
#         data=Cursor.fetchone()

#         if data:
#             sessions["e_maile"]= data["e_maile"]
#             sessions["password"]= data["password"]
#             return redirect(url_for("dashboard"))
#         else:
#             flash("username and password not correct")
#             return redirect(url_for("login"))
#         # Check if account exists using MySQL
       
# @app.route('/dashboard',methods=["GET","POST"])
# def dashboard():
#     return render_template("dashboard.html")
# @app.route('/logout')
# def logout():
#     sessions.clear()
#     return redirect(url_for("login"))

    # conn=db_connection()
    # Cursor=conn.cursor()
    # if request.method=='GET':
    # Cursor=conn.execute("SELECT * FROM USER")
    # for row in Cursor.fetchall()
  #return jsonify(intervention)
    # form = LoginForm()
    # if form.validate_on_submit():
    #     user = User.query.filter_by(username=form.username.data).first()
    #     if user:
    #         if check_password_hash(user.password, form.password.data):
    #             login_user(user, remember=form.remember.data)
                #return 
                # redirect(url_for('dashboard'))

        #return '<h1>Invalid username or password</h1>'
    # form = LoginForm()
    # if form.validate_on_submit():
    #      return '<h1>' + form.email.data + ' ' + form.password.data + '</h1>'

    #return '<h1>Invalid username or password</h1>'
      
#     return render_template('login.html', form=form)


# @app.route('/dashboard')

# def dashboard():
#     return render_template('dashboard.html')

# @app.route('/logout')
# def logout():
  
#     return redirect(url_for('index'))

