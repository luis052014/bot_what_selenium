from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

browser=webdriver.Firefox()



def seleccionarChat(nombre):
    buscando= True
    while buscando:
        print("bUSCANDO CHAT")
        time.sleep(2)
        elements = browser.find_elements_by_tag_name("span")
        for element in elements:
            if element.text == nombre:
                print("Fany amor encontrada")
                buscando = False
                element.click()
                break

def enviarMensaje(mensaje):
    chatbox= browser.find_element_by_xpath('/html/body/div[1]/div[1]/div[1]/div[4]/div[1]/footer/div[1]/div/div/div[2]/div[1]/div/div[2]')
    chatbox.send_keys(mensaje)
    chatbox.send_keys(Keys.ENTER)

def validaQR():
    try:
        element = browser.find_element_by_tag_name("canvas")
    except:
        return False
    return True

def botWhatsapp():
    browser.get('https://web.whatsapp.com/')
    time.sleep(5)

    espera = True

    while espera == True:
        print("ESTOY ESPERANDO")
        espera = validaQR()
        time.sleep(2)
        if espera == False:
            print("SE AUTENTICÓ")
            break
    mensajear= "Fanyamor"
    seleccionarChat(mensajear)
    mensaje="Hola amor como estas"
    enviarMensaje(mensaje)




botWhatsapp()
