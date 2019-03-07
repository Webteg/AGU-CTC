#!./env/bin/python3
# -*- coding: utf-8 -*-
from captcha import solveCaptcha, ImageCaptcha
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


class extractLattes:
    def __init__(self, url=None):
        
        self.conn = sqlite3.connect("professores.db")
        self.cursor = self.conn.cursor()
        self.headers_agent = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    def get_sqlData(self, query, arg ):
        try:
            self.cursor.execute(query, (arg,))
        except Exception as e:
            return e
        return self.cursor.fetchall()

    def serch_by_name(self, name):
        url = "http://buscatextual.cnpq.br/buscatextual/busca.do"
        
        options = se.webdriver.ChromeOptions()
        options.add_argument('headless')
        driver = se.webdriver.Chrome('/home/lab-pesquisa/Desktop/projetos/AGU-CTC/chromedriver', chrome_options=options)
        driver.get(url)
        sleep(3)

        text_fild = driver.find_element_by_id("textoBusca")
        text_fild.send_keys(name)
        driver.find_element_by_id('buscarDemais').click()
        driver.find_element_by_id('botaoBuscaFiltros').click()
        html = driver.page_source
        bs = BeautifulSoup(html, "html.parser")
        id_html =  bs.findAll('li')
        # if id_html==[]:
        #     return False
        # else:
        #     return [str(id_html)[41:51],name]
        lattesId = str(id_html)[41:51]
        print(lattesId)
        driver.get("http://buscatextual.cnpq.br/buscatextual/visualizacv.do?id=" + lattesId)
        urlImage = driver.find_element_by_id("image_captcha").get_attribute("src")
        print(urlImage)
        # captchaNum = ImageCaptcha(urlImage)
        # print(captchaNum, urlImage)
        # text_fild = driver.find_element_by_id("informado")
        # text_fild.send_keys(captchaNum)
        # driver.find_element_by_id('btn_validar_captcha').click()
        # sleep(4)
        # return driver.page_source 



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
            print(req.content)
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
        
            #return [artigos_publicados,len(artigos_publicados),linhas_de_pesquisa, projetos_em_desenvolvimento,area_atuacao,patentes,len(patentes),orientacoes]
            return artigos_publicados
          
        except Exception as e:
                return e
    
    def set_sqlData(self,query,args):
        try:
            self.cursor.execute(query,args)
            self.conn.commit()
        except Exception as e:
            return e

    def set_artigos(self, data, id_matricula):
        try:
            for i in data:
                self.set_sqlData('ISERT INTO artigos(matricula_id,artigo) VALUES (?,?)', ([i,id_matricula], ))
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
    names = lattes.get_sqlData("SELECT nome, matricula FROM professores WHERE departamento=? AND lattes=1",arg=depart_name)
    for i in names:
        
        recovery_id = lattes.serch_by_name(i[0])
        print(recovery_id)
        # lattes_infos =  lattes.recovery_by_id(recovery_id)
        # print(lattes_infos)
        #lattes.set_artigos(lattes_infos,i[1])
        

