"""
Faz perguntas aos usuários e armazena as respostas
"""

from dicgram import Bot

bot = Bot(token='<TOKEN>', nome='QuestionadorBot')

banco = {}
questionario = {'Qual é o seu nome?': None,
                'Qual é a sua idade?': None,
                'Qual é a sua cor favorita?': None,
                'Qual é a sua comida favorita?': None}


def preencher_perguntas(mim, msg, args):
    nova_pergunta = None
    user_id = msg.chat.id
    texto = msg.text

    if user_id not in banco:
        banco[user_id] = questionario.copy()
    elif banco[user_id] == 'Fim':
        return

    for pergunta, resposta in banco[user_id].items():
        if not resposta:
            nova_pergunta, banco[user_id][pergunta] = pergunta, texto
            break

    if not nova_pergunta:
        banco[user_id] = 'Fim'
        return 'Obrigado por responder o questionário!'
    return nova_pergunta


bot.comandos_privado['@mensagem'] = preencher_perguntas
