from dotenv import load_dotenv
import os
import requests
import json
from src.data.driveBot import driveBot
from src.data.transform_dataframe import transform_data
from src.visualization.visualize import barv_npsmean_by, hist_nps
from PIL import Image


load_dotenv()

class TelegramBot():
    def __init__(self):
        TOKEN = os.getenv("API_KEY")
        self.url = f"https://api.telegram.org/bot{TOKEN}/"
        self.driveBot = driveBot()
    def start(self):
        print("Inicializando bot...")
        update_id = None
        while True:
            update = self.get_message(update_id)
            # print("Update recebido:", update)  # <<< imprima o JSON inteiro

            messages = update.get('result', [])
            if messages:
                for message in messages:
                    try:
                        update_id = message['update_id']
                        chat_id = message['message']['from']['id']
                        message_text = message['message']['text']
                        answer_bot, figure_boolean = self.create_answer(message_text)
                        self.send_answer(chat_id, answer_bot, figure_boolean)
                    except Exception as e:
                        print("Erro ao processar mensagem:", e)
                        pass

    def get_message(self, update_id):
        link_request = f"{self.url}getUpdates?timeout=1000"
        if update_id:
            link_request = f"{self.url}getUpdates?timeout=1000&offset={update_id + 1}"
        result = requests.get(link_request)
        return json.loads(result.content)
    
    def create_answer(self, message_text):
        dataframe = transform_data(self.driveBot.get_data())
        message_text = message_text.lower()
        if message_text in ["/start", "ola", "eae", "menu", "oi", "oie"]:
            return "Ola, tudo bem? Seja bem vindo ao Bot do RH da Empresa RDS. Selecione o que deseja:" + "\n" + "1 - NPS interno mensal médio por setor" + "\n" + "2 - NPS interno mensal médio por contratação" + "\n" + "3 - Distribuição do NPS interno" + "\n", 0
        elif message_text == '1':
            return barv_npsmean_by(dataframe, "Setor"), 1
        elif message_text == '2':
            return barv_npsmean_by(dataframe, "Tipo de Contratação"), 1
        elif message_text == '3':
            return hist_nps(dataframe), 1
        else:
            return "Comando não encontrado, tente novamente. Selecione o que deseja:" + "\n" + "1 - NPS interno mensal médio por setor" + "\n" + "2 - NPS interno mensal médio por contratação" + "\n" + "3- Distribuição do NPS interno" + "\n", 0
    
    def send_answer(self, chat_id, answer, figure_boolean):
        if figure_boolean == 0:
            link_to_send = f"{self.url}sendMessage?chat_id={chat_id}&text={answer}"
            requests.get(link_to_send)
            return
        else:
            answer.seek(0)
            requests.post(f"{self.url}sendPhoto?chat_id={chat_id}", files = dict(photo=answer))
            answer.close()
            return