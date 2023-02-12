"""
Robô que não gosta de grupos, então ele sai deles.
"""

from dicgram import Bot

bot = Bot('<TOKEN>')


def sair_do_grupo(mim, msg, args):
    try:
        if msg.new_chat_participant.username == mim.username:
            mim.send_message(chat_id=msg.chat.id,
                             text='Não gosto de grupos, então vou sair. Fuiiiz!')
            mim.leave_chat(chat_id=msg.chat.id)
    except AttributeError:
        pass


bot.publico['@chat'] = sair_do_grupo
