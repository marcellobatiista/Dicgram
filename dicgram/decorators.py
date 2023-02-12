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

        from fastapi import FastAPI, Request
        from fastapi.responses import JSONResponse

        app = FastAPI()

        @app.post('/' + self._webhook_url.split('/')[-1])
        async def webhook(request: Request):
            """
            Webhook

            :param request: request
            :return: JSONResponse
            """

            data = await request.json()
            func(*args, **kwargs, msg=Mensagem(data))
            return JSONResponse({'status': 'ok'})

        import uvicorn

        uvicorn.run(app, host='0.0.0.0', port=self._webhook_port, log_level='error')

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
