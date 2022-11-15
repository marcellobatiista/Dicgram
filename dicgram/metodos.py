# Author: Marcelo Batista
# GitHub: https://github.com/marcellobatiista
# Sábado, 12 de Novembro de 2022

import requests
from bs4 import BeautifulSoup


class Metodos:
    def __init__(self, token):
        """
        Inicializa a classe
        """

        self.__token = token
        self.__metodos = self.__get_metodos()
        for mtd in self.__metodos:
            self.__criar_metodos(mtd)

    @staticmethod
    def __get_metodos():
        """
        Retorna uma lista com todos os métodos disponíveis na API do Telegram

        :return: lista com todos os métodos disponíveis na API do Telegram
        """

        core = requests.get('https://core.telegram.org/bots/api#available-methods')
        soup = BeautifulSoup(core.content, 'html.parser')
        a = soup.find_all('h4')

        metodos_avaliados = [mtd.find('a').get('href')[1:] for mtd in a]
        metodos_avaliados.remove('formatting-options')
        metodos_avaliados.remove('inline-mode-methods')
        return metodos_avaliados[metodos_avaliados.index('getme'):]

    def __criar_metodos(self, nome):
        """
        Cria um método para cada um dos métodos disponíveis na API do Telegram

        :param nome: nome do método
        :return: None
        """

        def metodo(**kwargs):
            url = f'https://api.telegram.org/bot{self.__token}/{nome}'
            r = requests.get(url,
                             params=kwargs)
            r = r.json().get('result', r.json())
            if r.get('ok', True) is False:
                raise Exception(r.get('description', 'Erro desconhecido'))
            return r

        metodo.__name__ = nome
        setattr(self, nome, metodo)

    def get_metodos(self):
        """
        Retorna uma lista com todos os métodos disponíveis na API do Telegram

        :return: lista com todos os métodos disponíveis na API do Telegram
        """

        return self.__metodos
