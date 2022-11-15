"""
Robô que captura mensagens de texto
por um utilizador e envia para o administrador
"""

from dicgram import Bot

bot = Bot(token='<TOKEN>', nome='SuporteBot')

ID_ADMIN = '<ID do administrador>'


def suporte(mim, msg, args):
    if not args:
        return 'Uso: /suporte <texto>'
    bot.sendmessage(chat_id=ID_ADMIN,
                    text=f'Usuário {msg.message.from_user.id} enviou:\n\n{" ".join(args)}')
    return 'Mensagem enviada com sucesso'


bot.comandos_privado = {
    '/suporte': suporte,
    '/start': 'Olá, sou um robô de suporte. Envie uma mensagem para o administrador.'
}
