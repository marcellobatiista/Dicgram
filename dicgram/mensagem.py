# Author: Marcelo Batista
# GitHub: https://github.com/marcellobatiista
# Sábado, 12 de Novembro de 2022


import json


class Mensagem:
    """
    Classe que transforma um dicionário em um objeto,
    """

    def __init__(self, dicionario):
        """
        :param dicionario: dicionário a ser transformado em objeto
        """

        dicionario = dicionario.get('channel_post', dicionario)
        dicionario = dicionario.get('edited_channel_post', dicionario)
        dicionario = dicionario.get('my_chat_member', dicionario)
        dicionario = dicionario.get('chat_member', dicionario)
        dicionario = dicionario.get('chat_join_request', dicionario)
        dicionario = dicionario.get('callback_query', dicionario)
        dicionario = dicionario.get('inline_query', dicionario)
        dicionario = dicionario.get('chosen_inline_result', dicionario)
        dicionario = dicionario.get('message', dicionario)  #

        for k, v in dicionario.items():
            if isinstance(v, dict):
                setattr(self, k.replace('from', 'from_user'), Mensagem(v))
            else:
                setattr(self, k.replace('from', 'from_user'), v)

    def __str__(self):
        """
        Existem casos em que o valor do atributo é um objeto,
        então é necessário transformar o objeto em um dicionário
        para que possa ser transformado em uma string
        """

        return json.dumps(self.__dict__, default=lambda o: o.__dict__, indent=4)
