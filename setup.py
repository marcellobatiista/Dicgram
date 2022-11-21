from setuptools import setup
from dicgram import version
from dicgram import autor
from dicgram import email


with open("README.md", encoding="utf-8") as f:
    readme = f.read()

with open("requirements.txt", encoding="utf-8") as r:
    requires = [i.strip() for i in r]

setup(
    name='dicgram',
    version=version,
    description='Framework para criar bots do Telegram',
    long_description=readme,
    long_description_content_type='text/markdown',

    url='https://github.com/marcellobatiista/dicgram',
    author=autor,
    author_email=email,

    license='MIT',
    keywords='telegram chat messenger api client library python',
    python_requires='>=3.7',
    packages=['dicgram'],
    install_requires=requires
)

