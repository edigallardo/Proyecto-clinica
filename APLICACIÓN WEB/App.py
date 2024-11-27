from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

app.config['SECRET_KEY'] = 'eIorsH7Wnh'


# Rutas para Doctores
@app.route('/doctores')
def mostrar_doctores():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Doctores")
    doctores = cursor.fetchall()
    return render_template('doctores.html', doctores=doctores)

@app.route('/agregar_doctor', methods=['POST'])
def agregar_doctor():
    nombre = request.form['nombre']
    especialidad = request.form['especialidad']
    cursor = db.cursor()
    cursor.execute("INSERT INTO Doctores (nombre, especialidad) VALUES (%s, %s)", (nombre, especialidad))
    db.commit()
    return redirect(url_for('mostrar_doctores'))

@app.route('/edit_doctor/<int:id>', methods=['GET', 'POST'])
def editar_doctor(id):
    cursor = db.cursor()
    if request.method == 'POST':
        nombre = request.form['nombre']
        especialidad = request.form['especialidad']
        cursor.execute("UPDATE Doctores SET nombre = %s, especialidad = %s WHERE id = %s", (nombre, especialidad, id))
        db.commit()
        return redirect(url_for('mostrar_doctores'))
    cursor.execute("SELECT * FROM Doctores WHERE id = %s", (id,))
    doctor = cursor.fetchone()
    return render_template('edit_doctor.html', doctor=doctor)

@app.route('/delete_doctor/<int:id>', methods=['POST'])
def eliminar_doctor(id):
    cursor = db.cursor()
    cursor.execute("DELETE FROM Doctores WHERE id = %s", (id,))
    db.commit()
    return redirect(url_for('mostrar_doctores'))