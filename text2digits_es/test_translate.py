from .translate import text2digits
import pytest


def test_translate():
    assert '99 PORCENTAJE' == text2digits('99%')
    assert '9' == text2digits('nueve')
    assert '2013' == text2digits('dos mil trece')
    assert 'tengo 2 caballos' == text2digits('tengo dos caballos')
    assert 'tengo 2000 casas' == text2digits('tengo dos mil casas')
    assert 'unas 2405 propiedades' == text2digits(
        'unas dos mil cuatrocientas cinco propiedades')
    assert 'tengo 1800 vinos' == text2digits('tengo mil ochocientos vinos')
    assert '1200000 cosas y 3 casas' == text2digits(
        'Un millón doscientas mil cosas y tres casas')
    assert '125000 cosas y 3 casas' == text2digits(
        'ciento veinticinco mil cosas y tres casas')
    assert '124.3 decimetros, tambien tengo' == text2digits(
        'ciento veinticuatro con treinta decimetros, tambien tengo')
    # assert '124.3 metros tambien  tengo' == text2digits('ciento veinticuatro metros treinta decimetros, tambien tengo')
    assert 'ghjghjg hj con fecha 26 DE JUNIO DEL AÑO 2013 en Granada' == text2digits(
        'ghjghjg hj con fecha VEINTISÉIS DE JUNIO DEL AÑO DOS MIL TRECE en Granada')
    assert 'para responder de 1.250.000 euros de principal; intereses ordinarios durante' == text2digits(
        'para responder de 1.250.000 euros de principal; intereses ordinarios durante'
    )
    assert 'de 31.224,16 Euros y demas' == text2digits(
        'de 31.224,16 Euros y demas')
    assert 'con fecha 22 de Diciembre de 2010' == text2digits(
        'con fecha veintidós de Diciembre de dos mil diez')
    assert '30003' == text2digits('tres hectareas y tres centiareas')
    assert 'de 205871.01 EUROS de' == \
        text2digits(
            'de DOSCIENTOS CINCO MIL OCHOCIENTOS SETENTA Y UN EUROS CON UN CENTIMO de')


def test_ordinals():
    assert '47 es 47 aniversario' == text2digits(
        '47 es cuadragésimo séptimo aniversario')
    assert '692a es 692 (o para aniversarios: 92 del 6 centenario)' == text2digits(
        '692a es sexcentésima nonagésima segunda (o para aniversarios: nonagésimo segundo del sexto centenario)')


@pytest.mark.skip(reason="not yet implemented")
def test_avos():
    assert 'una 9.0909  parte' == text2digits('una once/ava parte')
    assert 'una 9.0909  parte' == text2digits('una once/avo parte')
    assert 'una 9.0909  parte nava' == text2digits('una once/avo parte nava')


if __name__ == '__main__':
    unittest.main()
