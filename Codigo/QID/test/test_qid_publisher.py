import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from qid_publisher import main

class Test_NombreFuncion(unittest.TestCase):

    def prueba1(self):
        print("Hola Mundo!")
        # DEFINICION DE VARIABLES PARA PASAR POR PARÁMETRO
        # LLAMADA A FUNCION GUARDANDO RESULTADO EN VARIABLE
        # COMPROBACION DE RESULTADO RETORNADO CON RESULTADO ESPERADO
        # self.assertEqual(RESULTADO_RETORNADO, RESULTADO_ESPERADO)

    # Crear más funciones aquí

if __name__ == '__main__':
    unittest.main()
