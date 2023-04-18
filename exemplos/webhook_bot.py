from dicgram import Bot


bot = Bot('<TOKEN>',
          webhook_url='https://4e32-187-19-231-202.ngrok-free.app',
          webhook_port=5000)


def mensagens(mim, msg, args):
    print(msg)


bot.privado = {
    '/start': 'Olá, eu sou um bot de teste para o webhook',
    '@mensagem': mensagens
}
