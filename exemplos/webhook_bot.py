from dicgram import Bot

bot = Bot('<TOKEN>',
          webhook_url='https://f7da-2804-29b8.ngrok.io/webhook')




bot.privado = {
    '/start': 'Olá, eu sou um bot de teste para o webhook'
}
