# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
import sqlite3
import csv
import os
from time import sleep
import pandas as pd 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class extractLattes:
    def __init__(self, url=None):
        
        self.ids = []
        self.conn = sqlite3.connect("/home/lab-pesquisa/Desktop/AGU-CTC/ids.db")
        self.cursor = self.conn.cursor()
        self.atual_url = "http://buscatextual.cnpq.br/buscatextual/busca.do?metodo=forwardPaginaResultados&registros=10;10&query=%28%2Bidx_assunto%3A+%28%22+universidade+federal+de+santa+catarina%22%29++%2Bidx_atuacao_prof_anterior%3Abra+%2Bidx_atuacao_prof_anterior%3Asu+%2Bidx_atuacao_prof_anterior%3Asc+%2Bidx_nme_inst_ativ_prof%3Auniversidade+federal+de+santa+catarina++++++%2Bidx_particao%3A1+%2Bidx_nacionalidade%3Ae%29+or+%28%2Bidx_assunto%3A+%28%22+universidade+federal+de+santa+catarina%22%29++%2Bidx_atuacao_prof_anterior%3Abra+%2Bidx_atuacao_prof_anterior%3Asu+%2Bidx_atuacao_prof_anterior%3Asc+%2Bidx_nme_inst_ativ_prof%3Auniversidade+federal+de+santa+catarina++++++%2Bidx_particao%3A1+%2Bidx_nacionalidade%3Ab%29&analise=cv&tipoOrdenacao=null&paginaOrigem=index.do&mostrarScore=true&mostrarBandeira=true&modoIndAdhoc=null"
        self.headers_agent = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    def get_name_by_department(self, depart):
        names = pd.read_excel("prof_CTC.xlsx", sheet_name=depart)
        return names["Nome"]

    def serch_by_name(self, name):
        url = "http://buscatextual.cnpq.br/buscatextual/busca.do"
        driver = webdriver.Chrome('/usr/bin/chromedriver')
        driver.get(url)
        text_fild = driver.find_element_by_id("textoBusca")
        text_fild.send_keys(name)
        driver.find_element_by_id('botaoBuscaFiltros').click()
        
        
            

        
        #print(driver.page_source)


    def bsobj(self, url):
        sleep(5)
        try:
            req = requests.get(url, headers=self.headers_agent)
            return BeautifulSoup(req.content, 'html.parser')
        except Exception as e:
            print(e)
            return e


    def recovery_by_id(self, id_lattes):
        for i in id_lattes:
            if self.check_id(i[0]):
                print("id já esta na base")
            else:
                sleep(6)
                url = "http://buscatextual.cnpq.br/buscatextual/visualizacv.do?id=" + str(i[0])
                try:
                    name = i[1]
                    req = requests.get(url, headers=self.headers_agent)
                    bsObj = BeautifulSoup(req.content, 'html.parser')
                    resumo =  bsObj.find('p', class_='resumo').text
                    endereco = bsObj.find_all('div',{'class':'title-wrapper'})[2].text
                    empresa = bsObj.find('div',{'class':'inst_back'}).text
                    print([i[0],empresa,endereco])
                    self.write([i[0],name,empresa,endereco,resumo])
                except Exception as e:
                    return e

    def get_url(self):
        return self.atual_url

    def check_id(self,id_lattes):
        self.cursor.execute("""SELECT id FROM ids""")
        date = self.cursor.fetchall()
        for i in date:
            if i[0]==id_lattes:
                return True
        return False

    def get_id(self, bsobj):
        ids_array = bsobj.findAll('li')
        ids = [[x.a.get('href')[24:34], x.a.text] for x in ids_array]
        return ids

    def next_page(self, pageNum):
        #url_writable = "http://buscatextual.cnpq.br/buscatextual/busca.do?metodo=forwardPaginaResultados&registros="+str(pageNum)+";10&query=%28%2Bidx_assunto%3A+%28%22universidade+federal+de+santa+catarina+%22%29+%2Bidx_assunto%3A%28centro+de+tecnologia+florianopolis+ufsc+ctc+%29+%2Bidx_grd_area_atua%3A%22ENGENHARIAS%22+++++++++++++++++%2Bidx_particao%3A1+%2Bidx_nacionalidade%3Ae%29+or+%28%2Bidx_assunto%3A+%28%22universidade+federal+de+santa+catarina+%22%29+%2Bidx_assunto%3A%28centro+de+tecnologia+florianopolis+ufsc+ctc+%29+%2Bidx_grd_area_atua%3A%22ENGENHARIAS%22+++++++++++++++++%2Bidx_particao%3A1+%2Bidx_nacionalidade%3Ab%29&analise=cv&tipoOrdenacao=null&paginaOrigem=index.do&mostrarScore=true&mostrarBandeira=true&modoIndAdhoc=null"    
        url_writable = "http://buscatextual.cnpq.br/buscatextual/busca.do?metodo=forwardPaginaResultados&registros="+str(pageNum)+";10&query=%28%2Bidx_assunto%3A+%28%22+universidade+federal+de+santa+catarina%22%29++%2Bidx_atuacao_prof_anterior%3Abra+%2Bidx_atuacao_prof_anterior%3Asu+%2Bidx_atuacao_prof_anterior%3Asc+%2Bidx_nme_inst_ativ_prof%3Auniversidade+federal+de+santa+catarina++++++%2Bidx_particao%3A1+%2Bidx_nacionalidade%3Ae%29+or+%28%2Bidx_assunto%3A+%28%22+universidade+federal+de+santa+catarina%22%29++%2Bidx_atuacao_prof_anterior%3Abra+%2Bidx_atuacao_prof_anterior%3Asu+%2Bidx_atuacao_prof_anterior%3Asc+%2Bidx_nme_inst_ativ_prof%3Auniversidade+federal+de+santa+catarina++++++%2Bidx_particao%3A1+%2Bidx_nacionalidade%3Ab%29&analise=cv&tipoOrdenacao=null&paginaOrigem=index.do&mostrarScore=true&mostrarBandeira=true&modoIndAdhoc=null"
        self.atual_url = url_writable


    def write(self, date):
        try:
            self.cursor.executemany("""INSERT INTO ids (id,nome,empresa,endereço,resumo) VALUES (?,?,?,?,?);""", [date])
            self.conn.commit()
            return "dado inserido no banco com sucesso"
        except Exception as e:
            print(e)

    def recovery_id_recursive(self, lastPage):
        sleep(4)
        try:
            id_lattes = self.get_id(self.bsobj())
            print('recovered ids,names:' + str(id_lattes))
            self.recovery_by_id(id_lattes)
            lastPage += 10
            self.next_page(lastPage)
            return self.recovery_id_recursive(lastPage)
        except Exception as e:
            return e
 
        

os.system('clear')
lattes = extractLattes()
print(lattes.serch_by_name("Jose Luis Almada Guntzel"))
#print(lattes.recovery_id_recursive(0))
#print(lattes.check_id('K4795324H4'))
#print(lattes.recovery_by_id("K4762759U5"))
#print(lattes.filter('K4762759U5'))

# for i in lattes.get_data():
#     #print(str(i[1])+':'+str(lattes.filter(i[0])))
#     lattes.recovery_by_id(i[0])