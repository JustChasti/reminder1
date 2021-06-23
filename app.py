from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import json
import datetime
import sender
import os
import config


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rem.db'
db = SQLAlchemy(app)
now = datetime.datetime.now()

message_list = []
time_list = []


class base_model(db.Model):
    __tablename__ = 'remind'
    id = db.Column(db.Integer(), primary_key=True)
    date = db.Column(db.Text(), nullable=False)
    time = db.Column(db.Text(), nullable=False)
    text = db.Column(db.Text(), nullable=False)

    def __repr__(self):
        return "<{}:{}>".format(self.id,  self.text)


@app.route("/", methods=["GET", "POST"])
def request_handler():
    r_obj = request.json
    global message_list 
    global time_list
    print(r_obj)
    if r_obj['type'] == 'message':
        model = base_model(date=r_obj['date'], time=r_obj['time'], text=r_obj['text'])
        db.session.add(model)
        db.session.commit()
    elif r_obj['type'] == 'ask':
        """ оптимизировать работу с датой и временем, что бы замена была замена базы и запроса 1 раз, лучше поменять еще в боте"""
        reminds = base_model.query.all()
        now = datetime.datetime.now()
        time0 = str(now.time())[:5].split(':')
        currenttime = int(time0[0])*60 + int(time0[1])
        if True:
            today = r_obj['date']
            today = today[5:].replace("-", ".")
            temp = str(today)
            today = temp[3:5] + "." + temp[:2]
            for i in reminds:
                basedate = str(i.date)
                #print(i.time, i.text)
                print(basedate, today)
                if len(str(i.date)) > 5:
                    temp = str(i.date)[5:]
                    basedate = temp[3:5] + "." + temp[:2]
                if basedate == today:
                    print(today, basedate, i.time)
                    basetime = str(i.time).split(':')
                    print(currenttime + config.upd_time_format_1, int(basetime[0])*60 + int(basetime[1]))
                    if currenttime + config.upd_time_format_1 > int(basetime[0])*60 + int(basetime[1]):  # 15 каждые 15 минут
                        message_list.append(i.text)
                        time_list.append(i.time)
                        print('sucsess0')
                        del_obj = base_model.query.get_or_404(i.id)
                        db.session.delete(del_obj)
                        #db1.execute('delete from entries where id = ?'[request.form['i.id']])
                        db.session.commit()
                        print('sucsess')
        data = {
                "upd": r_obj['time'],
                "message":  message_list,
                "time": time_list
                }
        with open('data.json', 'w') as f:
            json.dump(data, f, ensure_ascii=False)
            print(data)

        print('station2')
        message_list = []
        time_list = []

    return 'обработчик запросов'


if __name__ == "__main__":
    app.run(debug=True)
