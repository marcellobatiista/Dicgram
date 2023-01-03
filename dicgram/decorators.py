import time

from dicgram.mensagem import Mensagem


def check_mensagem(func):
    """
    Decorator para verificar novas mensagens

    :param func: função a ser decorada
    :return: função decorada
    """

    def wrapper(*args, **kwargs):
        """
        Wrapper da função decorada

        :param args: argumentos da função decorada
        :param kwargs: argumentos nomeados da função decorada
        :return: None
        """

        self = args[0]

        last_update_id = None
        while True:
            updates = self._get_updates(last_update_id)
            if not updates:
                pass
            elif 'result' in updates:
                for result in updates['result']:
                    if result['update_id'] != last_update_id:
                        last_update_id = result['update_id']
                        func(*args, **kwargs, msg=Mensagem(result))
            time.sleep(self._atrasar_att)

    return wrapper


def check_funcao_resp(func):
    """
    Decorator para verificar se a função de resposta é válida

    :param func: função a ser decorada
    :return: função decorada
    """

    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except TypeError as e:
            if 'str' in str(e):
                raise Exception('Função de evento não definida')

    return wrapper
