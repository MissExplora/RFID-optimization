#!/usr/local/bin/python2.7

import sqlite3
import json
import time
import datetime



def UbaciJSON(primljen_json, test1): 
    cur = test1.cursor()
    podatak = cur.execute("SELECT radi FROM pinkie WHERE id_pinkie=?", (primljen_json["id_pinkie"]))
    podatak = str(podatak[0])
    if (podatak == "1"): # ako je signal primljen od blagajne koja radi, obradi, inace ignoriraj
        cur.execute("INSERT INTO poruka VALUES(?,?,?,?)", (primljen_json["id_pinkie"], primljen_json["id_tag"], time.time(), primljen_json["action"]))
        cur.commit()
    cur.close()


        
def NaBlagajni(test1): # uz pretpostavku da se dinamicki poziva svake minute (auto-reload stranice svaku min)
    cur1 = test1.cursor()
    cur2 = test1.cursor()
    blagajne = {} 
    
    for index in cur1.execute("SELECT id_pinkie FROM pinkie WHERE radi=1"):
        m = str(index[0])
        blagajne[m] = cur2.execute("""SELECT 
                                    (SELECT id_pinkie FROM poruka WHERE poruka.id_tag=tagovi.id_tag ORDER BY vrijeme_por DESC limit 1) AS pinkic,  
                                    SUM(tagovi.vrsta_tag) AS suma, 
                                    (SELECT ime_blagajne FROM pinkie WHERE 
                                    (SELECT id_pinkie FROM poruka WHERE poruka.id_tag=tagovi.id_tag ORDER BY vrijeme_por DESC limit 1)=?) AS blagajna 
                                    FROM tagovi
                                    WHERE tagovi.aktivnost_t=1 AND (SELECT id_pinkie FROM poruka WHERE poruka.id_tag=tagovi.id_tag ORDER BY vrijeme_por DESC limit 1)=?
                                    GROUP BY pinkic""", (m,m)).fetchall()       
    cur1.close()
    cur2.close()
    return blagajne
        
        
        
def KolikoKosarica(test1):
    cur1 = test1.cursor()
    cur2 = test1.cursor()
    kosarice = {}
    for index in cur1.execute("SELECT id_pinkie FROM pinkie WHERE radi=1"):
        m = str(index[0])
        kosarice[m] = cur2.execute("SELECT ime_blagajne, kosarice FROM pinkie WHERE id_pinkie=?", (m)).fetchall()
    cur1.close()
    cur2.close()
    return kosarice
    
        
        
def StatUsloIzaslo(dan, test1): # vraca broj ulazaka i izlazaka
    cur1 = test1.cursor()
    cur2 = test1.cursor()
    uslo = {} # dictionary svih tagova sa vremenima koji su dosli unutar jednog sata
    izaslo = {} # dictionary svih tagova sa vremenima koji su otisli unutar jednog sata
    
    for index in cur1.execute("SELECT id_pinkie FROM pinkie"):
        m = str(index[0])
        for n in range(8,22):
            sat1 = dan+n*3600
            sat2 = dan+(n+1)*3600
            uslo[m,n] = cur2.execute("SELECT COUNT(id_tag) FROM poruka WHERE aktivnost=1 AND id_pinkie=? AND vrijeme_por>=? AND vrijeme_por<?", (m, sat1, sat2)).fetchall()
            izaslo[m,n] = cur2.execute("SELECT COUNT(id_tag) FROM poruka WHERE aktivnost=0 AND id_pinkie=? AND vrijeme_por>=? AND vrijeme_por<?", (m, sat1, sat2)).fetchall()
    cur1.close()
    cur2.close()
    return (uslo, izaslo) 
    
    
    
def StatVrijemeZadrzavanja(dan, test1): # max, min i avg zadrzavanje po blagajnama bez "slucajnih"
    cur1 = test1.cursor()
    cur2 = test1.cursor()
    uslo = {} # dictionary svih tagova sa vremenima koji su dosli unutar jednog sata
    izaslo = {} # dictionary svih tagova sa vremenima koji su otisli unutar jednog sata
    stat = {}
    
    for index in cur1.execute("SELECT id_pinkie FROM pinkie"):
        m = str(index[0])
        for n in range(8,22):
            sat1 = dan+n*3600
            sat2 = dan+(n+1)*3600
            uslo[m,n] = cur2.execute("SELECT id_tag, vrijeme_por FROM poruka WHERE aktivnost=1 AND id_pinkie=? AND vrijeme_por>=? AND vrijeme_por<?", (m,sat1,sat2)).fetchall()
            izaslo[m,n] = cur2.execute("SELECT id_tag, vrijeme_por FROM poruka WHERE aktivnost=0 AND id_pinkie=? AND vrijeme_por>=? AND vrijeme_por<?", (m,sat1,sat2)).fetchall()
        
            vrijeme = []   
            if (len(izaslo[m,n])!=0 and len(uslo[m,n])!=0): 
                uslo[m,n].sort()
                izaslo[m,n].sort()
                i=0
                while(i<len(izaslo[m,n])):
                    if(izaslo[m,n][i][0]==uslo[m,n][i][0]):
                        vrijeme.append(izaslo[m,n][i][1]-uslo[m,n][i][1])
                        i+=1
                    else:
                        uslo[m,n].pop(i)
            
            if len(vrijeme)!=0:                
                minimalno = min(vrijeme)/60
                maximalno = max(vrijeme)/60
                prosjecno = 0
                for i in vrijeme:
                    prosjecno += i
                    prosjecno = (prosjecno/len(vrijeme))/60
            else:
                minimalno = maximalno = prosjecno = 0
            stat[m,n] = [minimalno, maximalno, prosjecno]
        
    cur1.close()
    cur2.close()
    return stat

            
            
            
def StatPresloNaDrugu(dan, test1): # statistika koliko je ljudi preslo iz jedne blagajne na drugu
    cur = test1.cursor()
    stat = {}
    
    for n in range(8,22):
        sat1 = dan+n*3600
        sat2 = dan+(n+1)*3600
        aktivni = cur.execute("""SELECT tagovi.id_tag, (SELECT vrijeme_por, id_pinkie FROM poruka WHERE poruka.id_tag=tagovi.id_tag AND vrijeme_por>=? AND vrijeme_por<? 
                                                        ORDER BY vrijeme_por DESC limit 1)
                                FROM tagovi
                                WHERE tagovi.aktivnost_t=1""", (sat1,sat2)).fetchall()
        for i in range(len(aktivni)):
            tag = aktivni[i][0]
            lista = cur.execute("""SELECT vrijeme_por, id_pinkie FROM poruka WHERE poruka.id_tag=? AND poruka.aktivnost=0 AND vrijeme_por>=? AND vrijeme_por<? 
                                    ORDER BY vrijeme_por DESC limit 1""", (tag,sat1,sat2)).fetchall()
            if ((aktivni[i][1]-lista[0])<=120 and aktivni[i][2]!=lista[1]): # ako je vrijeme proteklo izmedju deaktivacije i ponovne aktivacije <= 2 min i nije na istoj blagajni
                if (lista[1],n) in stat:
                    stat[lista[1],n] += 1
                else:  
                    stat[lista[1],n] = 1
                    
    cur.close()
    return stat
    
    
    
            

if __name__=="__main__":
    test1 = sqlite3.connect("baza.proba1")
    print StatVrijemeZadrzavanja(1380240000,test1)
    