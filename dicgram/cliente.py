# Author: Marcelo Batista
# GitHub: https://github.com/marcellobatiista
# Sábado, 12 de Novembro de 2022

import time
from threading import Thread
from typing import Union, Callable

import requests

from dicgram.decorators import check_funcao_resp
from dicgram.decorators import polling_message
from dicgram.decorators import webhook_message
from dicgram.mensagem import Mensagem
from dicgram.metodos import Metodos


class Bot(Metodos):
    """
    Funções de requisição ao bot API do Telegram
    """

    version = None
    copyright = None

    privado = {}
    publico = {}

    def __init__(
            self,
            token,
            polling=True,
            polling_rate=0.5,
            webhook_url=None,
            webhook_port=8000
    ):

        """
        Inicializa o bot

        :param token: token do bot
        :param polling: se o bot deve receber atualizações de novas mensagens: Default é True
        :param polling_rate: atraso entre as atualizações de novas mensagens: Default é 0.5
        :param webhook_url: url do webhook: Default é None
        :param webhook_port: porta do seu server para o webhook: Default é None
        """

        self.__token = token
        self.__att = polling is True

        self._polling_rate = polling_rate
        self._polling_rate = self._polling_rate if self._polling_rate > 0 else 0.5

        self._webhook_url = webhook_url
        self._webhook_port = webhook_port

        if self._webhook_url and self._webhook_url.find('https://') == -1:
            raise Exception('URL do webhook deve ser HTTPS')

        self.__setup(self.__token)
        super().__init__(self.__token)
        self.__set_mim()
        self.__webhook_info = self._info_webhook()

        if self._webhook_url:
            self.__run_webhook()
        elif self.__att:
            self.__run_polling()

    def __str__(self):
        """
        Retorna as informações do bot

        :return: informações do bot
        """

        return self.get_me().__str__()

    def __status(self) -> str:
        if self._webhook_url:
            status = f'\n{self.copyright}\n@{self.username} ({self.version}) - Webhook ativo!\n'
            status += f'URL: {self._webhook_url}\n'
            status += f'Porta: {self._webhook_port}\n'
        else:
            status = f'\n{self.copyright}\n@{self.username} ({self.version}) - Polling ativo!\n'
            status += f'Polling rate: {self._polling_rate}s\n'
        return status

    def __setup(self, token) -> None:
        """
        Configura o bot

        :param token: token do bot
        :return: None
        """

        if ':' not in token:
            raise Exception('Token não informado')
        self.__API_URL = f'https://api.telegram.org/bot{token}/'

    def __run_polling(self) -> None:
        """
        Inicia o loop do bot para capturar novas mensagens
        """

        Thread(target=self.__receber_mensagem).start()
        print(self.__status())

    def __run_webhook(self) -> None:
        """
        Inicia o server do bot para receber novas mensagens
        """

        Thread(target=self.__receber_mensagem_webhook).start()
        print(self.__status())

    def __set_mim(self) -> None:
        """
        Adiciona informações do bot ao objeto
        :return: None
        """

        gm = self.get_me()
        atributos = dir(gm)
        for atributo in atributos:
            if atributo[0] != '_':
                setattr(self, atributo, getattr(gm, atributo))

    def _get_updates(self, offset: int = None) -> dict:
        """
        Pega as novas mensagens

        :param offset: id da última mensagem
        :return: json com as novas mensagens
        """

        # deleta webhook antes
        if self.__webhook_info['result']['url']:
            self._set_webhook('')
            self.__webhook_info = self._info_webhook()

        url = f'{self.__API_URL}getUpdates?timeout=100'
        if offset:
            url += '&offset={}'.format(offset)
        try:
            r = requests.get(url)
            return r.json()
        except requests.exceptions.ConnectionError:
            print('Debug: Erro de conexão')
            time.sleep(5)

    def _info_webhook(self) -> dict:
        """
        Pega as informações do webhook

        :return: json com as informações do webhook
        """

        url = f'{self.__API_URL}getWebhookInfo'
        return requests.get(url).json()

    def _set_webhook(self, url: str, cert: str = None) -> None:
        """
        Configura o webhook do bot

        :param url: url do webhook
        :param cert: certificado do webhook
        :return: None
        """

        url = f'{self.__API_URL}setWebhook?url={url}'
        if cert:
            url += f'&certificate={cert}'
        requests.get(url)

    @polling_message
    def __receber_mensagem(self, msg: Mensagem) -> None:
        """
        Recebe a mensagem e a processa

        :param msg: mensagem recebida do bot através do decorador
        """

        chat_id, is_privado, texto = self.__info_msg(msg)
        self.__responder_comando(texto, msg)

    @webhook_message
    def __receber_mensagem_webhook(self, msg: Mensagem) -> None:
        """
        Recebe a mensagem e a processa

        :param msg: mensagem recebida do bot através do decorador
        """

        chat_id, is_privado, texto = self.__info_msg(msg)
        self.__responder_comando(texto, msg)

    @staticmethod
    def __info_msg(msg: Mensagem) -> tuple:
        """
        Retorna 3 informações importantes da mensagem

        :param msg: mensagem recebida do bot
        :return: informações da mensagem
        """

        conteudo = getattr(msg, msg.update)

        chat = getattr(conteudo, 'chat', None)
        chat_id = getattr(chat, 'id', None)
        is_privado = getattr(chat, 'type', None) == 'private'
        texto = getattr(conteudo, 'text', None)

        return chat_id, is_privado, texto

    def __responder_comando(self, texto: str, msg: Mensagem) -> None:
        """
        Mensagem a ser enviada quando o usuário digitar o cmd

        :param texto: comando digitado pelo usuário
        :param msg: mensagem recebida

        Se o chat for privado, o comando será procurado na lista de comandos
        privados, caso contrário, será procurado na lista de comandos de chat
        A função que será executada será a que estiver associada ao comando
        digitado pelo usuário na lista de comandos do chat qualquer ou privado.
        Se não houver uma função associada ao comando, será enviada uma mensagem
        padrão como resposta.

        Exemplo:

        bot = Bot()

        def ola_mundo(mim, msg, args):
            bot.send_menssage(chat_id=msg.chat.id, text='Olá mundo 1!')
            mim.send_menssage(chat_id=msg.chat.id, text='Olá mundo 2!')
            return 'Olá mundo 3!'

        bot.privado = {
            '/hello': ola_mundo,
            '/world': "Hello World!",
        }

        bot.run()
        """

        cmd = texto.split(' ')[0] if texto else None
        msg_pv = self.privado.get(cmd, None)
        msg_pb = self.publico.get(cmd, None)

        self.__item_de_resposta(msg, msg_pv, msg_pb)

    def __item_de_resposta(self, msg: Mensagem,
                           msg_pv: Union[str, None, Callable],
                           msg_pb: Union[str, None, Callable]) -> None:
        """
        Envia a mensagem de resposta

        :param msg: mensagem recebida
        :return: None
        """

        chat_id, is_privado, texto = self.__info_msg(msg)
        func_resp = self.__funcao_manipuladora(msg, msg_pv, msg_pb)

        if func_resp is False:
            if isinstance(msg_pv, str) and is_privado:
                self.send_message(chat_id=chat_id, text=msg_pv)
            elif not is_privado and isinstance(msg_pb, str):
                self.send_message(chat_id=chat_id, text=msg_pb)
            else:
                self.__responder_evento(msg)

    def __funcao_manipuladora(self, msg: Mensagem,
                              msg_pv: Union[str, None, Callable],
                              msg_pb: Union[str, None, Callable]) -> Union[
        bool, None]:
        """
        Função que será executada quando o bot receber uma mensagem

        :param msg: mensagem recebbida
        :return: False se não for uma função
        """

        chat_id, is_privado, texto = self.__info_msg(msg)
        args = self.__pegar_argumentos(texto)

        msg = getattr(msg, msg.update)
        if isinstance(lambda: None, type(msg_pv)) and is_privado:
            resp = msg_pv(mim=self, msg=msg, args=args)
            self.__responder_retorno(chat_id, resp)
        elif isinstance(lambda: None, type(msg_pb)) and not is_privado:
            resp = msg_pb(mim=self, msg=msg, args=args)
            self.__responder_retorno(chat_id, resp)
        else:
            return False

    @check_funcao_resp
    def __responder_evento(self, msg: Mensagem) -> None:
        """
        Responde a um evento com a chave especial @

        :param msg: mensagem recebida do bot
        :return: None

        Exemplo:

        bot = Bot()

        def ola_evento(mim, msg, args):
            print(msg)

        bot.comandos_publicp = {
            '@mensagem': ola_evento,
            '@chat': ola_evento
        }

        """

        self.__evento_chat(msg)
        self.__evento_mensagem(msg)
        self.__evento_edit_mensagem(msg)

    def __executar_funcao(self,
                          func: Callable,
                          msg: Mensagem,
                          is_privado: bool) -> any:
        """
        :param func: função a ser executada
        :param msg: mensagem recebida do bot
        :param is_privado: se a mensagem é privada
        """

        try:
            resp = func(mim=self, msg=msg, args=None) if is_privado else None
        except AttributeError as e:
            atributo = str(e).split()[-1].strip("'")
            setattr(Mensagem, atributo, None)
            return self.__executar_funcao(func, msg, is_privado)
        return resp

    def __evento_chat(self, msg: Mensagem) -> None:
        """
        Responde a um evento de chat

        :param msg: mensagem recebida do bot
        :return: None
        """

        chat_id, is_privado, texto = self.__info_msg(msg)

        msg = getattr(msg, msg.update)
        if '@chat' in self.privado and not texto:
            func = self.privado['@chat']
            resp = self.__executar_funcao(func, msg, is_privado)
            self.__responder_retorno(chat_id, resp)
        if '@chat' in self.publico and not texto:
            func = self.publico['@chat']
            resp = self.__executar_funcao(func, msg, not is_privado)
            self.__responder_retorno(chat_id, resp)

    def __evento_mensagem(self, msg: Mensagem) -> None:
        """
        Responde a um evento de mensagem

        :param msg: mensagem recebida do bot
        :return: None
        """

        post = msg.update == 'message' or msg.update == 'channel_post'
        chat_id, is_privado, texto = self.__info_msg(msg)

        msg = getattr(msg, msg.update)
        if '@mensagem' in self.privado and post:
            func = self.privado['@mensagem']
            resp = self.__executar_funcao(func, msg, is_privado)
            self.__responder_retorno(chat_id, resp)
        if '@mensagem' in self.publico and post:
            func = self.publico['@mensagem']
            resp = self.__executar_funcao(func, msg, not is_privado)
            self.__responder_retorno(chat_id, resp)

    def __evento_edit_mensagem(self, msg: Mensagem) -> None:
        """
        Responde a um evento de edição de mensagem

        :param msg: mensagem recebida do bot
        :return: None
        """

        edit_post = msg.update == 'edited_message' or msg.update == 'edited_channel_post'
        chat_id, is_privado, texto = self.__info_msg(msg)

        msg = getattr(msg, msg.update)
        if '@edit' in self.privado and edit_post:
            func = self.privado['@edit']
            resp = self.__executar_funcao(func, msg, is_privado)
            self.__responder_retorno(chat_id, resp)
        if '@edit' in self.publico and edit_post:
            func = self.publico['@edit']
            resp = self.__executar_funcao(func, msg, not is_privado)
            self.__responder_retorno(chat_id, resp)

    @staticmethod
    def __pegar_argumentos(texto: str) -> Union[list, None]:
        """
        Pega os argumentos do comando

        :param texto: texto do comando
        :return: lista com os argumentos
        """

        if texto:
            args = texto.split(' ')
            if len(args) > 1:
                args = args[1:]
            else:
                args = None
            return args
        return None

    def __responder_retorno(self, chat_id: Union[int, str], resp: str) -> None:
        """
        Responde a mensagem com o retorno da função

        :param chat_id: id do chat
        :param resp: retorno da função
        :return: None

        """

        if resp:
            self.send_message(chat_id=chat_id, text=resp)
