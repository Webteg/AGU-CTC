# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
import sqlite3
import csv
import os
from time import sleep


class extractLattes:
    def __init__(self, url=None):
        self.ids = []
        self.conn = sqlite3.connect("/home/lab-pesquisa/Desktop/AGU-CTC/ids.db")
        self.cursor = self.conn.cursor()
        self.atual_url = "http://buscatextual.cnpq.br/buscatextual/busca.do?metodo=forwardPaginaResultados&registros=0;10&query=%28+%2Bidx_grd_area_atua%3A%22ENGENHARIAS%22++++++++%2Bidx_atuacao_prof_anterior%3Abra+%2Bidx_atuacao_prof_anterior%3Asu+%2Bidx_atuacao_prof_anterior%3Asc+%2Bidx_nme_inst_ativ_prof%3Auniversidade+federal+de+santa+catarina++++++%2Bidx_particao%3A1+%2Bidx_nacionalidade%3Ae%29+or+%28+%2Bidx_grd_area_atua%3A%22ENGENHARIAS%22++++++++%2Bidx_atuacao_prof_anterior%3Abra+%2Bidx_atuacao_prof_anterior%3Asu+%2Bidx_atuacao_prof_anterior%3Asc+%2Bidx_nme_inst_ativ_prof%3Auniversidade+federal+de+santa+catarina++++++%2Bidx_particao%3A1+%2Bidx_nacionalidade%3Ab%29&analise=cv&tipoOrdenacao=null&paginaOrigem=index.do&mostrarScore=false&mostrarBandeira=true&modoIndAdhoc=null"
        self.headers_agent = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    def filter(self, id):
        data =  self.recovery_by_id(id)
        if not data:
            return 'No data'
        else:
            if "Universidade Federal de Santa Catarina" in data[0]:
                return True
            else:
                return False


    def bsobj(self):
        try:
            req = requests.get(self.atual_url, headers=self.headers_agent)
            return BeautifulSoup(req.content, 'html.parser')
        except Exception as e:
            return e

    def get_data(self,id=None):
        self.cursor.execute("""SELECT * FROM ids""")
        return self.cursor.fetchall()

    def recovery_by_id(self, id):
        sleep(4)
        max_data = []
        url = "http://buscatextual.cnpq.br/buscatextual/visualizacv.do?id=" + str(id)
        try:
            req = requests.get(url, headers=self.headers_agent)
            bsObj = BeautifulSoup(req.content, 'html.parser')
            description =  bsObj.findAll('p', class_='resumo')[0].text
            endereco = bsObj.find_all('div',{'class':'layout-cell layout-cell-9'})[2].text
            for children in bsObj.find_all('div',{'class':'title-wrapper'})[6].children:
                print(children.get_text)
                
                

        except Exception as e:
            return e

    def get_url(self):
        return self.atual_url

    def get_id(self, bsobj):
        ids_array = bsobj.findAll('li')
        ids = [[x.a.get('href')[24:34], x.a.text] for x in ids_array]
        return ids

    def next_page(self, pageNum):
        url_writable = "http://buscatextual.cnpq.br/buscatextual/busca.do?metodo=forwardPaginaResultados&registros=" + \
            str(pageNum)+";10&query=%28+%2Bidx_grd_area_atua%3A%22ENGENHARIAS%22++++++++%2Bidx_atuacao_prof_anterior%3Abra+%2Bidx_atuacao_prof_anterior%3Asu+%2Bidx_atuacao_prof_anterior%3Asc+%2Bidx_nme_inst_ativ_prof%3Auniversidade+federal+de+santa+catarina++++++%2Bidx_particao%3A1+%2Bidx_nacionalidade%3Ae%29+or+%28+%2Bidx_grd_area_atua%3A%22ENGENHARIAS%22++++++++%2Bidx_atuacao_prof_anterior%3Abra+%2Bidx_atuacao_prof_anterior%3Asu+%2Bidx_atuacao_prof_anterior%3Asc+%2Bidx_nme_inst_ativ_prof%3Auniversidade+federal+de+santa+catarina++++++%2Bidx_particao%3A1+%2Bidx_nacionalidade%3Ab%29&analise=cv&tipoOrdenacao=null&paginaOrigem=index.do&mostrarScore=false&mostrarBandeira=true&modoIndAdhoc=null"
        self.atual_url = url_writable

    def write(self, date):
        for i in date:
            self.cursor.executemany(
                """INSERT INTO ids (id,Nome) VALUES (?,?);""", [i])
        self.conn.commit()

    def recovery_id_recursive(self, lastPage):
        sleep(4)
        try:
            id_lattes = self.get_id(self.bsobj())
            print('recovered ids,names:' + str(id_lattes))
            self.write(id_lattes)
            lastPage += 10
            self.next_page(lastPage)
            return self.recovery_id_recursive(lastPage)
        except Exception as e:
            return e
 
        

os.system('clear')
lattes = extractLattes()
# print(lattes.recovery_id_recursive(0))
print(lattes.recovery_by_id("K4762759U5"))
#print(lattes.filter('K4258346A3'))

#for i in lattes.get_data():
    #print(str(i[1])+':'+str(lattes.filter(i[0])))
    #print(lattes.recovery_by_id(i[0]))