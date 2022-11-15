# Author: Marcelo Batista
# GitHub: https://github.com/marcellobatiista
# Sábado, 12 de Novembro de 2022


import requests

from threading import Thread
from dicgram import FRAMEWORK_VERSION, COPYRIGHT
from dicgram.metodos import Metodos
from dicgram.mensagem import Mensagem
from dicgram import check_mensagem
from dicgram import check_funcao_resp


class Bot(Metodos):
    """
    Funções de requisição ao bot API do Telegram
    """

    version = FRAMEWORK_VERSION

    def __init__(self, **kwargs):
        """
        Inicializa o bot

        :param nome: nome do bot
        :param token: token do bot
        :param loop: se o bot deve receber atualizações de novas mensagens: Default é True
        """

        self.__token = kwargs.get('token', None)
        self.__nome = kwargs.get('nome', 'Bot')
        self.__att = kwargs.get('loop', True) is True

        self.__setup(self.__token)
        super().__init__(self.__token)

        self.comandos_privado = {}
        self.comandos_publico = {}

        self.__run() if self.__att else None

    def __status__(self):
        return f'\n{COPYRIGHT}\n{self.__nome} ({self.version}) - Online!\n\n'

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
        print(self.__status__())

    def _get_updates(self, offset=None):
        """
        Pega as novas mensagens

        :param offset: id da última mensagem
        :return: json com as novas mensagens
        """

        url = f'{self.__API_URL}getUpdates?timeout=100'
        if offset:
            url += '&offset={}'.format(offset)
        r = requests.get(url)
        return r.json()

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

        message = msg.get('channel_post', msg.get('message', {}))

        chat_id = message.get('chat', {}).get('id')
        is_privado = message.get('chat', {}).get('type') == 'private'
        texto = message.get('text', '')

        return chat_id, is_privado, texto

    @check_funcao_resp
    def __responder_evento(self, msg):
        """
        Responde a um evento com a chave especial @eventos

        :param msg: mensagem recebida do bot
        :return: None

        Exemplo:

        bot = Bot()

        def ola_evento(mim, msg, args):
            print(msg)

        bot.comandos_publicp = {
            '@mensagem': ola_evento
        }

        """

        chat_id, is_privado, texto = self.__info_msg(msg)

        if '@chat' in self.comandos_privado and texto == '':
            func = self.comandos_privado['@chat']
            func(mim=self, msg=Mensagem(msg), args=None) if is_privado else None
        if '@chat' in self.comandos_publico and texto == '':
            func = self.comandos_publico['@chat']
            func(mim=self, msg=Mensagem(msg), args=None) if not is_privado else None

        if '@mensagem' in self.comandos_privado and texto != '':
            func = self.comandos_privado['@mensagem']
            func(mim=self, msg=Mensagem(msg), args=None) if is_privado else None
        if '@mensagem' in self.comandos_publico and texto != '':
            func = self.comandos_publico['@mensagem']
            func(mim=self, msg=Mensagem(msg), args=None) if not is_privado else None

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
            bot.sendmenssage(chat_id=msg.chat.id, text='Olá mundo 1!')
            mim.sendmenssage(chat_id=msg.chat.id, text='Olá mundo 2!')
            return 'Olá mundo 3!'

        bot.comandos_privado = {
            '/hello': ola_mundo,
            '/world': "Hello World!",
        }

        bot.run()
        """

        cmd = texto.split(' ')[0]

        msg_pv = self.comandos_privado.get(cmd, None)
        msg_pb = self.comandos_publico.get(cmd, None)

        self.__item_de_resposta(msg, msg_pv, msg_pb)

    def __funcao_de_resposta(self, msg, msg_pv, msg_pb):
        """
        Função que será executada quando o bot receber uma mensagem

        :param msg: mensagem recebbida
        :return: False se não for uma função e True se for uma função
        """

        chat_id, is_privado, texto = self.__info_msg(msg)
        args = self.__pegar_argumentos(texto)

        if isinstance(lambda: None, type(msg_pv)) and is_privado:
            resp = msg_pv(mim=self, msg=Mensagem(msg), args=args)
            self.__responder_retorno(chat_id, resp)
        elif isinstance(lambda: None, type(msg_pb)) and not is_privado:
            resp = msg_pb(mim=self, msg=Mensagem(msg), args=args)
            self.__responder_retorno(chat_id, resp)
        else:
            return False

    def __item_de_resposta(self, msg, msg_pv, msg_pb):
        """
        Função que será executada quando o bot receber uma mensagem

        :param msg: mensagem recebbida
        :return: None
        """

        chat_id, is_privado, texto = self.__info_msg(msg)
        func_resp = self.__funcao_de_resposta(msg, msg_pv, msg_pb)

        if func_resp is False:
            if isinstance(msg_pv, str) and is_privado:
                self.sendmessage(chat_id=chat_id, text=msg_pv)
            elif not is_privado and isinstance(msg_pb, str):
                self.sendmessage(chat_id=chat_id, text=msg_pb)
            else:
                self.__responder_evento(msg)

    @staticmethod
    def __pegar_argumentos(texto):
        """
        Pega os argumentos do comando

        :param texto: texto do comando
        :return: lista com os argumentos
        """

        args = texto.split(' ')
        if len(args) > 1:
            args = args[1:]
        else:
            args = None

        return args

    def __responder_retorno(self, chat_id, resp):
        """
        Responde a mensagem com o retorno da função

        :param chat_id: id do chat
        :param resp: retorno da função
        :return: None

        """

        if resp:
            self.sendmessage(chat_id=chat_id, text=resp)
