# Author: Marcelo Batista
# GitHub: https://github.com/marcellobatiista
# Sábado, 12 de Novembro de 2022
import time
from threading import Thread

import requests

from dicgram.decorators import check_funcao_resp
from dicgram.decorators import check_mensagem
from dicgram.metodos import Metodos


class Bot(Metodos):
    """
    Funções de requisição ao bot API do Telegram
    """

    version = None
    copyright = None

    comandos_privado = {}
    comandos_publico = {}

    def __init__(self, **kwargs):
        """
        Inicializa o bot

        :param nome: nome do bot
        :param token: token do bot
        :param update: se o bot deve receber atualizações de novas mensagens: Default é True
        :param atrasar_update: atraso entre as atualizações de novas mensagens: Default é 0.5
        """

        self.__token = kwargs.get('token', None)
        self.__att = kwargs.get('update', True) is True

        self._atrasar_att = kwargs.get('atrasar_update', 0.5)
        self._atrasar_update = self._atrasar_att if self._atrasar_att > 0 else 0.5

        self.__setup(self.__token)
        super().__init__(self.__token)
        self.__set_mim()
        self.__run() if self.__att else None

    def __str__(self):
        """
        Retorna as informações do bot

        :return: informações do bot
        """

        return self.get_me().__str__()

    def __status(self):
        return f'\n{self.copyright}\n@{self.username} ({self.version}) - Online!\n\n'

    def __setup(self, token):
        """
        Configura o bot

        :param token: token do bot
        :return: None
        """

        if not token:
            raise Exception('Token não informado')
        self.__API_URL = f'https://api.telegram.org/bot{token}/'

    def __run(self):
        """
        Inicia o loop do bot para capturar novas mensagens
        """

        Thread(target=self.__receber_mensagem).start()
        print(self.__status())

    def __set_mim(self):
        """
        Adiciona informações do bot ao objeto
        :return: None
        """
        
        gm = self.get_me()
        atributos = dir(gm)
        for atributo in atributos:
            if atributo[0] != '_':
                setattr(self, atributo, getattr(gm, atributo))

    def _get_updates(self, offset=None):
        """
        Pega as novas mensagens

        :param offset: id da última mensagem
        :return: json com as novas mensagens
        """

        url = f'{self.__API_URL}getUpdates?timeout=100'
        if offset:
            url += '&offset={}'.format(offset)
        try:
            r = requests.get(url)
            return r.json()
        except requests.exceptions.ConnectionError:
            print('Debug: Erro de conexão')
            time.sleep(5)

    @check_mensagem
    def __receber_mensagem(self, msg):
        """
        Recebe a mensagem e a processa

        :param msg: mensagem recebida do bot através do decorador
        """

        chat_id, is_privado, texto = self.__info_msg(msg)
        self.__responder_comando(texto, msg)

    @staticmethod
    def __info_msg(msg):
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

    def __responder_comando(self, texto, msg):
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

        bot.comandos_privado = {
            '/hello': ola_mundo,
            '/world': "Hello World!",
        }

        bot.run()
        """

        cmd = texto.split(' ')[0] if texto else None
        msg_pv = self.comandos_privado.get(cmd, None)
        msg_pb = self.comandos_publico.get(cmd, None)

        self.__item_de_resposta(msg, msg_pv, msg_pb)

    def __item_de_resposta(self, msg, msg_pv, msg_pb):
        """
        Envia a mensagem de resposta

        :param msg: mensagem recebida
        :return: None
        """

        chat_id, is_privado, texto = self.__info_msg(msg)
        func_resp = self.__funcao_de_resposta(msg, msg_pv, msg_pb)

        if func_resp is False:
            if isinstance(msg_pv, str) and is_privado:
                self.send_message(chat_id=chat_id, text=msg_pv)
            elif not is_privado and isinstance(msg_pb, str):
                self.send_message(chat_id=chat_id, text=msg_pb)
            else:
                self.__responder_evento(msg)

    def __funcao_de_resposta(self, msg, msg_pv, msg_pb):
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
    def __responder_evento(self, msg):
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

    def __evento_chat(self, msg):
        """
        Responde a um evento de chat

        :param msg: mensagem recebida do bot
        :return: None
        """

        chat_id, is_privado, texto = self.__info_msg(msg)

        msg = getattr(msg, msg.update)
        if '@chat' in self.comandos_privado and not texto:
            func = self.comandos_privado['@chat']
            resp = func(mim=self, msg=msg, args=None) if is_privado else None
            self.__responder_retorno(chat_id, resp)
        if '@chat' in self.comandos_publico and not texto:
            func = self.comandos_publico['@chat']
            resp = func(mim=self, msg=msg, args=None) if not is_privado else None
            self.__responder_retorno(chat_id, resp)

    def __evento_mensagem(self, msg):
        """
        Responde a um evento de mensagem

        :param msg: mensagem recebida do bot
        :return: None
        """

        post = msg.update == 'message' or msg.update == 'channel_post'
        chat_id, is_privado, texto = self.__info_msg(msg)

        msg = getattr(msg, msg.update)
        if '@mensagem' in self.comandos_privado and post:
            func = self.comandos_privado['@mensagem']
            resp = func(mim=self, msg=msg, args=None) if is_privado else None
            self.__responder_retorno(chat_id, resp)
        if '@mensagem' in self.comandos_publico and post:
            func = self.comandos_publico['@mensagem']
            resp = func(mim=self, msg=msg, args=None) if not is_privado else None
            self.__responder_retorno(chat_id, resp)

    def __evento_edit_mensagem(self, msg):
        """
        Responde a um evento de edição de mensagem

        :param msg: mensagem recebida do bot
        :return: None
        """

        edit_post = msg.update == 'edited_message' or msg.update == 'edited_channel_post'
        chat_id, is_privado, texto = self.__info_msg(msg)

        msg = getattr(msg, msg.update)
        if '@edit' in self.comandos_privado and edit_post:
            func = self.comandos_privado['@edit']
            resp = func(mim=self, msg=msg, args=None) if is_privado else None
            self.__responder_retorno(chat_id, resp)
        if '@edit' in self.comandos_publico and edit_post:
            func = self.comandos_publico['@edit']
            resp = func(mim=self, msg=msg, args=None) if not is_privado else None
            self.__responder_retorno(chat_id, resp)

    @staticmethod
    def __pegar_argumentos(texto):
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

    def __responder_retorno(self, chat_id, resp):
        """
        Responde a mensagem com o retorno da função

        :param chat_id: id do chat
        :param resp: retorno da função
        :return: None

        """

        if resp:
            self.send_message(chat_id=chat_id, text=resp)
