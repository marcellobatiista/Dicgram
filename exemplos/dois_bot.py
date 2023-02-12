"""
Conversa entre dois bots
O bot 1 envia uma mensagem para o bot 2
O bot 2 responde a mensagem do bot 1
O bot 1 responde a mensagem do bot 2
O bot 2 responde a mensagem do bot 1
E assim por diante
"""

from dicgram import Bot

bot1 = Bot('<TOKEN1>')
bot2 = Bot('<TOKEN2>')


def bot1_responder(mim, msg, args):
    bot2.send_message(chat_id=msg.chat.id,
                      text=f'Bot1 disse: {msg.text}')


def bot2_responder(mim, msg, args):
    bot1.send_message(chat_id=msg.chat.id,
                      text=f'Bot2 disse: {msg.text}')


bot1.privado['@mensagem'] = bot1_responder
bot2.privado['@mensagem'] = bot2_responder
