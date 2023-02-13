# ![Dicgram](https://img.icons8.com/color/48/null/neuron.png) Dicgram

Dicgram é um Framework simples para criação de bots para o Telegram em Python

## Instalação 

`pip install dicgram` ou `python setup.py install`

O uso dele é bem simples, basta criar um arquivo principal e importar o Dicgram, e criar uma instância do Bot.

### Classe `Bot`

A classe `Bot` é a classe principal do módulo `dicgram.cliente`.
Ela é responsável por fazer a conexão com o Telegram e gerenciar os eventos.

Parâmetros:

* **token** (`str`) - O token do bot que você recebeu do BotFather.
* **polling** (`bool`, _opcional_) - Se o bot deve receber atualizações de novas mensagens. Padrão é `True`.
* **polling_rate** (`float` | `int`, _opcional_) - O tempo de espera, em segundos, para receber uma resposta do Telegram. Padrão é `0.5`.
* **webhook_url** (`str`, _opcional_) - A URL do webhook. Padrão é `None`.
* **webhook_port** (`int`, _opcional_) - A porta do server para o webhook. Padrão é `8000`.


### Comandos

Os comandos são criados em um dicionário, onde a chave é o comando e o valor é uma string 
que será enviada como resposta ao comando enviado pelo usuário.


### Exemplo de uso básico

```python
from dicgram import Bot

bot = Bot('<TOKEN>')

# Responde aos comandos no privado
bot.privado = {
    '/start': 'Olá, mundo! Eu sou um bot!',
    '/help': 'Em que posso ajudar? :)',
}

# Responde aos comandos em canais e grupos
bot.publico = {
    '/start': 'Olá, mundo! (publico)',
    '/help': 'Em que posso ajudar, (publico)?',
}

# Usuário privado: /start 
# Bot: Olá, mundo! Eu sou um bot!

# Usuário público: /start
# Bot: Olá, mundo! (publico)

# Usuário privado: /help
# Bot: Em que posso ajudar? :)

# Usuário público: /help
# Bot: Em que posso ajudar, (publico)?
````

Além disso, é possível criar comandos com parâmetros, que serão passados como argumentos para a função manipuladora.

### Exemplo de uso intermediário

```python
from dicgram import Bot

bot = Bot('<TOKEN>')

def soma(mim, msg, args):
    return sum(map(int, args))

bot.privado = {
    '/soma': soma,
}

# Usuário: /soma 1 2 3
# Bot: 6

# Usuário: /soma 1 2 3 4 5 6 7 8 9 10
# Bot: 55

# Usuário: /soma 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20
# Bot: 210
```

Quer tornar seu bot mais dinâmico? Existem dois argumentos de fluxo opcionais para a função manipuladora, `mim` e `msg`.

O primeiro é um objeto da classe `Bot`, que contém informações do seu bot e métodos da API do Telegram para enviar mensagens, arquivos, etc.

O segundo é um objeto da classe `Mensagem`, que contém informações sobre a mensagem enviada pelo usuário,
como o ID do usuário, o nome do usuário, o ID do chat, o tipo do chat, etc. 


### Exemplo de uso intermediário ||

```python
from dicgram import Bot

bot = Bot('<TOKEN>')

def consultar_cotacao(mim, msg, args):
    if not args:
        mim.send_message(chat_id=msg.from_user.id, text='Você precisa informar o nome da moeda.')
        return 'Uma mensagem foi enviada para você no privado.'

    moeda = args[0].upper()
    if moeda not in ('USD', 'EUR', 'BTC'):
        bot.send_message(chat_id=msg.from_user.id, text='Moeda inválida.')
        return 'Enviei uma mensagem para você no privado.'

    cotacao = {
        'USD': 3.75,
        'EUR': 4.20,
        'BTC': 50000.00,
    }[moeda]

    return f'A cotação do {moeda} é {cotacao}.'


bot.privado['/start'] = 'Olá, mundo! Eu sou um bot!'
bot.publico['/cotacao'] = consultar_cotacao


# Usuário público: /cotacao
# Bot privado: Você precisa informar o nome da moeda.
# Bot público: Uma mensagem foi enviada para você no privado.

# Usuário público: /cotacao usd
# Bot publico: A cotação do USD é 3.75.

# Usuário público: /cotacao xyz
# Bot privado: Moeda inválida.
# Bot público: Enviei uma mensagem para você no privado.

# Usuário privado: /start
# Bot: Olá, mundo! Eu sou um bot!
```

Tem certos momentos em que você quer que o bot responda a uma mensagem específica, sem que seja necessário um comando.
Para isso, você pode usar chaves de eventos para o dicionário de comandos.

No momento, existem três chaves de eventos: 

 - `@mensagem`
 - `@edit`
 - `@chat`

A chave `@mensagem` é usada para responder a eventos de mensagens novas.

A chave `@chat` é usada para responder a eventos do 
que acontece no chat, como um novo usuário entrando no grupo, um usuário saindo do grupo, etc. 

A chave `@edit` é usada para 
responder a eventos de mensagens editadas pelo usuário.

### Exemplo de uso avançado

```python
from dicgram import Bot

bot = Bot(token='<TOKEN>')

usuarios = {}
chat = None


def contador_de_mensagens(mim, msg, args):
    global chat
    chat = msg.chat.id

    if msg.from_user.id not in usuarios:
        usuarios[msg.from_user.id] = 1
    else:
        usuarios[msg.from_user.id] += 1


def mostrar_contagem(mim, msg, args):
    if msg.from_user.id in usuarios:
        nome = msg.from_user.first_name
        return f'{nome}, você já mandou {usuarios[msg.from_user.id]} mensagens'
    else:
        return 'Você ainda não mandou nenhuma mensagem'


def desligar_contador(mim, msg, args):
    mim.publico.pop('@mensagem', None)
    usuarios.clear()
    mim.send_message(chat_id=chat,
                    text='Pessoas, o contador de mensagens foi desligado pelo admin')
    return 'Contador de mensagens desligado!'


bot.publico = {
    '@mensagem': contador_de_mensagens,
    '/contagem': mostrar_contagem,
}
bot.privado['/desligar'] = desligar_contador

# Usuário1 público: /contagem
# Bot público: Você ainda não mandou nenhuma mensagem

# Usuário1 público: Olá, mundo!

# Usuário1 público: /contagem
# Bot público: Dev, você já mandou 1 mensagens

# Usuário privdao: /desligar
# Bot privado: Contador de mensagens desligado!
# Bot público: Pessoas, o contador de mensagens foi desligado pelo admin
```

Os métodos da API do Telegram são acessados através da instância da classe `Bot`.
Por exemplo, o método send_message é acessado através de `bot.send_message`.
O nome dos métodos é o mesmo da API do Telegram, mas em snake_case.

A documentação da API do Telegram pode ser encontrada [aqui](https://core.telegram.org/bots/api#available-methods).

### Exemplo de uso de métodos da API do Telegram

```python
from dicgram import Bot


bot = Bot(token='<TOKEN>', update=False)

bot.set_chat_title(chat_id='<ID DO GRUPO>', title='Novo título do grupo')
bot.send_location(chat_id='<ID DO GRUPO>', latitude=-23.5505, longitude=-46.6333)
# etc...
```

### Projeto feito por [Marcelo](https://github.com/marcellobatiista)

* [Telegram](https://t.me/@SP4CNE)

### Licença

MIT License

