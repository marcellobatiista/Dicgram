# Author: Marcelo Batista
# GitHub: https://github.com/marcellobatiista
# Sábado, 12 de Novembro de 2022

import requests
from bs4 import BeautifulSoup
from dicgram.mensagem import Mensagem


class Metodos:
    def __init__(self, token):
        """
        Inicializa a classe
        """

        self.__token = token
        self.__metodos = self.__get_metodos()
        for mtd in self.__metodos:
            self.__criar_metodo(mtd)

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

    def __criar_metodo(self, nome):
        """
        Cria um método disponível na API do Telegram

        :param nome: nome do método
        :return: None
        """

        def metodo(*args, **kwargs):
            mtsp = self.sem_parametros()
            if (not kwargs or args) and nome not in mtsp:
                raise ValueError('Você deve passar os parâmetros como argumentos nomeados')

            url = f'https://api.telegram.org/bot{self.__token}/{nome}'
            r = requests.get(url,
                             params=kwargs)
            r = r.json().get('result', r.json())

            if r.get('ok') or (isinstance(r, bool) and r):  # Msg Usuário
                return r
            elif not r.get('description'):  # Msg Bot
                return Mensagem(r)
            else:
                raise Exception(r.get('description', r))

        metodo.__name__ = nome
        setattr(self, nome, metodo)

    @staticmethod
    def sem_parametros():
        """
        Retorna uma lista com todos os
        métodos disponíveis na API do Telegram
        que não possuem parâmetros
        """

        return ['getme', 'close', 'getforumtopiciconstickers',
                'getupdates', 'getwebhookinfo', 'logOut']

    def get_metodos(self):
        """
        Retorna uma lista com todos os métodos disponíveis
        na API do Telegram
        """

        return self.__metodos
