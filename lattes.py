# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
import sqlite3
import csv
import os
from time import sleep
import selenium as se
import pandas as pd 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class extractLattes:
    def __init__(self, url=None):
        
        self.ids = []
        self.conn = sqlite3.connect("professores.db")
        self.cursor = self.conn.cursor()
        self.atual_url = "http://buscatextual.cnpq.br/buscatextual/busca.do?metodo=forwardPaginaResultados&registros=10;10&query=%28%2Bidx_assunto%3A+%28%22+universidade+federal+de+santa+catarina%22%29++%2Bidx_atuacao_prof_anterior%3Abra+%2Bidx_atuacao_prof_anterior%3Asu+%2Bidx_atuacao_prof_anterior%3Asc+%2Bidx_nme_inst_ativ_prof%3Auniversidade+federal+de+santa+catarina++++++%2Bidx_particao%3A1+%2Bidx_nacionalidade%3Ae%29+or+%28%2Bidx_assunto%3A+%28%22+universidade+federal+de+santa+catarina%22%29++%2Bidx_atuacao_prof_anterior%3Abra+%2Bidx_atuacao_prof_anterior%3Asu+%2Bidx_atuacao_prof_anterior%3Asc+%2Bidx_nme_inst_ativ_prof%3Auniversidade+federal+de+santa+catarina++++++%2Bidx_particao%3A1+%2Bidx_nacionalidade%3Ab%29&analise=cv&tipoOrdenacao=null&paginaOrigem=index.do&mostrarScore=true&mostrarBandeira=true&modoIndAdhoc=null"
        self.headers_agent = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    def get_name_by_department(self, depart):
        names = pd.read_excel("prof_CTC.xlsx", sheet_name=depart)
        return names["Nome"]

    def serch_by_name(self, name):
        url = "http://buscatextual.cnpq.br/buscatextual/busca.do"
        options = se.webdriver.ChromeOptions()
        options.add_argument('headless')
        driver = se.webdriver.Chrome(chrome_options=options)
        driver.get(url)
        sleep(2)

        text_fild = driver.find_element_by_id("textoBusca")
        text_fild.send_keys(name)
        driver.find_element_by_id('buscarDemais').click()
        driver.find_element_by_id('botaoBuscaFiltros').click()
        html = driver.page_source
        bs = BeautifulSoup(html, "html.parser")
        id_html =  bs.findAll('li')
        return [str(id_html)[41:51],name]


    def bsobj(self, url):
        sleep(5)
        try:
            req = requests.get(url, headers=self.headers_agent)
            return BeautifulSoup(req.content, 'html.parser')
        except Exception as e:
            print(e)
            return e


    def recovery_by_id(self, id_lattes):
        #sleep(6)
        #url = "http://buscatextual.cnpq.br/buscatextual/visualizacv.do?id="+str(id_lattes[0])
        try:
            #name = id_lattes[1]
            #req = requests.get(url, headers=self.headers_agent)
            file_html = open('html.txt','r')
            bsObj = BeautifulSoup(file_html.read(), 'html.parser')

            resumo =  bsObj.find('p', class_='resumo').text
            
            title_wrapper =[[x,x.a.h1.text] for x in  bsObj.findAll('div',{'class':'title-wrapper'}) if x.a is not None]
            #---------------------------------------------------------------------------------------------------#
            artigos = [ x[0] for x in title_wrapper if x[1]=='Produções'][0]
            artigos  =[ x.get_text() for x in artigos.findAll('div',{'class':'layout-cell-pad-5'}) if len(x.get_text())>10]
           #---------------------------------------------------------------------------------------------------#
            linhas_de_pesquisa =[ x[0] for x in title_wrapper if x[1]=='Linhas de pesquisa'][0]
            linhas_de_pesquisa = [ x.get_text() for x in linhas_de_pesquisa.findAll('div',{'class':'layout-cell-pad-5'}) if len(x.get_text())>10]
            #---------------------------------------------------------------------------------------------------#
            projetos_de_pesquisa =[ x[0] for x in title_wrapper if x[1]=='Projetos de pesquisa'][0]
            projetos_de_pesquisa = [ x.get_text() for x in projetos_de_pesquisa.findAll('div',{'class':'layout-cell-pad-5'}) if len(x.get_text())>15]
            #arrumar array 
            #---------------------------------------------------------------------------------------------------#
            projetos_em_desenvolvimento = [ x[0] for x in title_wrapper if x[1]=='Projetos de desenvolvimento'][0]
            projetos_em_desenvolvimento = [ x.get_text() for x in projetos_em_desenvolvimento.findAll('div',{'class':'layout-cell-pad-5'}) if len(x.get_text())>15]
            #arrumar array 
            #---------------------------------------------------------------------------------------------------#

            area_atuacao = [ x[0] for x in title_wrapper if x[1]=='Áreas de atuação'][0]
            area_atuacao = [ x.get_text() for x in area_atuacao.findAll('div',{'class':'layout-cell-pad-5'}) if len(x.get_text())>15]
           
             #---------------------------------------------------------------------------------------------------#

            #---------------------------------------------------------------------------------------------------#

            patentes = [ x[0] for x in title_wrapper if x[1]=='Patentes e registros'][0]
            patentes = [ x.get_text().replace('\t','').replace('\n','') for x in patentes.findAll('div',{'class':'layout-cell-pad-5'}) if len(x.get_text())>15]
           
             #---------------------------------------------------------------------------------------------------#

            orientacoes = [ x[0] for x in title_wrapper if x[1]=='Orientações'][0]
            orientacoes = [ x.get_text() for x in orientacoes.findAll('div',{'class':'layout-cell-pad-5'}) if len(x.get_text())>15]
           
             #---------------------------------------------------------------------------------------------------#

            


            print(orientacoes)




          
        except Exception as e:
                return e
                

    def check_id(self,id_lattes):
        self.cursor.execute("""SELECT id FROM ids""")
        date = self.cursor.fetchall()
        for i in date:
            if i[0]==id_lattes:
                return True
        return False

    def write(self, date):
        try:
            self.cursor.executemany("""INSERT INTO ids (id,nome,empresa,endereço,resumo) VALUES (?,?,?,?,?);""", [date])
            self.conn.commit()
            return "dado inserido no banco com sucesso"
        except Exception as e:
            print(e)

#'--------------------------------------------------------------------------'

    def get_url(self):
        return self.atual_url

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

    def get_id(self, bsobj):
        ids_array = bsobj.findAll('li')
        ids = [[x.a.get('href')[24:34], x.a.text] for x in ids_array]
        return ids

    def next_page(self, pageNum):
        #url_writable = "http://buscatextual.cnpq.br/buscatextual/busca.do?metodo=forwardPaginaResultados&registros="+str(pageNum)+";10&query=%28%2Bidx_assunto%3A+%28%22universidade+federal+de+santa+catarina+%22%29+%2Bidx_assunto%3A%28centro+de+tecnologia+florianopolis+ufsc+ctc+%29+%2Bidx_grd_area_atua%3A%22ENGENHARIAS%22+++++++++++++++++%2Bidx_particao%3A1+%2Bidx_nacionalidade%3Ae%29+or+%28%2Bidx_assunto%3A+%28%22universidade+federal+de+santa+catarina+%22%29+%2Bidx_assunto%3A%28centro+de+tecnologia+florianopolis+ufsc+ctc+%29+%2Bidx_grd_area_atua%3A%22ENGENHARIAS%22+++++++++++++++++%2Bidx_particao%3A1+%2Bidx_nacionalidade%3Ab%29&analise=cv&tipoOrdenacao=null&paginaOrigem=index.do&mostrarScore=true&mostrarBandeira=true&modoIndAdhoc=null"    
        url_writable = "http://buscatextual.cnpq.br/buscatextual/busca.do?metodo=forwardPaginaResultados&registros="+str(pageNum)+";10&query=%28%2Bidx_assunto%3A+%28%22+universidade+federal+de+santa+catarina%22%29++%2Bidx_atuacao_prof_anterior%3Abra+%2Bidx_atuacao_prof_anterior%3Asu+%2Bidx_atuacao_prof_anterior%3Asc+%2Bidx_nme_inst_ativ_prof%3Auniversidade+federal+de+santa+catarina++++++%2Bidx_particao%3A1+%2Bidx_nacionalidade%3Ae%29+or+%28%2Bidx_assunto%3A+%28%22+universidade+federal+de+santa+catarina%22%29++%2Bidx_atuacao_prof_anterior%3Abra+%2Bidx_atuacao_prof_anterior%3Asu+%2Bidx_atuacao_prof_anterior%3Asc+%2Bidx_nme_inst_ativ_prof%3Auniversidade+federal+de+santa+catarina++++++%2Bidx_particao%3A1+%2Bidx_nacionalidade%3Ab%29&analise=cv&tipoOrdenacao=null&paginaOrigem=index.do&mostrarScore=true&mostrarBandeira=true&modoIndAdhoc=null"
        self.atual_url = url_writable

#'--------------------------------------------------------------------------'

   
os.system('clear')
lattes = extractLattes()

#id_name = lattes.serch_by_name("Janaide Cavalcante Rocha")
date = lattes.recovery_by_id('id_name')
print(date)
#print(id_lattes)
#dados = lattes.recovery_by_id(id_lattes)
#print(dados)

