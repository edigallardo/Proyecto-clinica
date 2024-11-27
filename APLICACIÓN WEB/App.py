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

# Rutas para Tratamientos
@app.route('/tratamientos')
def mostrar_tratamientos():
    cursor = db.cursor()
    cursor.execute("""
        SELECT Tratamientos.id, Citas.id, Medicamentos.nombre, Tratamientos.dosis, Tratamientos.duracion
        FROM Tratamientos
        JOIN Citas ON Tratamientos.cita_id = Citas.id
        JOIN Medicamentos ON Tratamientos.medicamento_id = Medicamentos.id
    """)
    tratamientos = cursor.fetchall()
    return render_template('tratamientos.html', tratamientos=tratamientos)

@app.route('/agregar_tratamiento', methods=['POST'])
def agregar_tratamiento():
    cita_id = request.form['cita_id']
    medicamento_id = request.form['medicamento_id']
    dosis = request.form['dosis']
    duracion = request.form['duracion']
    cursor = db.cursor()
    cursor.execute("INSERT INTO Tratamientos (cita_id, medicamento_id, dosis, duracion) VALUES (%s, %s, %s, %s)", (cita_id, medicamento_id, dosis, duracion))
    db.commit()
    return redirect(url_for('mostrar_tratamientos'))

@app.route('/edit_tratamiento/<int:id>', methods=['GET', 'POST'])
def editar_tratamiento(id):
    cursor = db.cursor()
    if request.method == 'POST':
        cita_id = request.form['cita_id']
        medicamento_id = request.form['medicamento_id']
        dosis = request.form['dosis']
        duracion = request.form['duracion']
        cursor.execute("UPDATE Tratamientos SET cita_id = %s, medicamento_id = %s, dosis = %s, duracion = %s WHERE id = %s", (cita_id, medicamento_id, dosis, duracion, id))
        db.commit()
        return redirect(url_for('mostrar_tratamientos'))
    cursor.execute("SELECT * FROM Tratamientos WHERE id = %s", (id,))
    tratamiento = cursor.fetchone()
    return render_template('edit_tratamiento.html', tratamiento=tratamiento)

@app.route('/delete_tratamiento/<int:id>', methods=['POST'])
def eliminar_tratamiento(id):
    cursor = db.cursor()
    cursor.execute("DELETE FROM Tratamientos WHERE id = %s", (id,))
    db.commit()
    return redirect(url_for('mostrar_tratamientos'))