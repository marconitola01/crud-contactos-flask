from flask import Flask, render_template, request,redirect, url_for, flash
import pymysql

app = Flask(__name__)
#config connection
conn = pymysql.connect(host='localhost',port=3306,user='root',password='',db='flaskcontact')
cur = conn.cursor()
cur.execute("SELECT * from contacts")

#session
app.secret_key = 'mysecretkey'

#imprimir todos los registros de la tabla en la consola cuando se ejecuta en la terminal
for row in cur:
    print(row)

#cur.close()
#conn.close()

@app.route('/')
#metodo para devolver la ruta inicial
def home():
    cur = conn.cursor()
    cur.execute('SELECT * from contacts')
    data = cur.fetchall()
    #print(data)
    return render_template('index.html',contacts = data)

# metodo para agregar nuevo registro en la bd
@app.route('/agregar_contacto',methods=['POST'])
def agregar():
    if(request.method == 'POST'):
        fullname = request.form['fullname']
        telefono = request.form['telefono']
        email = request.form['email']
        print(fullname,telefono,email)

        cur.execute('INSERT INTO contacts (fullname,telefono,email) VALUES (%s,%s,%s)',(fullname,telefono,email))
        conn.commit()
        flash('contacto agregado satisfactoriamente')
        return redirect(url_for('home'))

#metodo para editar registros en la bd
@app.route('/editar/<id>')
def editar(id):
    cur = conn.cursor()
    cur.execute('SELECT * FROM contacts WHERE id = %s',(id))
    data = cur.fetchall()
    #print(data[0])
    #return 'recibido'
    return render_template('editar.html',contact = data[0])

#metodo de actualizacion de registros en la bd
@app.route('/actualizar/<id>',methods = ['POST'])
def actualizar(id):
    if(request.method == 'POST'):
        fullname = request.form['fullname']
        telefono = request.form['telefono']
        email = request.form['email']
        cur = conn.cursor()
        cur.execute('UPDATE contacts SET fullname = %s, telefono = %s, email = %s WHERE id=%s',(fullname,telefono,email,id))
        flash('contacto actualizado correctamente')
        return redirect(url_for('home'))


#metodo para eliminar un registro de la bd
@app.route('/eliminar/<string:id>')
def eliminar(id):
    cur = conn.cursor()
    cur.execute('DELETE FROM contacts WHERE id = {0}'.format(id))
    conn.commit()
    flash('contacto eliminado satisfactoriamente')
    return redirect(url_for('home'))



if __name__ == "__main__":
    app.run(port = 3000, debug=True)
