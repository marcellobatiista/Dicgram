# Author: Marcelo Batista
# GitHub: https://github.com/marcellobatiista
# Sábado, 12 de Novembro de 2022


import json


class Campos:
    campos = ['message',
              'edited_message', 'channel_post',
              'edited_channel_post', 'inline_query',
              'chosen_inline_result', 'callback_query',
              'shipping_query', 'pre_checkout_query',
              'poll', 'poll_answer',
              'my_chat_member', 'chat_member',
              'chat_join_request']

    def __init__(self, message: dict):
        self.message = message

    def update(self) -> int:
        """
        Retorna o campo da mensagem

        :return: str
        """

        return list(self.message.keys())[1]


class Mensagem:
    """
    Classe que transforma um dicionário em um objeto,
    """

    def __init__(self, dicionario: dict):
        """
        :param dicionario: dicionário a ser transformado em objeto
        """

        self.update = None

        for k, v in dicionario.items():
            if isinstance(v, dict):
                setattr(self, k.replace('from', 'from_user'), Mensagem(v))
            else:
                if k == 'update_id':
                    setattr(self, k.replace('update_id', 'update'), Campos(dicionario).update())
                else:
                    setattr(self, k.replace('from', 'from_user'), v)

    def __str__(self):
        """
        Existem casos em que o valor do atributo é um objeto,
        então é necessário transformar o objeto em um dicionário
        para que possa ser transformado em uma string
        """

        return json.dumps(self.__dict__, default=lambda o: o.__dict__, indent=4)
