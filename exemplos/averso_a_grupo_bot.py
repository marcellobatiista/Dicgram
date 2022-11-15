"""
Robô que não gosta de grupos, então ele sai deles.
"""

from dicgram import Bot

bot = Bot(token='<TOKEN>', nome='SuporteBot')


def sair_do_grupo(mim, msg, args):
    try:
        if msg.message.new_chat_participant.username == 'applicativo_bot':
            mim.sendmessage(chat_id=msg.message.chat.id,
                            text='Não gosto de grupos, então vou sair. Fuiiiz!')
            mim.leavechat(chat_id=msg.message.chat.id)
    except AttributeError:
        pass


bot.comandos_publico['@chat'] = sair_do_grupo
