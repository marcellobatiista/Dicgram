"""
Robô que captura mensagens de texto
por um utilizador e envia para o administrador
"""

from dicgram import Bot

bot = Bot('<TOKEN>')

ID_ADMIN = '<ID do administrador>'


def suporte(mim, msg, args):
    if not args:
        return 'Uso: /suporte <texto>'
    bot.send_message(chat_id=ID_ADMIN,
                     text=f'Usuário {msg.from_user.id} enviou:\n\n{" ".join(args)}')
    return 'Mensagem enviada com sucesso'


bot.privado = {
    '/suporte': suporte,
    '/start': 'Olá, sou um robô de suporte. Envie uma mensagem para o administrador.'
}
