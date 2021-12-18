from flask import Flask, render_template, url_for,jsonify,request
from flask_socketio import SocketIO, send

import uuid

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

uuid_exist=[]
names=[]
calif=[]

@socketio.on('mensaje')
def mensaje(msg):
    print(msg)
    send(msg,broadcast=True)

@app.route('/')
def inico():
    return "inicio"

@app.route('/client<uuid>',methods=['POST', 'GET'])
def client(uuid):
    if request.method == 'POST':
        exist2=False
        uuid_temp=request.form.get("UUID")
        for i in range(len(uuid_exist)):
            if (uuid_exist[i] == uuid):
                print(uuid_exist[i])
                exist2=True
            if exist2:
                calif[i]=request.form.get("calificacion")
                print(calif)
                return ('', 204)
        return render_template("client.html", UUID=uuid_temp)
        #return ('', 204)
    else:
        exist=False
        for i in range(len(uuid_exist)):
            if (uuid_exist[i] == uuid):
                print(uuid_exist[i])
                exist=True
            if exist:
                return render_template("client.html", UUID=uuid)
        else:
            return render_template("client.html", UUID="intruduceuuid")

        

@app.route('/test<word>')
def test(word):
    return render_template('Califications.html',name_part=word)

@app.route('/makeuuid<name>')
def make(name):
    UUID_new=str(uuid.uuid4())
    names.append(name)
    uuid_exist.append(UUID_new)
    print(UUID_new)
    calif.append('?')
    message = 'maked ' + UUID_new
    return message

@app.route('/gadet<uuid>')
def gadet(uuid):
    exist=False
    for i in range(len(uuid_exist)):
        if (uuid_exist[i] == uuid):
            print(uuid_exist[i])
            exist=True
        if exist:
            return render_template('Califications.html',name_part=names[i],uuid=uuid)
    else:
        return 'dont exist'




"""
Vien aqui comienza la parte de apirest y todo el asunto api

en resumen basandonos en la UUID buscamos los demas datos, y se supone que todas las array son simetricas

"""
@app.route('/getnum<uuid>')
def UUID(uuid):
    exist=False
    for i in range(len(uuid_exist)):
        if (uuid_exist[i] == uuid):
            print(uuid_exist[i])
            exist=True
        if exist:
            return jsonify({"uuid":uuid_exist[i],"name":names[i],"calification":calif[i]})
    else:
        return jsonify({"error":"not exist"})
    
@app.route('/send',methods=['POST'])
def sendcalification():
    for i in range(len(uuid_exist)):
        if (uuid_exist[i] == uuid):
            print(uuid_exist[i])
            exist=True
        if exist:
            uuid_temp = request.form.get("uuid")
            calif[i] = request.form.get("calificacion")
            return render_template("client.html", name_part=names[i], UUID=uuid_temp)
    else:
        return 'error not exist'

if __name__ == '__main__':
    #app.run(host="0.0.0.0", port=8080, debug=True)
    socketio.run(app)