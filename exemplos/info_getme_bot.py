"""
Retorna informações do objeto bot
"""

from dicgram import Bot

bot = Bot(token='<TOKEN>')


def meu_bot(mim, msg, args):
    return mim


bot.comandos_privado['/start'] = meu_bot

# {
#         "id": 5322877719,
#         "is_bot": true,
#         "first_name": "Aplicativo",
#         "username": "applicativo_bot",
#         "can_join_groups": true,
#         "can_read_all_group_messages": false,
#         "supports_inline_queries": false
# }
