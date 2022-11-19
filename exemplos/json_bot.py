"""
Retorna informações do objeto mim e msg
"""

from dicgram import Bot

bot = Bot(token='<TOKEN>')


def info_msg(mim, msg, args):
    mim.send_message(chat_id=msg.chat.id, text=f'<code>{msg}</code>', parse_mode='HTML')
    info_mim(mim, msg, args)


def info_mim(mim, msg, args):
    mim.send_message(chat_id=msg.chat.id, text=f'<code>{mim}</code>', parse_mode='HTML')


bot.comandos_privado['@mensagem'] = info_msg
