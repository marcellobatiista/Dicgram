import time
from typing import Callable

from dicgram.mensagem import Mensagem


def polling_message(func: Callable) -> Callable:
    """
    Decorator para verificar novas mensagens

    :param func: função a ser decorada
    :return: função decorada
    """

    def wrapper(*args, **kwargs) -> None:
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
            time.sleep(self._polling_rate)

    return wrapper


def webhook_message(func: Callable) -> Callable:
    """
    Decorator para verificar novas mensagens

    :param func: função a ser decorada
    :return: função decorada
    """

    def wrapper(*args, **kwargs) -> None:
        """
        Wrapper da função decorada

        :param args: argumentos da função decorada
        :param kwargs: argumentos nomeados da função decorada
        :return: None
        """

        self = args[0]
        self._set_webhook(self._webhook_url)

        import logging
        from flask import Flask, request, jsonify

        app = Flask(__name__)
        log = logging.getLogger('werkzeug')
        log.setLevel(logging.ERROR)

        @app.route('/' + self._webhook_url.split('/')[-1], methods=['POST'])
        def webhook():
            """
            Webhook

            :return: Json com status
            """

            data = request.get_json()
            func(*args, **kwargs, msg=Mensagem(data))
            return jsonify({'status': 'ok'})

        app.run(host='0.0.0.0', port=self._webhook_port)

    return wrapper


def check_funcao_resp(func: Callable) -> Callable:
    """
    Decorator para verificar se a função de resposta é válida

    :param func: função a ser decorada
    :return: função decorada
    """

    def wrapper(*args, **kwargs) -> None:
        try:
            func(*args, **kwargs)
        except TypeError as e:
            if 'str' in str(e):
                raise Exception('Função de evento não definida')

    return wrapper
