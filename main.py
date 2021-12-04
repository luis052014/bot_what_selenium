from time import sleep
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver
import re
from unicodedata import normalize
from selenium.webdriver.common.keys import Keys
import firebase_admin
from firebase_admin import credentials,firestore

cred = credentials.Certificate("resource/botv3.json")
filepath = ('resource/whatsapp_session.txt')
driver = webdriver

firebase_admin.initialize_app(cred)

def crear_driver_session():

    with open(filepath,mode='r', encoding='utf-8') as fp:
        for cnt, line in enumerate(fp):
            if cnt == 0:
                executor_url = line
            if cnt == 1:
                session_id = line

    def new_command_execute(self, command, params=None):
        if command == "newSession":
            # Mock the response
            return {'success': 0, 'value': None, 'sessionId': session_id}
        else:
            return org_command_execute(self, command, params)

    org_command_execute = RemoteWebDriver.execute

    RemoteWebDriver.execute = new_command_execute

    new_driver = webdriver.Remote(command_executor=executor_url, desired_capabilities={})
    new_driver.session_id = session_id

    RemoteWebDriver.execute = org_command_execute

    return new_driver

def buscar_chats():
    print("BUSCANDO CHATS")
    if len(driver.find_elements_by_class_name("zaKsw")) == 0:
        print("CHAT ABIERTO")
        message = identificar_mensaje()
        if message != None:
            return True
        
    chats = driver.find_elements_by_class_name("_3m_Xw")
    for chat in chats:
        sleep(1)
        print("DETECTANDO MENSAJES SIN LEER")
        element_name = chat.find_elements_by_class_name("zoWT4")
        name = element_name[0].text.lower().strip()
        chats_mensajes = chat.find_elements_by_class_name("_1i_wG")
                
        if len(chats_mensajes) == 0:
            #print("Ningun mensaje sin leer")
            continue

                

        print("IDENTIFICANDO CONTACTO")

        firestore_db = firestore.client()
        snapshots = firestore_db.collection('contacto').where('nombre','==', name).get()
        if not snapshots:
            print(name," NO AUTORIZADO")
            continue
        else:
            print(name, "AUTORIZADO PARA SER ATENDIDO POR BOT")
                
            chat.click()
            return True
            
    

    
    return False

    
    


    
def normalizar(message: str):
    # -> NFD y eliminar diacríticos
    message = re.sub(
        r"([^n\u0300-\u036f]|n(?!\u0303(?![\u0300-\u036f])))[\u0300-\u036f]+", r"\1", 
        normalize( "NFD", message), 0, re.I
    )

    # -> NFC
    return normalize( 'NFC', message)

def identificar_mensaje():
    elemnt_box_messagge = driver.find_elements_by_class_name("Nm1g1")

    posicion = len(elemnt_box_messagge) -1

    color = elemnt_box_messagge[posicion].value_of_css_property("background-color")
    print(color)
    if color == "rgba(255, 255, 255, 1)" or color == "rgba(5, 97, 98, 1)":
        print("CHAT ATENDIDO")

        
        return

    element_message = elemnt_box_messagge[posicion].find_elements_by_class_name("_1Gy50")
    message = element_message[0].text.lower().strip()
    print("MENSAJE RECIBIDO:", message)

    return normalizar(message)

def preparar_respuesta(message :str):
    print("PREPARANDO RESPUESTA")

    if message.__contains__("HOLA AMOR"):
        response = "Hola amor, como estás <3"
    elif message.__contains__("QUE HACES"):
        response = "Solo pensar en ti, y tu que haces?."
    elif message.__contains__("TE QUIERO CHUPAR EL PITO"):
        response = "Cuando quieras mi amor"
    elif message.__contains__("QUIERO QUE ME FOLLES"):
        response = "oooh"
    elif message.__contains__("TE AMO"):
        response = "Tambien te amo mucho mi amor"
    else:
        response = "sigo aprendiendo vocabulario, Hola soy un bot programado para enviar mensajes automaticamente hecho por _by_luis_salas_ , "

    return response

def procesar_mensaje(message :str):
    chatbox = driver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div/div/div[2]/div[1]')
    response = preparar_respuesta(message)
    chatbox.send_keys(response,Keys.ENTER)

def whatsapp_boot_init():
    global driver
    driver = crear_driver_session()

    while True:
        if not buscar_chats():
            sleep(1)
            continue
        
        message = identificar_mensaje()

        if message == None:
            continue

        procesar_mensaje(message)


if __name__ == '__main__':
    whatsapp_boot_init()
