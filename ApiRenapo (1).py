import requests  # importing requests module
import json  # importing json module for json handling
import deathbycaptcha
# import Customdeathbycaptcha  # importing deathbycaptcha for solving recaptcha
from datetime import datetime
from pprint import pprint
from sys import path
from twocaptcha import TwoCaptcha
import ssl
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import time
# from proxy_service import proxy_SP_1
import time

class ApiRenapo(object):
    """docstring for ApiRenapo"""

    def __init__(self):
        super(ApiRenapo, self).__init__()
        self.TOTAL_REQUEST = 3

    # def solverecaptcha(self):  # for solving recaptcha returns captcha text
    #     username = "Garangou2145" #  # deathbycaptcha username
    #     password = "mJQfZ!aUcyGu3f8" # 
    #     sitekey = "6Lfi0jcpAAAAAPfBiQkGzQR3gv8mDRkqPDHAy8hS"  # site key for getting/solving recaptcha
    #     pageurl = "https://www.gob.mx/v1/renapoCURP/consulta"  # site url for getting/solving recaptcha
    #     Captcha_dict = {  # json object that stores google site key and page url
    #         'googlekey': sitekey,
    #         'pageurl': pageurl
    #     }
    #     json_Captcha = json.dumps(Captcha_dict)  # Parsing object into a json string.
    #     # client = Customdeathbycaptcha.SocketClient(username, password)  # setting up Customdeathbycaptcha client
    #     for x in range(2):
    #         try:  # trying to solve captcha
    #             client = deathbycaptcha.HttpClient(username, password)  # setting up deathbycaptcha client
    #             captcha = client.decode(type=4, token_params=json_Captcha)  # downloading recaptcha and solving it
    #             if captcha:  # if recaptcha is not null
    #                 return (captcha["text"])  # returns captcha text
    #                 break
    #         except Exception as e:  # if any error occurs
    #             print("error")  # printing Error
    #             print(e)  # printing Error
    #             time.sleep(2)  # waiting for Error
    #             if x == 1:
    #                 return 'error'
        
    def solverecaptcha(self):
        api_key = 'c0120096fd0628323bfcd7773825a0e'
        for x in range(3):
            try:

                solver = TwoCaptcha(api_key)
                result = solver.recaptcha(
                        sitekey='6Lfi0jcpAAAAAPfBiQkGzQR3gv8mDRkqPDHAy8hS',
                        url='https://www.gob.mx/v1/renapoCURP/consulta',
                        )
                return result["code"]
            except Exception as e:  # if any error occurs
                print("error")  # printing Error
                print(e)  # printing Error
                time.sleep(2)  # waiting for Error
                if x == 2:
                    return 'error'
                

    def get_cookies(self,curl_val):

        ssl._create_default_https_context = ssl._create_unverified_context

        # Set Chrome options
        options = uc.ChromeOptions()
        options.add_argument('--headless=new')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-setuid-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-accelerated-2d-canvas')
        options.add_argument('--disable-gpu')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')

        # Launch browser with the above options
        driver = uc.Chrome(options=options)

        # Go to the target URL
        driver.get('https://www.gob.mx/curp/')

        # Wait for the page to load and the input field to appear
        time.sleep(5)

        # Find the input field and enter the CURP value
        curp_input = driver.find_element(By.ID, 'curpinput')
        curp_input.send_keys(curl_val)

        # Simulate human interaction with a small delay before submission
        time.sleep(2)

        # Find the "Buscar" (submit) button and click it
        submit_button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
        submit_button.click()

        # Wait for a while to let the page load
        time.sleep(5)
        vals = [i["value"] for i in driver.get_cookies() if i["name"]=='_abck'][0]
        driver.close()

        return vals

    def request(self, curp):  # request to url and returns data using requests library
        
        max_retries = 3
        delay = 5  # seconds
        backoff_factor = 2
        for attempt in range(1, max_retries + 1):
            with open('/Users/muhammadthanish/Desktop/datagram/testcookie.txt', 'r') as file:
                content = file.read()
                file.close()
            header = {  # setting up header for request
                "authority": "www.gob.mx",
                "path": "/ v1 / renapoCURP / consulta",
                "scheme": "https",
                "origin": "https://www.gob.mx",
                'referer': "https://www.gob.mx/",
                'cookie': f'_abck={content}',
                "accept": "application/json",
                "accept-language": "en-US,en;q=0.9",
                "access-control-allow-headers": "Origin, X-Requested-With, Content-Type, Accept",
                "access-control-allow-origin": "*",
                "content-type": "application/json",
                "sec-ch-ua": "\" Not;A Brand\";v=\"99\", \"Google Chrome\";v=\"91\", \"Chromium\";v=\"91\"",
                "sec-ch-ua-mobile": "?0",
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "same-origin",
                "x-requested-with": "XMLHttpRequest",
                "referrerPolicy": "origin",
                "credentials": "include"

            }
            cap = self.solverecaptcha()
            data = {  # setting up payload for with recaptcha text
                "curp": curp,  # setting up curp
                "ip": "127.0.0.1",
                "token": cap,  # setting up recaptcha text
                "tipoBusqueda": "curp"
            }
            try:

                s = requests.Session()
                res = s.post("https://www.gob.mx/v1/renapoCURP/consulta", headers=header,json=data, timeout=20)
                if res.status_code == 200:
                    return res
                    # coo = dict(res.cookies)
                    # with open('/Users/muhammadthanish/Desktop/datagram/testcookie.txt', 'w') as file:
                    #     file.write(coo["_abck"])
                    #     file.close()
            except:
                try:
                    print("cookies expired we so taking cookies from browser...")
                    #cap = self.solverecaptcha()
                    coo_val = self.get_cookies(curp)
                    with open('/Users/muhammadthanish/Desktop/datagram/testcookie.txt', 'w') as file:
                        file.write(coo_val)
                        file.close()
                    if attempt < max_retries:
                        #wait_time = delay * (backoff_factor ** (attempt - 1))
                        wait_time = 3
                        print(f"Retrying in {wait_time} seconds...")
                        time.sleep(wait_time)
                except:

                    res = ""
        return res   # returning xml/html or json data

    def getDataByCurp(self, curp, getRfc=False):
        response = self.request(curp)
        dict_return = self.getDictResponse(response, curp, getRfc)

        return dict_return

    def getDictResponse(self, response, curp, getRfc):
        dict_return = self.__getDict()
        if response == 'error':
                dict_return['status'] = 'noOk'
                dict_return['statusMessage'] = 'Error en DbC'
                return dict_return

        try:
            if response.status_code == 200:
                response_json = response.json()
                if 'mensaje' in response_json and 'datos ingresados no son correctos' in response_json['mensaje']:
                    dict_return['status'] = 'ok'
                    dict_return['statusMessage'] = 'Curp No Existente'
                    return dict_return
                else:
                    response_json = response_json['registros'][0]
            else:
                dict_return['status'] = 'noOk'
                dict_return['statusMessage'] = 'Error en peticion ' + str(response.status_code) + ' ' + str(
                    response.reason)
                return dict_return


        except Exception as e:
            dict_return['status'] = 'noOk'
            dict_return['statusMessage'] = 'Error en peticion ' + str(e)
            return dict_return

        if not 'docProbatorio' in response_json:
            dict_return['CURP'] = curp
            dict_return['generado'] = curp
            dict_return['validado'] = datetime.now()
            dict_return['status'] = 'ok'
            dict_return['statusMessage'] = 'Curp No Existente'
        else:
            dict_return['AnioReg'] = response_json["datosDocProbatorio"][
                "anioReg"] if "anioReg" in response_json["datosDocProbatorio"] else ''
            dict_return['Apellido1'] = response_json["primerApellido"]
            dict_return['Apellido2'] = response_json["segundoApellido"]
            dict_return['CURP'] = response_json["curp"]
            dict_return['CveMunicipioReg'] = response_json["datosDocProbatorio"][
                "claveMunicipioRegistro"] if "claveMunicipioRegistro" in response_json["datosDocProbatorio"] else ''
            dict_return['DocProbatorio'] = response_json["docProbatorio"]
            dict_return['FechNac'] = response_json["fechaNacimiento"]
            dict_return['Nombres'] = response_json["nombres"]
            dict_return['NumActa'] = response_json["datosDocProbatorio"]["numActa"] if "numActa" in response_json[
                "datosDocProbatorio"] else ''
            dict_return['NumEntidadReg'] = response_json["datosDocProbatorio"][
                "claveEntidadRegistro"] if "claveEntidadRegistro" in response_json["datosDocProbatorio"] else ''
            dict_return['Sexo'] = "M" if "MUJER" in response_json["sexo"] else "H"
            dict_return['StatusCurp'] = response_json["statusCurp"]
            dict_return['generado'] = curp
            dict_return['validado'] = datetime.now()
            dict_return['status'] = 'ok'
            dict_return['statusMessage'] = 'ok'

        if getRfc:
            dict_return['rfc'] = response_json['rfc'] if 'rfc' in response_json else ''
            dict_return['validado_rfc'] = response_json['rfc_valid'] if 'rfc_valid' in response_json and response_json[
                "rfc_valid"] else False

        return dict_return

    def __getDict(self):
        return {
            'AnioReg': '',
            'Apellido1': '',
            'Apellido2': '',
            'CURP': '',
            'CveMunicipioReg': '',
            'DocProbatorio': '',
            'FechNac': '',
            'Nombres': '',
            'NumActa': '',
            'NumEntidadReg': '',
            'Sexo': '',
            'StatusCurp': '',
            'generado': '',
            'validado': '',
            'status': '',
            'statusMessage': '',
        }


if __name__ == '__main__':
    curp = ApiRenapo()
    with open('/Users/muhammadthanish/Downloads/1000 Curps.txt', 'r') as file:
        # Read all lines and strip the newline characters
        array = [line.strip() for line in file]
    data_arr = []
    cnt = 0
    for i in array[200:500]:
        print(cnt)
        cnt+=1
        print(i)
        aaa = curp.getDataByCurp(i)
        print(aaa)
        data_arr.append(aaa)
    import csv; [csv.DictWriter(f, fieldnames=data_arr[0].keys()).writerows(data_arr) for f in [open('output2.csv', 'w', newline='')]]
    print("aaaaaa")
    print("bbbbbbb")