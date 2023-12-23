from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Sample data for testing
def initialize_database():
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()

    # Create Labs table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS labs (
            lab_id INTEGER PRIMARY KEY,
            lab_name TEXT,
            capacity INTEGER
        )
    ''')

    # Create Teams table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS teams (
            team_id INTEGER PRIMARY KEY,
            team_lead_name TEXT,
            domain_name TEXT,
            lab_id INTEGER,
            FOREIGN KEY (lab_id) REFERENCES labs (lab_id)
        )
    ''')

    # Create Schedule table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS schedule (
            schedule_id INTEGER PRIMARY KEY,
            team_id INTEGER,
            lab_id INTEGER,
            start_time TEXT,
            end_time TEXT,
            FOREIGN KEY (team_id) REFERENCES teams (team_id),
            FOREIGN KEY (lab_id) REFERENCES labs (lab_id)
        )
    ''')

    # Create JuryPanel table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS jury_panel (
            panel_id INTEGER PRIMARY KEY,
            panel_name TEXT,
            team_id INTEGER,
            evaluation_time TEXT,
            FOREIGN KEY (team_id) REFERENCES teams (team_id)
        )
    ''')

    # # Sample data for Labs table
    # cursor.executemany('INSERT INTO labs (lab_name, capacity) VALUES (?, ?)',
    #                    [('Lab 1', 20), ('Lab 2', 20), ('Lab 3', 16)])

    connection.commit()
    connection.close()

initialize_database()

# Routes
@app.route('/base')
def base():
    return render_template('base.html')
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/team_registration', methods=['GET', 'POST'])
def team_registration():
    if request.method == 'POST':
        team_lead_name = request.form['team_lead_name']
        domain_name = request.form['domain_name']
        lab_preference = request.form['lab_preference']

        # Add logic to insert data into the database (similar to labs insertion)
        # For simplicity, assume lab_preference is a lab ID
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        cursor.execute('INSERT INTO teams (team_lead_name, domain_name, lab_id) VALUES (?, ?, ?)',
                       (team_lead_name, domain_name, lab_preference))
        connection.commit()
        connection.close()

        return redirect(url_for('index'))

    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    labs = cursor.execute('SELECT * FROM labs').fetchall()
    connection.close()

    return render_template('team_registration.html', labs=labs)

@app.route('/labs')
def labs():
    search_query = request.args.get('labSearch', '')
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    labs = cursor.execute('SELECT * FROM labs WHERE lab_name LIKE ?', (f'%{search_query}%',)).fetchall()
    connection.close()
    return render_template('labs.html', labs=labs)

@app.route('/schedule')
def schedule():
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    schedule_query = '''
        SELECT schedule.*, teams.team_lead_name
        FROM schedule
        JOIN teams ON schedule.team_id = teams.team_id
        JOIN labs ON schedule.lab_id = labs.lab_id
    '''
    schedule = cursor.execute(schedule_query).fetchall()
    connection.close()
    return render_template('schedule.html', schedule=schedule)

@app.route('/jury_panel')
def jury_panel():
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    jury_panel_query = '''
        SELECT jury_panel.*, teams.team_lead_name
        FROM jury_panel
        JOIN teams ON jury_panel.team_id = teams.team_id
    '''
    jury_panel = cursor.execute(jury_panel_query).fetchall()
    
    connection.close()
    return render_template('jury_panel.html', jury_panel=jury_panel)

@app.route('/team_details')
def team_details():
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    teams = cursor.execute('SELECT * FROM teams').fetchall()
    connection.close()
    return render_template('team_details.html', teams=teams)

@app.route('/search_team_details', methods=['GET', 'POST'])
def search_team_details():
    search_query = request.form["searcher"]
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    teams = cursor.execute('SELECT * FROM teams WHERE team_lead_name LIKE ?', (f'%{search_query}%',)).fetchall()
    connection.close()
    return render_template('team_details.html', teams=teams)


@app.route('/search_team_details2', methods=['GET', 'POST'])
def search_team_details2():
    search_query = request.form["searcher"]
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    schedule_query = '''
        SELECT schedule.*, teams.team_lead_name
        FROM schedule
        JOIN teams ON schedule.team_id = teams.team_id
        JOIN labs ON schedule.lab_id = labs.lab_id
        WHERE teams.team_lead_name LIKE ?
    '''
    schedule = cursor.execute(schedule_query, (f'%{search_query}%',)).fetchall()
    connection.close()
    return render_template('schedule.html', schedule=schedule)


@app.route('/search_team_details3', methods=['GET', 'POST'])
def search_team_details3():
    search_query = request.form["searcher"]
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()
    jury_panel_query = '''
        SELECT jury_panel.*, teams.team_lead_name
        FROM jury_panel
        JOIN teams ON jury_panel.team_id = teams.team_id
        WHERE teams.team_lead_name LIKE ?
    '''
    jury_panel = cursor.execute(jury_panel_query, (f'%{search_query}%',)).fetchall()
    connection.close()
    return render_template('jury_panel.html', jury_panel=jury_panel)

@app.route('/graphs')
def graphs():
    connection = sqlite3.connect('data.db')
    cursor = connection.cursor()

    import matplotlib.pyplot as plt
    query = "SELECT lab_name, capacity FROM labs" 
    data = cursor.execute(query).fetchall()

    # Extract data for the plot
    labels = [row[0] for row in data]
    values = [row[1] for row in data]

    # Create a bar plot
    plt.bar(labels, values)
    plt.xlabel('Lab Name')
    plt.ylabel('Capacity')
    plt.title('Lab Capacities')
    plt.savefig('static/bar_chart.png')  
    plt.close()

    query = '''
        SELECT schedule.start_time, teams.team_lead_name
        FROM schedule
        JOIN teams ON schedule.team_id = teams.team_id
        ORDER BY schedule.start_time
    '''
    data = cursor.execute(query).fetchall()

    # Extract data for the plot
    timestamps = [row[0] for row in data]
    team_names = [row[1] for row in data]

    # Create a line chart
    plt.figure(figsize=(10, 6))
    plt.plot(timestamps, team_names, marker='o', linestyle='-')
    plt.xlabel('Time')
    plt.ylabel('Team Lead Names')
    plt.title('Team Schedule Over Time')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('static/bar_chart2.png')  
    plt.close()
    bar_chart_url = url_for('static', filename='bar_chart.png')
    bar_chart_url2 = url_for('static', filename='bar_chart2.png')

    return render_template('graph.html', bar_chart_url=bar_chart_url,bar_chart_url2=bar_chart_url2)

if __name__ == '__main__':
    app.run(debug=True)
