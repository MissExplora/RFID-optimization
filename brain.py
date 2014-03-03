import util
from bottle import route, run, post, get, request, response, static_file
import json
import random
from sys import argv
import sqlite3
import time
import datetime
import finalna_verzija
db = sqlite3.connect("baza.proba1")


@post('/javljanje')
def javi():
    finalna_verzija.UbaciJSON(request.json,db)
    db.commit()

@get("/pinkiji")
def vrati():
    a = []
    response.set_header('Access-Control-Allow-Origin', '*')
    response.content_type = 'application/json'
    c = finalna_verzija.NaBlagajni(db)
    for i in c:
        pinki, broj, blagajna = c[i][0]
        a.append({"idpinkie":pinki,
            "count":int(broj),
            "blagajna":blagajna})
    return json.dumps(a)


@get("/kos")
def vrati():
    a = []
    response.set_header('Access-Control-Allow-Origin', '*')
    response.content_type = 'application/json'
    c = finalna_verzija.KolikoKosarica(db)
    for i in c:
        blagajna, koliko = c[i][0]
        a.append({"blagajna":blagajna,
            "count":koliko,
            "idpinkie":blagajna})

    return json.dumps(a)


@get("/stat1/<datum>")
def stat1(datum=None):
    print datum
    if not datum:
        datum = time.mktime(datetime.date.today().timetuple())
    response.set_header('Access-Control-Allow-Origin', '*')
    response.content_type = 'application/json'
    return json.dumps(
            util.flatten(finalna_verzija.StatUsloIzaslo(
                time.mktime(datetime.datetime.strptime(datum, "%m-%d-%Y").timetuple())
                ,db)
            ))


@get("/stat2/<datum>")
def stat2(datum=None):
    if not datum:
        datum = time.mktime(datetime.date.today().timetuple())
    response.set_header('Access-Control-Allow-Origin', '*')
    response.content_type = 'application/json'
    return json.dumps(
            util.flatten(finalna_verzija.StatVrijemeZadrzavanja(
                time.mktime(datetime.datetime.strptime(datum, "%m-%d-%Y").timetuple())
                ,db)
            ))


@get("/stat3/<datum>")
def stat3(datum=None):
    if not datum:
        datum = time.mktime(datetime.date.today().timetuple())
    response.set_header('Access-Control-Allow-Origin', '*')
    response.content_type = 'application/json'
    return json.dumps(
            util.flatten(finalna_verzija.StatPresloNaDrugu(
                time.mktime(datetime.datetime.strptime(datum, "%m-%d-%Y").timetuple())
                ,db)
            ))



@route('/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='./agk')



run(host='0.0.0.0', port=8080, debug=True)
