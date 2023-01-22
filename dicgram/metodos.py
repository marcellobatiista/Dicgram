# Author: Marcelo Batista
# GitHub: https://github.com/marcellobatiista
# Sábado, 12 de Novembro de 2022

import requests
from bs4 import BeautifulSoup

from dicgram.mensagem import Mensagem


class Metodos:
    def __init__(self, token: str):
        """
        Inicializa a classe
        """

        self.__token = token
        self.__metodos = self._get_metodos()
        for mtd in self.__metodos:
            self.__criar_metodo(mtd)

    @staticmethod
    def _get_metodos() -> list:
        """
        Retorna uma lista com todos os métodos disponíveis na API do Telegram

        :return: lista com todos os métodos disponíveis na API do Telegram
        """

        core = requests.get('https://core.telegram.org/bots/api#available-methods')
        soup = BeautifulSoup(core.content, 'html.parser')
        a = soup.find_all('h4')

        metodos = [mtd.text for mtd in a if ' ' not in mtd.text]
        metodos_avaliados = metodos[metodos.index('getMe'):]

        return Metodos.snake_case(metodos_avaliados)

    def __criar_metodo(self, nome: str) -> None:
        """
        Cria um método disponível na API do Telegram

        :param nome: nome do método
        :return: None
        """

        def metodo(*args, **kwargs):
            mtsp = self.sem_parametros()
            if (not kwargs or args) and nome not in mtsp:
                raise ValueError('Você deve passar os parâmetros como argumentos nomeados')

            url = f'https://api.telegram.org/bot{self.__token}/{nome.replace("_", "")}'
            r = requests.get(url,
                             params=kwargs)
            r = r.json().get('result', r.json())

            if isinstance(r, bool):
                pass
            elif r.get('ok'):  # Msg Usuário
                return Mensagem(r)
            elif not r.get('description'):  # Msg Bot
                return Mensagem(r)
            else:
                raise Exception(r.get('description', r))

        metodo.__name__ = nome
        setattr(self, nome, metodo)

    @staticmethod
    def snake_case(lista: list) -> list:
        """
        Retorna uma lista com todos os métodos
        disponíveis na API do Telegram em snake_case

        :param lista: lista com os métodos
        :return: lista com os métodos em snake_case
        """

        lista_formatada = []
        for nome in lista:
            nome_formatado = ''
            for letra in nome:
                if len(nome_formatado) > 0 and letra.isupper() and nome_formatado[-1].islower():
                    nome_formatado += '_'
                nome_formatado += letra
            lista_formatada.append(nome_formatado.lower())
        return lista_formatada

    def sem_parametros(self) -> list:
        """
        Retorna uma lista com todos os
        métodos disponíveis na API do Telegram
        que não possuem parâmetros
        """

        return self.snake_case(['getMe', 'close', 'getForumTopicIconStickers',
                                'getUpdates', 'getWebhookInfo', 'logOut'])

    def get_metodos(self) -> list:
        """
        Retorna uma lista com todos os métodos disponíveis
        na API do Telegram
        """

        return self.__metodos
