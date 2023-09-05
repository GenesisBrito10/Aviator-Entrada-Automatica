import datetime
import telebot
import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import tkinter as tk
from tkinter import ttk
import undetected_chromedriver as uc

class WebScraper:

    def __init__(self):
        # EDIT!

        self.game = "Aviator"
        self.token = '6240343377:AAHSgzfJiOl1ojjc1DhYyFTXls-OtI9R2bQ'
        self.chat_id = '-834547003'
        self.gales = 2
        self.link = '[Clique aqui!](blaze.com/r/0aJYR6)'
        self.options = uc.ChromeOptions()
        self.options.add_argument('--profile-directory=Default')
        self.options.add_argument("--disable-infobars")
        self.options.add_argument("--disable-logging")
        self.options.add_argument("--disable-login-animations")
        self.options.add_argument("--disable-notifications")
        self.options.add_argument("--disable-default-apps")
        self.options.add_argument("--disable-popup-blocking")
        #self.options.binary_location = "/usr/bin/google-chrome-stable"
        self.driver = None

        # MAYBE EDIT!
        self.win_results = 0
        self.loss_results = 0
        self.max_hate = 0
        self.win_hate = 0
        self.stop = 1
        self.win = 1

        # NO EDIT!
        self.count = 0
        self.analisar = True
        self.alvo = 1.5
        self.message_delete = False
        self.bot = telebot.TeleBot(token=self.token, parse_mode='MARKDOWN')
        self.date_now = str(datetime.datetime.now().strftime("%d/%m/%Y"))
        self.check_date = self.date_now
        self.saldo = 0.0
        self.janela = tk.Tk()
        self.janela.title("Aviator Bot")

        self.combo = ttk.Combobox(self.janela, values=list(range(0, 101)))
        self.combo.set("Valor Entrada:")
        self.combo.pack()

        self.combo2 = ttk.Combobox(self.janela, values=list(range(0, 101)))
        self.combo2.set("Stop Win:")
        self.combo2.pack()

        self.combo3 = ttk.Combobox(self.janela, values=list(range(0, 101)))
        self.combo3.set("Stop Loss:")
        self.combo3.pack()

        """ self.combo4 = ttk.Combobox(self.janela, values=list(range(9)))
        self.combo4.set("Total de Gales:")
        self.combo4.pack() """

        self.botao = tk.Button(
            self.janela, text="Executar", command=self.executar)
        self.botao.pack()

        self.janela.mainloop()

    def initialize_browser(self):
        self.driver = uc.Chrome(
            )
        return self.driver

    def pegar_resultado(self):
        elements = self.driver.find_elements(
            By.CSS_SELECTOR, ".payouts-block .payout.ng-star-inserted")

        # Lê os textos de cada elemento e os armazena em uma lista
        multipliers = []
        for element in elements[:10]:
            try:
                multiplier = float(element.text.replace('x', ''))
                multipliers.append(multiplier)
            except ValueError:
                pass

        return multipliers
    
    def pegar_saldo(self):
        saldo = self.driver.find_element(By.XPATH,'/html/body/app-root/app-game/div/div[1]/div[1]/app-header/div/div[2]/div/div[1]/div/span[1]').text
        return saldo
    
    def results(self):

        if self.win_results + self.loss_results != 0:
            a = 100 / (self.win_results + self.loss_results) * self.win_results
        else:
            a = 0
        self.win_hate = (f'{a:,.2f}%')

        self.bot.send_message(chat_id=self.chat_id, text=(f'''
► PLACAR GERAL = ✅{self.win_results}  |  🚫{self.loss_results} 
► Consecutivas = {self.max_hate}
► Assertividade = {self.win_hate}
► Saldo = R${self.saldo}
    
    '''))
        return

    def send_sinal(self):
        self.analisar = False
        elem = self.driver.find_element(
            By.XPATH, '/html/body/app-root/app-game/div/div[1]/div[2]/div/div[2]/div[3]/app-bet-controls/div/app-bet-control[1]/div/div[3]/div[2]/div[2]/div/app-spinner/div/div[2]/input')
        elem.click()
        elem.send_keys(Keys.CONTROL + 'a')
        elem.send_keys(str(self.alvo))
        self.driver.find_element(
            By.XPATH, '/html/body/app-root/app-game/div/div[1]/div[2]/div/div[2]/div[3]/app-bet-controls/div/app-bet-control[1]/div/div[1]/div[2]/button').click()

    def gale_1(self):
        self.analisar = False
        self.gale1 = self.valor_banca*2
        elem = self.driver.find_element(
            By.XPATH, '/html/body/app-root/app-game/div/div[1]/div[2]/div/div[2]/div[3]/app-bet-controls/div/app-bet-control[1]/div/div[1]/div[1]/app-spinner/div/div[2]/input')
        elem.click()
        elem.send_keys(Keys.CONTROL + 'a')
        elem.send_keys(str(self.gale1))
        self.driver.find_element(
            By.XPATH, '/html/body/app-root/app-game/div/div[1]/div[2]/div/div[2]/div[3]/app-bet-controls/div/app-bet-control[1]/div/div[1]/div[2]/button').click()

    def gale_2(self):
        self.analisar = False
        self.gale2 = self.gale1*2
        elem = self.driver.find_element(
            By.XPATH, '/html/body/app-root/app-game/div/div[1]/div[2]/div/div[2]/div[3]/app-bet-controls/div/app-bet-control[1]/div/div[1]/div[1]/app-spinner/div/div[2]/input')
        elem.click()
        elem.send_keys(Keys.CONTROL + 'a')
        elem.send_keys(str(self.gale2))
        self.driver.find_element(
            By.XPATH, '/html/body/app-root/app-game/div/div[1]/div[2]/div/div[2]/div[3]/app-bet-controls/div/app-bet-control[1]/div/div[1]/div[2]/button').click()

    def gale_3(self):
        self.gale3 = self.gale2*2
        elem = self.driver.find_element(
            By.XPATH, '/html/body/app-root/app-game/div/div[1]/div[2]/div/div[2]/div[3]/app-bet-controls/div/app-bet-control[1]/div/div[1]/div[1]/app-spinner/div/div[2]/input')
        elem.click()
        elem.send_keys(Keys.CONTROL + 'a')
        elem.send_keys(str(self.gale3))
        self.driver.find_element(
            By.XPATH, '/html/body/app-root/app-game/div/div[1]/div[2]/div/div[2]/div[3]/app-bet-controls/div/app-bet-control[1]/div/div[1]/div[2]/button').click()

    def gale_4(self):
        self.gale4 = self.gale3*2
        elem = self.driver.find_element(
            By.XPATH, '/html/body/app-root/app-game/div/div[1]/div[2]/div/div[2]/div[3]/app-bet-controls/div/app-bet-control[1]/div/div[1]/div[1]/app-spinner/div/div[2]/input')
        elem.click()
        elem.send_keys(Keys.CONTROL + 'a')
        elem.send_keys(str(self.gale4))
        self.driver.find_element(
            By.XPATH, '/html/body/app-root/app-game/div/div[1]/div[2]/div/div[2]/div[3]/app-bet-controls/div/app-bet-control[1]/div/div[1]/div[2]/button').click()

    def gale_5(self):
        self.gale5 = self.gale4*2
        elem = self.driver.find_element(
            By.XPATH, '/html/body/app-root/app-game/div/div[1]/div[2]/div/div[2]/div[3]/app-bet-controls/div/app-bet-control[1]/div/div[1]/div[1]/app-spinner/div/div[2]/input')
        elem.click()
        elem.send_keys(Keys.CONTROL + 'a')
        elem.send_keys(str(self.gale5))
        self.driver.find_element(
            By.XPATH, '/html/body/app-root/app-game/div/div[1]/div[2]/div/div[2]/div[3]/app-bet-controls/div/app-bet-control[1]/div/div[1]/div[2]/button').click()

    def gale_6(self):
        self.gale6 = self.gale5*2
        elem = self.driver.find_element(
            By.XPATH, '/html/body/app-root/app-game/div/div[1]/div[2]/div/div[2]/div[3]/app-bet-controls/div/app-bet-control[1]/div/div[1]/div[1]/app-spinner/div/div[2]/input')
        elem.click()
        elem.send_keys(Keys.CONTROL + 'a')
        elem.send_keys(str(self.gale6))
        self.driver.find_element(
            By.XPATH, '/html/body/app-root/app-game/div/div[1]/div[2]/div/div[2]/div[3]/app-bet-controls/div/app-bet-control[1]/div/div[1]/div[2]/button').click()

    def gale_7(self):
        self.gale7 = self.gale6*2
        elem = self.driver.find_element(
            By.XPATH, '/html/body/app-root/app-game/div/div[1]/div[2]/div/div[2]/div[3]/app-bet-controls/div/app-bet-control[1]/div/div[1]/div[1]/app-spinner/div/div[2]/input')
        elem.click()
        elem.send_keys(Keys.CONTROL + 'a')
        elem.send_keys(str(self.gale7))
        self.driver.find_element(
            By.XPATH, '/html/body/app-root/app-game/div/div[1]/div[2]/div/div[2]/div[3]/app-bet-controls/div/app-bet-control[1]/div/div[1]/div[2]/button').click()

    def gale_8(self):
        self.gale8 = self.gale7*2
        elem = self.driver.find_element(
            By.XPATH, '/html/body/app-root/app-game/div/div[1]/div[2]/div/div[2]/div[3]/app-bet-controls/div/app-bet-control[1]/div/div[1]/div[1]/app-spinner/div/div[2]/input')
        elem.click()
        elem.send_keys(Keys.CONTROL + 'a')
        elem.send_keys(str(self.gale8))
        self.driver.find_element(
            By.XPATH, '/html/body/app-root/app-game/div/div[1]/div[2]/div/div[2]/div[3]/app-bet-controls/div/app-bet-control[1]/div/div[1]/div[2]/button').click()

    def alert_gale(self, cont):
        if cont == 1:
            self.gale_1()
        elif cont == 2:
            self.gale_2()
        elif cont == 3:
            self.gale_3()
        elif cont == 4:
            self.gale_4()
        elif cont == 5:
            self.gale_5()
        elif cont == 6:
            self.gale_6()
        elif cont == 7:
            self.gale_7()
        elif cont == 8:
            self.gale_8()

    def martingale(self, result):

        if result == "WIN":
            print(f"WIN")
            self.saldo = self.pegar_saldo()
            self.win += 1
            self.win_results += 1
            self.max_hate += 1
            # self.bot.send_sticker(self.chat_id, sticker='CAACAgEAAxkBAAEBuhtkFBbPbho5iUL3Cw0Zs2WBNdupaAACQgQAAnQVwEe3Q77HvZ8W3y8E')
            self.bot.send_message(chat_id=self.chat_id,
                                  text=(f'''✅✅✅ WIN ✅✅✅'''))
            self.clicar()
        elif result == "LOSS":

            self.count += 1

            if self.count > self.gales:
                print(f"LOSS")
                self.saldo = self.pegar_saldo()
                self.stop += 1
                self.loss_results += 1
                self.max_hate = 0
                #self.bot.send_sticker(self.chat_id, sticker='CAACAgEAAxkBAAEBuh9kFBbVKxciIe1RKvDQBeDu8WfhFAACXwIAAq-xwEfpc4OHHyAliS8E')
                self.bot.send_message(
                    chat_id=self.chat_id, text=(f'''🚫🚫🚫 LOSS 🚫🚫🚫'''))
                self.clicar()
            else:
                print(f"Vamos para o {self.count}ª Gale 🍀")
                self.alert_gale(self.count)
                return

        self.count = 0
        self.analisar = True
        self.results()
        return

    def clicar(self):
        elem = self.driver.find_element(
            By.XPATH, '/html/body/app-root/app-game/div/div[1]/div[2]/div/div[2]/div[3]/app-bet-controls/div/app-bet-control[1]/div/div[1]/div[1]/app-spinner/div/div[2]/input')
        elem.click()
        elem.send_keys(Keys.CONTROL + 'a')
        elem.send_keys(str(self.valor_banca))

    def check_results(self, results):

        if results >= self.alvo:
            self.martingale('WIN')
            return

        elif results < self.alvo:
            self.martingale('LOSS')
            return

    def start(self):
        check = []
        driver = self.initialize_browser()
        driver.get(
            "https://br.betano.com/casino/live/")
        input("Aperte Enter Apos Fazer Login")
        wait = WebDriverWait(driver, 60)

        frame = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="cronus-iframe-0"]'))
        )
        self.driver.switch_to.frame(frame)

        frame2 = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="game_frame_25_3337_1"]'))
        )
        self.driver.switch_to.frame(frame2)

        """ frame3 = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="game"]'))
        )
        self.driver.switch_to.frame(frame3)

        frame4 = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, '/html/body/app-root/iframe'))
        )
        self.driver.switch_to.frame(frame4) """

        wait.until(
            EC.presence_of_element_located(
                (By.XPATH, '/html/body/app-root/app-game/div/div[1]/div[2]/div/div[2]/div[3]/app-bet-controls/div/app-bet-control[1]/div/app-navigation-switcher/div/button[2]'))
        ).click()

        wait.until(
            EC.presence_of_element_located(
                (By.XPATH, '/html/body/app-root/app-game/div/div[1]/div[2]/div/div[2]/div[3]/app-bet-controls/div/app-bet-control[1]/div/div[3]/div[2]/div[1]/app-ui-switcher'))
        ).click()

        self.clicar()

        time.sleep(2)
        while True:
            if self.win == self.stop_win or self.stop == self.stop_loss:
                if self.win == self.stop_win:
                    print("Atingiu seu Stop Win")
                    break
                elif self.stop == self.stop_loss:
                    print("Atingiu seu Stop Loss")
                    break
            else:
                self.date_now = str(
                    datetime.datetime.now().strftime("%d/%m/%Y"))
                
                results = []
                time.sleep(1)

                results = self.pegar_resultado()

                if check != results:
                    check = results
                    self.estrategy(results)

    def estrategy(self, results):
        print(results)
        if self.analisar == False:
            self.check_results(results[0])
            return

        
        elif self.analisar == True:
            if results[0] > 2 and results[1] > 2:
                print("Sinal ENCONTRADO!")
                self.send_sinal()
                return
            """ with open('estrategy.csv', newline='') as f:
                reader = csv.reader(f)

                ESTRATEGIAS = []

                for row in reader:
                    string = str(row[0])

                    split_saida = string.split('=')
                    split_string = split_saida[0].split('-')

                    listx = []
                    for i in split_string:
                        listx.append(float(i))

                    values = listx
                    values.reverse()
                    dictionary = {'PADRAO': values,
                                  'SAIDA': float(split_saida[1])}
                    ESTRATEGIAS.append(dictionary)

                for i in ESTRATEGIAS:
                    lista = results[0:len(i['PADRAO'])]
                    self.alvo = i['SAIDA']
                    count = 0
                    sinal = False
                    print("Primeiro: " , i)
                    for i in i['PADRAO']:
                        try:
                            print("Segundo: " , i)
                            print("Lista: " , lista[count])
                            if i >= lista[count]:
                                sinal = True
                                count += 1
                            else:
                                sinal = False
                                break
                        except:
                            sinal = False
                            print("Resultados incompletos")
                            break

                    if sinal:
                        print("Sinal ENCONTRADO!")
                        self.send_sinal()
                        return """

    def executar(self):

        self.valor_banca = int(self.combo.get())
        self.stop_win = int(self.combo2.get())
        self.stop_loss = int(self.combo3.get())
        """ self.gale = int(self.combo4.get()) """
        self.start()


scraper = WebScraper()
scraper.start()
