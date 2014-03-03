def cleanup(ldict):
    def razbacaj(di):
        tmp = {"blagajne":{}}
        for i,v in di:
            tmp["blagajne"][i] = {}
        for i,v in di:
            tmp["blagajne"][i][v] = di[i,v][0][0]
        return tmp 

    uslo, izaslo = ldict[0],ldict[1]
    return [{"uslo":razbacaj(uslo),"izaslo":razbacaj(izaslo)}]



def flatten(ldict):
    def raz(di,di2):
        tmp = []
        for i,v in di:
            tmp.append({"blagajna":i,"sati":v,"uslo":di[i,v][0][0]
                ,"izaslo":di2[i,v][0][0]})
        return tmp

    uslo, izaslo = ldict[0],ldict[1]
    return sorted(raz(uslo,izaslo),key=lambda k: k["sati"])


