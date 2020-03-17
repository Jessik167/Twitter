# -*- coding: utf-8 -*-
import time
import requests
from selenium import webdriver
from urllib.parse import quote
import Controlador as c
import Vista as v

def strip_spaces(text): 
    text = text.replace("\n", "")
    text = text.replace("'", "")
    return text

def is_downloadable(url):
    """
    Does the url contain a downloadable resource
    """
    try:
        try:
            h = requests.head(url, allow_redirects=True, timeout=5)
        except:
            return False
        header = h.headers
        content_type = header.get('content-type')
        #print(content_type.lower())
        if 'text' in content_type.lower():
            return False
        if 'html' in content_type.lower():
            return False
        if 'pdf' in content_type.lower():
            return False
        if 'application' in content_type.lower():
            return True
        if 'audio' in content_type.lower():
            return True
        if 'mpeg' in content_type.lower():
            return True
        return False
    except:
        return False
    


c.crea_tabla()
Artistas = c.artist_itunes()
for art in Artistas:
    search_word = quote(art[0] + ' descarga directa lang:es')
    #print(art[0])
    #print(search_word)
    url = r'https://twitter.com/search?q='+ str(search_word) +'&src=typed_query'
    #url = r'https://twitter.com/search?q=Jennifer%20Lopez%20descarga%20directa%20lang%3Aes&src=typed_query'
    driver = webdriver.Chrome('C:\\Users\\APDIF\\Desktop\\chromedriver.exe')
    #driver
    driver.get(url)
    try:
        driver.find_element_by_css_selector("input.text-input.email-input.js-signin-email").send_keys('jguerrero@apdif.com.mx')
        driver.find_element_by_name("session[password]").send_keys('$Apd1f')
        driver.find_element_by_css_selector("input.EdgeButton.EdgeButton--primary.EdgeButton--medium.submit.js-submit").click()
    except:
        pass
    time.sleep(5)
    i = 0
    tam_pag = driver.execute_script("return document.body.scrollHeight")
    while i <= tam_pag:
        tope_pag = driver.execute_script("return document.documentElement.scrollTop")
        ## TOMA LOS TWEETS
        for article in driver.find_elements_by_css_selector('article'):
            le = len(driver.find_elements_by_css_selector('article'))
            Hash = ""
            try:
                href = article.find_element_by_css_selector('div.css-901oao.r-hkyrab.r-1qd0xha.r-a023e6.r-16dba41.r-ad9z0x.r-bcqeeo.r-bnwqim.r-qvutc0 > a').get_attribute('title')
                if is_downloadable(href) == True:
                    c.crea_tablaUsuario()
                    try:
                        usuario = article.find_element_by_css_selector('div.css-901oao.css-bfa6kz.r-1re7ezh.r-18u37iz.r-1qd0xha.r-a023e6.r-16dba41.r-ad9z0x.r-bcqeeo.r-qvutc0 > span').text
                        texto = article.find_element_by_css_selector('div.css-901oao.r-hkyrab.r-1qd0xha.r-a023e6.r-16dba41.r-ad9z0x.r-bcqeeo.r-bnwqim.r-qvutc0').text
                        texto = strip_spaces(texto)
                        if texto.find(art[0]) != -1:
                            if texto.find(usuario) != -1:
                                id_usuario = c.existe_usuario(usuario)
                                fecha = article.find_element_by_css_selector('time').text
                                try:
                                    for a in article.find_elements_by_css_selector('article span.r-18u37iz > a'):
                                        Hash += a.text + ","
                                except:
                                    pass
                                print('------------------------------------------------------------------------')
                                print('Fecha: ' + fecha)
                                print('Usuario: ' + usuario)
                                print('Infringing: ' + href)
                                print('Referer: ' + url)
                                print('Hashtag: ' + Hash)
                                print('Texto: ' + '\n' +texto)
                                print('------------------------------------------------------------------------')
                                if c.existe_inf(href) == False:
                                    if id_usuario == False:
                                        c.inserta_Usuario(usuario)
                                        v.muestra_item_guardado(usuario)
                                        id_usuario = c.existe_usuario(usuario)
                                    c.inserta_item_nueva(id_usuario, texto, Hash, url, href, fecha)
                                    v.muestra_item_guardado(href)
                    except:
                        pass
            except:
                pass
        i += 600
        driver.execute_script('window.scrollBy(' + str(tope_pag) + ',' + str(i) + ')')
        #print('HREF: ' + href)
    #time.sleep(1)
    driver.close()