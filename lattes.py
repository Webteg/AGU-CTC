#!./env/bin/python3
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
import numpy as np
import matplotlib.pyplot as plt

class extractLattes:
    def __init__(self, url=None):
        
        self.conn = sqlite3.connect("professores.db")
        self.cursor = self.conn.cursor()
        self.headers_agent = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    def get_name_by_department(self, depart):
        self.cursor.execute("SELECT nome FROM professores WHERE departamento=?",(depart, ))
        return self.cursor.fetchall()

    def serch_by_name(self, name):
        url = "http://buscatextual.cnpq.br/buscatextual/busca.do"
        
        options = se.webdriver.ChromeOptions()
        options.add_argument('headless')
        driver = se.webdriver.Chrome(chrome_options=options)
        driver.get(url)
        #sleep(2)

        text_fild = driver.find_element_by_id("textoBusca")
        text_fild.send_keys(name)
        driver.find_element_by_id('buscarDemais').click()
        driver.find_element_by_id('botaoBuscaFiltros').click()
        html = driver.page_source
        bs = BeautifulSoup(html, "html.parser")
        id_html =  bs.findAll('li')
        return [str(id_html)[41:51],name]


    def bsobj(self, url):
        try:
            req = requests.get(url, headers=self.headers_agent)
            return BeautifulSoup(req.content, 'html.parser')
        except Exception as e:
            print(e)
            return e


    def recovery_by_id(self, id_lattes):
        sleep(2)
        url = "http://buscatextual.cnpq.br/buscatextual/visualizacv.do?id="+str(id_lattes[0])
        try:
            name = id_lattes[1]
            req = requests.get(url, headers=self.headers_agent)
            bsObj = BeautifulSoup(req.content, 'html.parser')
            resumo =  bsObj.find('p', class_='resumo').text
            title_wrapper =[[x,x.a.h1.text] for x in  bsObj.findAll('div',{'class':'title-wrapper'}) if x.a is not None]
            artigos_publicados = [ x[0] for x in title_wrapper if x[1] is not None and x[1]=="Produções"]
            if not artigos_publicados==[]:
                #artigos  =[ x.get_text() for x in artigos[0].findAll('div',{'class':'layout-cell-pad-5'}) if len(x.get_text())>10]
                artigos_publicados = [ x.get_text() for x in artigos_publicados[0].findAll('div',{'class':'artigo-completo'}) if len(x.get_text())>10]

            linhas_de_pesquisa =[ x[0] for x in title_wrapper if x[1]=='Linhas de pesquisa']
            if not linhas_de_pesquisa==[]:
                linhas_de_pesquisa = [ x.get_text() for x in linhas_de_pesquisa[0].findAll('div',{'class':'layout-cell-pad-5'}) if len(x.get_text())>10]

            projetos_de_pesquisa =[ x[0] for x in title_wrapper if x[1]=='Projetos de pesquisa']
            if not projetos_de_pesquisa==[]:
                projetos_de_pesquisa = [ x.get_text() for x in projetos_de_pesquisa[0].findAll('div',{'class':'layout-cell-pad-5'}) if len(x.get_text())>15]
                projetos_de_pesquisa = list(zip(projetos_de_pesquisa[::2], projetos_de_pesquisa[1::2]))

            projetos_em_desenvolvimento = [ x[0] for x in title_wrapper if x[1]=='Projetos de desenvolvimento']
            if not projetos_em_desenvolvimento == []:
                projetos_em_desenvolvimento = [ x.get_text() for x in projetos_em_desenvolvimento[0].findAll('div',{'class':'layout-cell-pad-5'}) if len(projetos_em_desenvolvimento)>0 and len(x.get_text())>15]
                projetos_em_desenvolvimento = list(zip(projetos_em_desenvolvimento[::2], projetos_em_desenvolvimento[1::2]))

            area_atuacao =[ x[0] for x in title_wrapper if x[1]=='Áreas de atuação']
            if not area_atuacao==[]:
                area_atuacao = [ x.get_text() for x in area_atuacao[0].findAll('div',{'class':'layout-cell-pad-5'}) if len(x.get_text())>15]
           
            patentes = [ x[0] for x in title_wrapper if x[1]=='Patentes e registros']
            if not patentes==[]:
                patentes = [ x.get_text().replace('\t','').replace('\n','') for x in patentes[0].findAll('div',{'class':'layout-cell-pad-5'}) if len(x.get_text())>15]
           
            orientacoes = [ x[0] for x in title_wrapper if x[1]=='Orientações']
            if not orientacoes==[]:
                orientacoes = [ x.get_text() for x in orientacoes[0].findAll('div',{'class':'layout-cell-pad-5'}) if len(x.get_text())>15]
        
            return [len(artigos_publicados),len(patentes), name]
          
        except Exception as e:
                return e
                

   

    def write(self, date):
        try:
            self.cursor.executemany("""INSERT INTO ids (id,nome,empresa,endereço,resumo) VALUES (?,?,?,?,?);""", [date])
            self.conn.commit()
            return "dado inserido no banco com sucesso"
        except Exception as e:
            print(e)


    def get_id(self, bsobj):
        ids_array = bsobj.findAll('li')
        ids = [[x.a.get('href')[24:34], x.a.text] for x in ids_array]
        return ids



departaments = ["ARQ","DAS","ECV","ELL","EGC","EMC","ENS","EPS","EQA","INE"]
   
os.system('clear')
lattes = extractLattes()
for depart_name in departaments:
    x=[]
    y=[]
    
    names = lattes.get_name_by_department(depart_name)
   

    for name in names:
        try:
            get_id = lattes.serch_by_name(name[0])
            
            if get_id[0] is None:
                print(get_id[1]+": Sem cadastro na plataforma lattes")
            else:
                date = lattes.recovery_by_id(get_id)
                print(date)
                # x.append(date[1])
                # y.append(date[0])
        except Exception as er:
            print(er)
    
    # plt.scatter(x, y)
    # plt.title('Dispersão: produção científica X patentes')
    # plt.show()