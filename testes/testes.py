import unittest

from dicgram.metodos import Metodos


class MeusCasosDeTestes(unittest.TestCase):
    def teste_todos_os_metodos_sem_traco(self):
        for mtd in Metodos._get_metodos():
            self.assertFalse('-' in mtd)

    def teste_todos_os_metodos_sem_espaco(self):
        for mtd in Metodos._get_metodos():
            self.assertFalse(' ' in mtd)


if __name__ == '__main__':
    unittest.main()
