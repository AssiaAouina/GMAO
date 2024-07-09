from cgitb import text
import sqlite3



conn = sqlite3.connect('gmao.db')
c = conn.cursor()

try:
    sqliteConnection = sqlite3.connect('gmao.db')
    cursor = sqliteConnection.cursor()
    print("Successfully Connected to SQLite")

    sqlite_query ="""INSERT INTO PDR (qt2) VALUES( '1');"""
    count = cursor.execute(sqlite_query)
    sqliteConnection.commit()
    print("Record inserted successfully into SqliteDb_developers table ", cursor.rowcount)
    cursor.close()

except sqlite3.Error as error:
    print("Failed to insert data into sqlite table", error)
finally:
    if sqliteConnection:
        sqliteConnection.close()
        print("The SQLite connection is closed")


# try:
#     sqliteConnection = sqlite3.connect('gmao.db')
#     cursor = sqliteConnection.cursor()
#     print("Successfully Connected to SQLite")
#
#     sqlite_query ="""INSERT INTO lesTaches\
#                  (ID,title,Details,Equipement,N_PDR,Date,Fréquance,Etat,Rp_d_intervention,ET_pdr) \
#            VALUES  ('1','tache1','','Roulement à billes à gorge profonde ','ROULEMENT DE PALIER  ', '2022-02-03 ','', '','','desponible'),
#                   ('2','tache2','','Roulement à billes à simple rangée','','2022-03-04 16:00:00', '','','','non_desponible'),
#                   ('3','tache3','','Roulement à rouleaux cylindriques',' ' ,'2022-04-16 16:00:00', '','','','desponible'),
#                   ('4','tache4','','Roulement à rouleaux coniques', ' ','2022-05-03 16:00:00', '','','','non_desponible')
#              ;"""
#     count = cursor.execute(sqlite_query)
#     sqliteConnection.commit()
#     print("Record inserted successfully into SqliteDb_developers table ", cursor.rowcount)
#     cursor.close()
#
# except sqlite3.Error as error:
#     print("Failed to insert data into sqlite table", error)
# finally:
#     if sqliteConnection:
#         sqliteConnection.close()
#         print("The SQLite connection is closed")
#


# c.execute("""INSERT INTO events\
#           (Detail,Equipement,Nom_pdr,start_event,end_event,Fréquance,Etat,Rp_inter,etat_pdr,title) \
#             VALUES
# ('','Roulement à billes à gorge profonde ','', '2022-02-03 16:00:00','2021-02-04 03:00:00', '','','','desponible','Tache1'),
# ('','Roulement à billes à simple rangée','','2022-03-04 16:00:00','2021-03-04 05:00:00', '','','','non_desponible','Tache2'),
# ('','Roulement à rouleaux cylindriques','' ,'2022-04-16 16:00:00','2021-04-16 03:00:00', '','','','desponible','Tache3'),
# ('','Roulement à rouleaux coniques', '','2022-05-03 16:00:00','2021-05-04 03:00:00', '','','','non_desponible','Tache4')
# ;""")
# print("insert")

# c.execute("""CREATE TABLE PDR(
#     id text,
#     Nom text,
#     Réf text,
#     Qt text,
#     Marque text,
#     Etat text

#      )"""
#          )
# print("created")
# c.execute("""CREATE TABLE events(
#     idcal   int  ,
#
#     start_event Date ,
#     end_event Date  ,
#
#     title text
#
#     )"""
#          )
# print("created")

# c.execute("""CREATE TABLE  events(
#     idcal  INTEGER PRIMARY KEY AUTOINCREMENT ,
#
#     start_event Date ,
#     end_event Date  ,
#
#     title text
#
#     )"""
#          )
# print("created")
# c.execute("SELECT * FROM events ")
# print(c.fetchall())
# c.execute("""ALTER TABLE events
# RENAME COLUMN id TO idcal;
      
#      )""")
# print("created")


# c.execute("DELETE FROM Equipement WHERE 'code_Equipement' = '';")
# c.execute("""CREATE TABLE lesTaches(
#   ID INTEGER ,
#   title text,
#   Details text,
#   Equipement text,
#   N_PDR text,
#   Date text,
#   Fréquance text,
#   Etat text,
#   Rp_d_intervention text,
#   ET_pdr text,
#
#   FOREIGN KEY(ID) REFERENCES events(idcal),
#   FOREIGN KEY(N_PDR) REFERENCES pdr(Nom),
#   FOREIGN KEY(title) REFERENCES events(title),
#   FOREIGN KEY(ET_pdr) REFERENCES pdr(Etat)
#     )"""
#         )
# print("created")
# c.execute("select * from image")
# print( c.fetchall())
#
# conn.execute("DROP TABLE events" )
# print("deleted")
# conn.commit()
# conn.close()
# print('success')
# c.execute("SELECT * FROM Equipement")
# print( c.fetchall())
# #c.execute("ALTER TABLE intervention ADD Temps_d_arrêt VARCHAR")

# #c.execute("ALTER TABLE intervention DROP Temps_d_arrêt ")
# c.execute("DELETE FROM Equipement WHERE code_Equipement IS NULL OR trim(code_Equipement) = '';")
# c.execute("SELECT * FROM Equipement")
# print( c.fetchall())

# 
# 7
# 3
# 1
# 5

# conn.execute = ("INSERT INTO inter   VALUES (1321, 'RIZQY  REDOUANE', 2125555555, 'RIZQY.REDOUANE@gmail.com' )")
# inter_list = [
#     (1321, 'RIZQY  REDOUANE', 2125555555, 'RIZQY.REDOUANE@gmail.com'),
#     (1423, 'LAHJIOUJ  ZAKARIA', 2126666666, 'LAHJIOUJ.ZAKARIA@gmail.com' ),
#     ("MIC", 'MOROCCAN.INDUSTRIAL.COMPANY', 2127777777, 'THE.MOROCCAN.COMPANY@gmail.com' ),
#  ]
# conn.executemany("insert into inter values ((id,name,contact,email))", inter_list)

# import sqlite3



# try:
#     sqliteConnection = sqlite3.connect('gmao.db')
#     cursor = sqliteConnection.cursor()
#     print("Successfully Connected to SQLite")

#     sqlite_query ="""INSERT INTO Equipement\
#                       (id_eq,code_Equipement,DESIGNATION,Marque,N_de_série,Date_d_acquisition,état,Remarque,type,image) \
#                     VALUES(1, 'PS0001',  'Poste à souder SAF-FRO', 'BUFFALLO', '500X 211-4675549','2012-01-01 00:00:00.000','En marche','','',''),
#                        (2, 'PS0002',  'Poste à souder SAF-FRO', 'BUFFALLO', ' 500X 211-4675553', '2012-01-01 00:00:00.000','En marche', '','',''),
#                        (3,'PS0003',  'Poste à souder SAF-FRO', 'BUFFALLO',' 500X 211-4675542','2012-01-01 00:00:00.000','En marche','','',''),
#                        (4,'PS0004', 'Poste à souder SAF-FRO', 'BUFFALLO', '  500X 211-4642420', '2012-01-01 00:00:00.000', 'En panne', '','',''),
#                        (5,'PS0005', 'Poste à souder SAF-FRO', 'BUFFALLO', '  500X 218-4548770', '2012-01-01 00:00:00.000', 'En panne', '','',''),
#                        (6,'PS0006', 'Poste à souder SAF-FRO', 'BUFFALLO', '  500X 218-4523554', '2012-01-01 00:00:00.000', 'En panne', '','',''),
#                        (7,'PS0007', 'Poste à souder SAF-FRO', 'BUFFALLO', '   500X 218-4523591', '2012-01-01 00:00:00.000', 'En panne', '','',''),
#                        (8,'PS0008', 'Poste à souder SAF-FRO', 'BUFFALLO', '  500X 218-4508900', '2012-01-01 00:00:00.000', 'En panne', '','',''),
#                        (9,'PS0009', 'Poste à souder SAF-FRO', 'BUFFALLO', ' 500X 218-4508901', '2012-01-01 00:00:00.000', 'En panne', '','',''),
#                        (10,'PS0010', 'Poste à souder SAF-FRO', 'BUFFALLO', '  500X 218-4508902', '2012-01-01 00:00:00.000', 'En panne', '','','');"""
                                
                       


#     count = cursor.execute(sqlite_query)
#     sqliteConnection.commit()
#     print("Record inserted successfully into SqliteDb_developers table ", cursor.rowcount)
#     cursor.close()

# except sqlite3.Error as error:
#     print("Failed to insert data into sqlite table", error)
# finally:
#     if sqliteConnection:
#         sqliteConnection.close()
#         print("The SQLite connection is closed")




# try:
#     conn = sqlite3.connect('gmao.db')
#     cur = conn.cursor()
#     print("Connexion réussie à SQLite")

#     sql = "INSERT INTO USER (e_maile, password) VALUES ('sncha@gmail.com','12345')"


#     count = cur.execute(sql)
#     conn.commit()
#     print("Enregistrement inséré avec succès dans la table USER")
#     cur.close()
#     conn.close()
#     print("SELECT * FROM USER")

# except sqlite3.Error as error:
#     print("Erreur lors de l'insertion dans la table USER", error)
# c.execute("""CREATE TABLE USER(
#     e_maile text,
#     password text
#     )"""
# )
# USER_list = [
#    ('sncha@gmail.com','12345'),
#    ('snchb@gmail.com' ,'azer123'),
#    ('snchc@gmail.com','ab1234'),
# ]
# c.executemany =("insert into USER values (?,?)",USER_list)
# Connection.commit()
# c.close()
#c.commit()
#c.close()
# c.execute("""CREATE TABLE inter(
#   id text ,
#   name text,
#   contact text,
#   email text
#    )"""
#           )
# c.execute("""CREATE TABLE Equipement(
 
#   code_Equipement text,
#   DESIGNATION text,
#   Marque text
#   N_de_série text,
#   Date_d_acquisition text,
#   état text,
#   Remarque text,
#    type text,
#    image blob
#     )"""
#         )
# c.execute("""CREATE TABLE intervention(
#   id_Equipement INTEGER ,
#   N_fiche_intervention text  ,
#   code_Equipement text,
#   n_intervenant text,
#   id_Intervenant text,
#   Date_d_anomalie text,
#   date_intervention text,
#   organ text,
#   Nature_de_panne text,
#   Cause_de_panne text,
#   date_interv text,
#   Date_de_mise_en_service text
#   Remarque text
 
# )""")

# Equipement_list = [
#    ( 'PS0001',  'Poste à souder SAF-FRO', 'BUFFALLO', '500X 211-4675549','2012-01-01 00:00:00.000','En marche','','',''),
#     ( 'PS0002',  'Poste à souder SAF-FRO', 'BUFFALLO', ' 500X 211-4675553', '2012-01-01 00:00:00.000','En marche', '','',''),
#     ( 'PS0003',  'Poste à souder SAF-FRO', 'BUFFALLO',' 500X 211-4675542','2012-01-01 00:00:00.000','En marche','','',''),
#     ( 'PS0004', 'Poste à souder SAF-FRO', 'BUFFALLO', '  500X 211-4642420', '2012-01-01 00:00:00.000', 'En panne', '','',''),
#     ( 'PS0005', 'Poste à souder SAF-FRO', 'BUFFALLO', '  500X 218-4548770', '2012-01-01 00:00:00.000', 'En panne', '','',''),
#     ( 'PS0006', 'Poste à souder SAF-FRO', 'BUFFALLO', '  500X 218-4523554', '2012-01-01 00:00:00.000', 'En panne', '','',''),
#     ( 'PS0007', 'Poste à souder SAF-FRO', 'BUFFALLO', '   500X 218-4523591', '2012-01-01 00:00:00.000', 'En panne', '','',''),
#     ( 'PS0008', 'Poste à souder SAF-FRO', 'BUFFALLO', '  500X 218-4508900', '2012-01-01 00:00:00.000', 'En panne', '','',''),
#     ( 'PS0009', 'Poste à souder SAF-FRO', 'BUFFALLO', ' 500X 218-4508901', '2012-01-01 00:00:00.000', 'En panne', '','',''),
#     ( 'PS0010', 'Poste à souder SAF-FRO', 'BUFFALLO', '  500X 218-4508902', '2012-01-01 00:00:00.000', 'En panne', '','',''),

# ]
# c.executemany("insert into  Equipement values ( code_Equipement,DESIGNATION,Marque,N_de_série,Date_d_acquisition,état,Remarque,type,image)", Equipement_list)
# print("SELECT * FROM Equipement")
# intervention_list = [
# ( '1','INTV00001',  'PS0002', 'LAHJIOUJ  ZAKARIA ', '1423','2021-07-03 08:00:00.000','2021-07-03 08:00:00.000',' Pompe','Electrique','ElectriqueElectrique','2','2021-07-03 08:00:00.000'),
# (' 2','INTV00002',  'PS0003', 'LAHJIOUJ  ZAKARIA ', '1423','2021-07-03 08:00:00.000','2021-07-03 08:00:00.000',' Reducteur ','Mécanique','Manque de phase','3','2021-07-03 08:00:00.000'),
# ( '3','INTV00003',  'PS0004', 'RIZQY REDOUANE ', '1321','2012-06-07 13:00:00.000','2012-06-07 13:00:00.000',' Frein ','Mécanique','Manque de phase',"10",'10,2012-06-07 13:00:00.000'),
# ( '4','INTV00004',  'PS0005', 'RIZQY REDOUANE', '1321','2012-06-07 13:00:00.000','2012-06-07 13:00:00.000',' Electrovanne ','Hydraulique','Manque de phase','7','2012-07-07 10:00:00.000'),
# ( '5','INTV00005',  'PS0006', 'THE MOROCCAN INDUSTRIAL COMPANY', 'MIC','2012-08-07 00:00:00.000','2012-08-07 00:00:00.000',' Reducteur  ','Mécanique','Manque de phase','3','2012-08-07 00:00:00.000'),
# ( '6','INTV00006',  'PS0004', 'THE MOROCCAN INDUSTRIAL COMPANY ', 'MIC','2021-04-05 00:00:00.000','2021-04-05 00:00:00.000',' Frein ','Mécanique','Manque de phase','1','2021-04-05 00:00:00.000'),
# ( '7','INTV00007',  'PS0005', 'THE MOROCCAN INDUSTRIAL COMPANY ', 'MIC','2021-03-06 00:00:00.000','2021-03-06 00:00:00.000',' Electrovanne ','Hydraulique','Manque de phase','5','2021-03-06 00:00:00.000'),
# ]
# c.executemany("insert into  intervention values (?,?,?,?,?,?,?,?,?,?,?,?)", intervention_list)



 

# (id,name,contact,email)
# "(1423, 'LAHJIOUJ  ZAKARIA', 2126666666, 'LAHJIOUJ.ZAKARIA@gmail.com' );" \
# "(MIC, 'MOROCCAN.INDUSTRIAL.COMPANY', 2127777777, 'THE.MOROCCAN.COMPANY@gmail.com' ); "