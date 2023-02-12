"""
Robô que calcula operações matemáticas
"""


import math

from dicgram import Bot

bot = Bot('<TOKEN>')


def somar(mim, msg, args):
    if not args:
        return 'Uso: /somar <números>'
    for i in args:
        if not i.isdigit() and '-' not in i:
            return f'"{i}" não é um número'
    return sum(map(int, args))


def subtrair(mim, msg, args):
    if not args:
        return 'Uso: /subtrair <números>'
    for i in args:
        if not i.isdigit() and '-' not in i:
            return f'"{i}" não é um número'
    return float(args[0]) - float(args[1])


def multiplicar(mim, msg, args):
    if not args:
        return 'Uso: /multiplicar <números>'
    for i in args:
        if not i.isdigit() and '-' not in i:
            return f'"{i}" não é um número'
    return float(args[0]) * float(args[1])


def dividir(mim, msg, args):
    if not args:
        return 'Uso: /dividir <números>'
    for i in args:
        if not i.isdigit() and '-' not in i:
            return f'"{i}" não é um número'
    if float(args[1]) == 0:
        return 'Não é possível dividir por zero'
    return float(args[0]) / float(args[1])


def potencia(mim, msg, args):
    if not args:
        return 'Uso: /potencia <números>'
    for i in args:
        if not i.isdigit() and '-' not in i:
            return f'"{i}" não é um número'
    return float(args[0]) ** float(args[1])


def raiz(mim, msg, args):
    if not args:
        return 'Uso: /raiz <números>'
    for i in args:
        if not i.isdigit() and '-' not in i:
            return f'"{i}" não é um número'
    return float(args[0]) ** (1 / float(args[1]))


def fatorial(mim, msg, args):
    if not args:
        return 'Uso: /fatorial <números>'
    for i in args:
        if not i.isdigit() and '-' not in i:
            return f'"{i}" não é um número'
    return math.factorial(int(args[0]))


def log(mim, msg, args):
    if not args:
        return 'Uso: /log <números>'
    for i in args:
        if not i.isdigit() and '-' not in i:
            return f'"{i}" não é um número'
    return math.log(int(args[0]))


def log10(mim, msg, args):
    if not args:
        return 'Uso: /log10 <números>'
    for i in args:
        if not i.isdigit() and '-' not in i:
            return f'"{i}" não é um número'
    return math.log10(int(args[0]))


def delta(mim, msg, args):
    if not args:
        return 'Uso: /delta <números>'
    for i in args:
        if not i.isdigit() and '-' not in i:
            return f'"{i}" não é um número'
    return float(args[1]) ** 2 - 4 * float(args[0]) * float(args[2])


def raizes(mim, msg, args):
    if not args:
        return 'Uso: /raizes <números>'
    for i in args:
        if not i.isdigit() and '-' not in i:
            return f'"{i}" não é um número'
    delt = float(args[1]) ** 2 - 4 * float(args[0]) * float(args[2])
    if delt < 0:
        return 'Não existe raízes reais'
    return f'x1 = {(-float(args[1]) + math.sqrt(delt)) / (2 * float(args[0]))}\n' \
           f'x2 = {(-float(args[1]) - math.sqrt(delt)) / (2 * float(args[0]))}'


bot.privado = {
    '/start': 'Olá, eu sou um bot matemático, digite /help para saber mais sobre mim.',

    '/somar': somar,
    '/subtrair': subtrair,
    '/multiplicar': multiplicar,
    '/dividir': dividir,
    '/potencia': potencia,
    '/raiz': raiz,
    '/fatorial': fatorial,
    '/log': log,
    '/log10': log10,
    '/delta': delta,
    '/raizes': raizes,

    '/help': 'Aqui estão os comandos que eu entendo:\n\n'
             '/somar <números> - Soma os números\n'
             '/subtrair <número1> <número2> - Subtrai o número2 do número1\n'
             '/multiplicar <número1> <número2> - Multiplica o número1 pelo número2\n'
             '/dividir <número1> <número2> - Divide o número1 pelo número2\n'
             '/potencia <número1> <número2> - Eleva o número1 à potência número2\n'
             '/delta <a> <b> <c> - Calcula o delta da equação de segundo grau\n'
             '/raizes <a> <b> <c> - Calcula as raízes da equação de segundo grau\n'
             '/raiz <número> - Calcula a raiz quadrada do número\n'
             '/log <número> - Calcula o logaritmo natural do número\n'
             '/log10 <número> - Calcula o logaritmo na base 10 do número\n'
             '/fatorial <número> - Calcula o fatorial do número\n'
}
