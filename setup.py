from setuptools import setup
from dicgram import version
from dicgram import autor
from dicgram import email

with open("requirements.txt", encoding="utf-8") as r:
    requires = [i.strip() for i in r]

setup(
    name='dicgram',
    version=version,
    description='Framework para criar bots do Telegram',

    url='https://github.com/marcellobatiista/dicgram',
    author=autor,
    author_email=email,

    license='MIT',

    python_requires='>=3.7',
    packages=['dicgram'],
    install_requires=requires
)

