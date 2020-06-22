from flask import Flask, render_template, flash, request, redirect, url_for
from flask_mysqldb import MySQL


app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'dbproyecto'
mysql = MySQL(app)

app.secret_key = 'mysecretkey'


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/persona')
def persona():

    return render_template('persona.html')



@app.route('/add_person', methods=['POST'])
def add_person():
    # creation into the database
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        cedula = request.form['cedu']
        direccion = request.form['dire']
        telefono = request.form['tele']
        edad = request.form['edad']

        cur = mysql.connection.cursor()

        cur.execute('INSERT INTO persona (nombre, apellido, cedula, edad, direccion, telefono) VALUES(%s, %s, %s,%s, %s, %s)',
                    (nombre, apellido, cedula, edad, direccion, telefono))

        mysql.connection.commit()
        flash('Se agrego una nueva persona')
        return redirect(url_for('persona'))

@app.route('/reporte')
def reporte():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM persona')
    data = cur.fetchall()
    cur.execute('SELECT * FROM libro')
    data2 = cur.fetchall()
    
    return render_template('reporte.html', persona = data, libro=data2)


@app.route('/delete/<id>')
def delete(id):
   cur =  mysql.connection.cursor()
   cur.execute('DELETE FROM persona WHERE id = {0}'.format(id)  )
   mysql.connection.commit()
   flash('Se elimino el dato')
   return redirect(url_for('reporte'))


@app.route('/edit/<id>')
def get_persona(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM persona WHERE id = {0}'.format(id))
    data = cur.fetchall()
    return render_template('editar.html', persona = data[0])

@app.route('/update/<id>', methods=['POST'])
def update_persona(id):
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        cedula = request.form['cedu']
        direccion = request.form['dire']
        telefono = request.form['tele']
        edad = request.form['edad']
        
        cur = mysql.connection.cursor()
        cur.execute("""
        UPDATE persona
        SET nombre = %s, 
            apellido = %s, 
            cedula = %s, 
            edad = %s, 
            direccion = %s, 
            telefono = %s
        WHERE id = %s
        """, (nombre,apellido,cedula,edad,direccion,telefono,id))
        mysql.connection.commit()

        flash('Se actualizo el dato')
        return redirect(url_for('reporte'))


@app.route('/buscar', methods=['GET', 'POST'])
def search():
    if request.method == "POST":
        book = request.form['book']
        cur = mysql.connection.cursor()

        cur.execute('SELECT * FROM persona')
        data2 = cur.fetchall()
        
        # search by author or book
        cur.execute("SELECT id, nombrelb, autor, fecha from libro WHERE nombrelb LIKE %s OR autor LIKE %s", (book, book))
        mysql.connection.commit()
        data = cur.fetchall()
    
        return render_template('reporte.html',libro=data, persona=data2)
    

  
if __name__ == '__main__':
    app.run(debug=True)