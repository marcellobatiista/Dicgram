"""
Retorna informações do objeto msg
"""

from dicgram import Bot

bot = Bot(token='<TOKEN>')


def minha_msg(mim, msg, args):
    return msg


bot.comandos_privado['/start'] = minha_msg

# {
#     "message_id": 2657,
#     "from_user": {
#         "id": 665448517,
#         "is_bot": false,
#         "first_name": "Dev",
#         "last_name": "Wulf",
#         "username": "SP4CNE",
#         "language_code": "pt-br"
#     },
#     "chat": {
#         "id": 665448517,
#         "first_name": "Dev",
#         "last_name": "Wulf",
#         "username": "SP4CNE",
#         "type": "private"
#     },
#     "date": 1668799915,
#     "text": "/start",
#     "entities": [
#         {
#             "offset": 0,
#             "length": 6,
#             "type": "bot_command"
#         }
#     ]
# }
