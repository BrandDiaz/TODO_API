from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'many random bytes'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'todoapi'
mysql = MySQL(app)


@app.route('/')
def Index():
    conn = mysql.connection.cursor()
    conn.execute("SELECT  * FROM tarea")
    datos = conn.fetchall()
    conn.close()

    return render_template('Index.html', tareas=datos)


@app.route('/agregar', methods=['POST'])
def agregar():
    if request.method == "POST":
        flash("Tarea agregada")
        Tarea = request.form['Tarea']
        Estado = request.form['Estado']
        conn = mysql.connection.cursor()
        conn.execute("INSERT INTO tarea (Tarea, Estado) VALUES (%s, %s)", (Tarea, Estado))
        mysql.connection.commit()

        return redirect(url_for('Index'))


@app.route('/borrar/<string:ID>', methods=['GET'])
def borrar(ID):
    flash("Tarea borrada")
    conn = mysql.connection.cursor()
    conn.execute("DELETE FROM tarea WHERE id=%s", (ID,))
    mysql.connection.commit()

    return redirect(url_for('Index'))


@app.route('/actualizar', methods=['POST', 'GET'])
def actualizar():
    if request.method == 'POST':
        ID = request.form['id']
        Tarea = request.form['Tarea']
        Estado = request.form['Estado']
        conn = mysql.connection.cursor()
        conn = mysql.connection.cursor()
        conn.execute("""
               UPDATE tarea
               SET Tarea=%s, Estado=%s
               WHERE id=%s
            """, (Tarea, Estado, ID))
        flash("Tarea actualizada")
        mysql.connection.commit()
        return redirect(url_for('Index'))


if __name__ == "__main__":
    app.run(debug=True)
