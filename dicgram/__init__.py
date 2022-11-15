import time

FRAMEWORK_VERSION = '0.1.0'
COPYRIGHT = 'Copyright (c) 2022 Marcelo <https://github.com/marcellobatiista>'

# =================================================================
AUTHOR = 'Marcelo Batista'
AUTHOR_EMAIL = 'batista.marcelo34@gmail.com'
AUTHOR_GITHUB = 'https://github.com/marcellobatiista'
AUTHOR_TWITTER = 'https://twitter.com/marcellobatiist'
AUTHOR_LINKEDIN = 'https://www.linkedin.com/in/marcellobatiista/'
AUTHOR_INSTAGRAM = 'https://www.instagram.com/marcellobatiista/'


# ==================================================================


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
            if 'result' in updates:
                for result in updates['result']:
                    if result['update_id'] != last_update_id:
                        last_update_id = result['update_id']
                        func(*args, **kwargs, msg=result)
            time.sleep(0.2)

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
