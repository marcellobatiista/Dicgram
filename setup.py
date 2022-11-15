from setuptools import setup
from dicgram import FRAMEWORK_VERSION

with open("requirements.txt", encoding="utf-8") as r:
    requires = [i.strip() for i in r]

setup(
    name='dicgram',
    version=FRAMEWORK_VERSION,
    description='Framework para criar bots do Telegram',

    url='https://github.com/marcellobatiista/dicgram',
    author='Marcelo Batista',
    author_email='batista.marcelo34@gmail.com',

    license='MIT',

    python_requires='>=3.7',
    packages=['dicgram'],
    install_requires=requires
)

