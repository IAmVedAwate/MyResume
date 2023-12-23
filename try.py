import sqlite3
connection = sqlite3.connect('data.db')
cursor = connection.cursor()
# Sample data for Labs table

cursor.executemany('INSERT INTO jury_panel (panel_name, team_id, evaluation_time) VALUES (?,?,?)',
                    [("Qazi Sir",1,"11:00"),("Jalane Sir",2,"11:00"),("Kamble Sir",3,"11:00"),("Qazi Sir",4,"11:00"),("Jalane Sir",5,"11:00"),("Kamble Sir",6,"11:00"),("Qazi Sir",7,"11:00"),("Jalane Sir",8,"11:00"),("Kamble Sir",9,"11:00"),("Qazi Sir",10,"11:00")])
connection.commit()
connection.close()

