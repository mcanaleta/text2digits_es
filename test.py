import unittest
from text2digits_es import text2digits


class TestText2DigitsEs(unittest.TestCase):
    def test_translate(self):
        self.assertEqual('99 PORCENTAJE', text2digits('99%'))
        self.assertEqual('9', text2digits('nueve'))
        self.assertEqual('2013', text2digits('dos mil trece'))
        self.assertEqual('tengo 2 caballos', text2digits('tengo dos caballos'))
        self.assertEqual('tengo 2000 casas',
                         text2digits('tengo dos mil casas'))
        self.assertEqual('unas 2405 propiedades', text2digits(
            'unas dos mil cuatrocientas cinco propiedades'))
        self.assertEqual('tengo 1800 vinos', text2digits(
            'tengo mil ochocientos vinos'))
        self.assertEqual('1200000 cosas y 3 casas', text2digits(
            'Un millón doscientas mil cosas y tres casas'))
        self.assertEqual('125000 cosas y 3 casas', text2digits(
            'ciento veinticinco mil cosas y tres casas'))
        self.assertEqual('124.3 decimetros, tambien tengo', text2digits(
            'ciento veinticuatro con treinta decimetros, tambien tengo'))
        # self.assertEqual('124.3 metros tambien  tengo', text2digits('ciento veinticuatro metros treinta decimetros, tambien tengo'))
        self.assertEqual('ghjghjg hj con fecha 26 DE JUNIO DEL AÑO 2013 en Granada', text2digits(
            'ghjghjg hj con fecha VEINTISÉIS DE JUNIO DEL AÑO DOS MIL TRECE en Granada'))
        self.assertEqual('para responder de 1.250.000 euros de principal; intereses ordinarios durante', text2digits(
            'para responder de 1.250.000 euros de principal; intereses ordinarios durante'
        ))
        self.assertEqual('de 31.224,16 Euros y demas', text2digits(
            'de 31.224,16 Euros y demas'))
        self.assertEqual('con fecha 22 de Diciembre de 2010', text2digits(
            'con fecha veintidós de Diciembre de dos mil diez'))
        self.assertEqual('30003', text2digits(
            'tres hectareas y tres centiareas'))
        self.assertEqual('de 205871.01 EUROS de',
                         text2digits(
                             'de DOSCIENTOS CINCO MIL OCHOCIENTOS SETENTA Y UN EUROS CON UN CENTIMO de'))

    def test_ordinals(self):
        self.assertEqual('47 es 47 aniversario', text2digits(
            '47 es cuadragésimo séptimo aniversario'))
        self.assertEqual('692a es 692 (o para aniversarios: 92 del 6 centenario)', text2digits(
            '692a es sexcentésima nonagésima segunda (o para aniversarios: nonagésimo segundo del sexto centenario)'))

    @unittest.skip("needs to be fixed, already broken in the fork")
    def test_avos(self):
        self.assertEqual('una 9.0909  parte',
                         text2digits('una once/ava parte'))
        self.assertEqual('una 9.0909  parte',
                         text2digits('una once/avo parte'))
        self.assertEqual('una 9.0909  parte nava',
                         text2digits('una once/avo parte nava'))


if __name__ == '__main__':
    unittest.main()
