from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
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

# Rutas para Citas
@app.route('/citas', methods=['GET', 'POST'])
def mostrar_citas():
    cursor = db.cursor()

    if request.method == 'POST':
        doctor_id = request.form.get('doctor_id')
        paciente_id = request.form.get('paciente_id')
        fecha = request.form.get('fecha')

        if not doctor_id or not paciente_id or not fecha:
            flash("Por favor, llena todos los campos.", "error")
            return redirect(url_for('citas'))

        cursor.execute("SELECT COUNT(*) FROM Doctores WHERE id = %s", (doctor_id,))
        if cursor.fetchone()[0] == 0:
            flash("Doctor no válido.", "error")
            return redirect(url_for('citas'))

        cursor.execute("SELECT COUNT(*) FROM Pacientes WHERE id = %s", (paciente_id,))
        if cursor.fetchone()[0] == 0:
            flash("Paciente no válido.", "error")
            return redirect(url_for('citas'))

        cursor.execute("INSERT INTO Citas (doctor_id, paciente_id, fecha) VALUES (%s, %s, %s)", (doctor_id, paciente_id, fecha))
        db.commit()

    # Obtener citas
    cursor.execute("""
        SELECT Citas.id, Doctores.nombre AS doctor, Pacientes.nombre AS paciente, Citas.fecha
        FROM Citas
        JOIN Doctores ON Citas.doctor_id = Doctores.id
        JOIN Pacientes ON Citas.paciente_id = Pacientes.id
    """)
    citas = cursor.fetchall()

    # Obtener doctores y pacientes
    cursor.execute("SELECT id, nombre FROM Doctores")
    doctores = cursor.fetchall()

    cursor.execute("SELECT id, nombre FROM Pacientes")
    pacientes = cursor.fetchall()

    cursor.close()

    return render_template('citas.html', citas=citas, doctores=doctores, pacientes=pacientes)


# Ruta para agregar una nueva cita
@app.route('/agregar_cita', methods=['GET', 'POST'])
def agregar_cita():
    cursor = db.cursor()

    if request.method == 'POST':
        # Recoger los datos del formulario
        doctor_id = request.form.get('doctor_id')
        paciente_id = request.form.get('paciente_id')
        fecha = request.form.get('fecha')

        if not doctor_id or not paciente_id or not fecha:
            flash("Por favor, llena todos los campos.", "error")
            return redirect(url_for('citas'))

        # Comprobamos que los ids de doctor y paciente existen en la base de datos
        cursor.execute("SELECT COUNT(*) FROM Doctores WHERE id = %s", (doctor_id,))
        if cursor.fetchone()[0] == 0:
            flash("Doctor no válido.", "error")
            return redirect(url_for('mostrar_citas'))

        cursor.execute("SELECT COUNT(*) FROM Pacientes WHERE id = %s", (paciente_id,))
        if cursor.fetchone()[0] == 0:
            flash("Paciente no válido.", "error")
            return redirect(url_for('mostrar_citas'))

        # Insertar la nueva cita en la base de datos
        cursor.execute("INSERT INTO Citas (doctor_id, paciente_id, fecha) VALUES (%s, %s, %s)", (doctor_id, paciente_id, fecha))
        db.commit()
        return redirect(url_for('mostrar_citas'))

    # Obtener doctores y pacientes para las listas desplegables
    cursor.execute("SELECT id, nombre FROM Doctores")
    doctores = cursor.fetchall()

    cursor.execute("SELECT id, nombre FROM Pacientes")
    pacientes = cursor.fetchall()
    cursor.close()
    
    # Renderizar la plantilla para agregar cita, pasando los doctores y pacientes
    return render_template('citas.html', doctores=doctores, pacientes=pacientes)





# Ruta para editar una cita existente
@app.route('/edit_cita/<int:id>', methods=['GET', 'POST'])
def editar_cita(id):
    cursor = db.cursor()

    if request.method == 'POST':
        # Obtener datos del formulario
        doctor_id = request.form['doctor_id']
        paciente_id = request.form['paciente_id']
        fecha = request.form['fecha']

        # Actualizar la cita en la base de datos
        cursor.execute("UPDATE Citas SET doctor_id = %s, paciente_id = %s, fecha = %s WHERE id = %s", (doctor_id, paciente_id, fecha, id))
        db.commit()
        return redirect(url_for('mostrar_citas'))#este cambio realice

    # Obtener la cita actual para pre-rellenar el formulario
    cursor.execute("SELECT id, doctor_id, paciente_id, fecha FROM Citas WHERE id = %s", (id,))
    cita = cursor.fetchone()

    # Obtener listas de doctores y pacientes para los desplegables
    cursor.execute("SELECT id, nombre FROM Doctores")
    doctores = cursor.fetchall()

    cursor.execute("SELECT id, nombre FROM Pacientes")
    pacientes = cursor.fetchall()

    # Renderizar la plantilla para editar la cita
    return render_template('edit_cita.html', cita=cita, doctores=doctores, pacientes=pacientes)

# Ruta para eliminar una cita
@app.route('/delete_cita/<int:id>', methods=['POST'])
def eliminar_cita(id):
    cursor = db.cursor()
    cursor.execute("DELETE FROM Citas WHERE id = %s", (id,))
    db.commit()
    return redirect(url_for('mostrar_citas'))
# Rutas para Medicamentos
@app.route('/medicamentos')
def mostrar_medicamentos():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Medicamentos")
    medicamentos = cursor.fetchall()
    return render_template('medicamentos.html', medicamentos=medicamentos)

@app.route('/agregar_medicamento', methods=['POST'])
def agregar_medicamento():
    nombre = request.form['nombre']
    descripcion = request.form['descripcion']
    precio = request.form['precio']
    cursor = db.cursor()
    cursor.execute("INSERT INTO Medicamentos (nombre, descripcion, precio) VALUES (%s, %s, %s)", (nombre, descripcion, precio))
    db.commit()
    return redirect(url_for('mostrar_medicamentos'))

@app.route('/edit_medicamento/<int:id>', methods=['GET', 'POST'])
def editar_medicamento(id):
    cursor = db.cursor()
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        precio = request.form['precio']
        cursor.execute("UPDATE Medicamentos SET nombre = %s, descripcion = %s, precio = %s WHERE id = %s", (nombre, descripcion, precio, id))
        db.commit()
        return redirect(url_for('mostrar_medicamentos'))
    cursor.execute("SELECT * FROM Medicamentos WHERE id = %s", (id,))
    medicamento = cursor.fetchone()
    return render_template('edit_medicamento.html', medicamento=medicamento)

@app.route('/delete_medicamento/<int:id>', methods=['POST'])
def eliminar_medicamento(id):
    cursor = db.cursor()
    cursor.execute("DELETE FROM Medicamentos WHERE id = %s", (id,))
    db.commit()
    return redirect(url_for('mostrar_medicamentos'))






# Ejecutar la aplicación
if __name__ == '__main__':
    app.run(debug=True)
