import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from qae_notification import main

class TestProductoEntorno(unittest.TestCase):

    def test_producto_entorno_valid_data(self):
        data = "Producto: Producto1 \n Entorno: Entorno1"
        result = main.productoEntorno(data)
        self.assertEqual(result, ["Producto1", "Entorno1"])

    def test_producto_entorno_no_match(self):
        data = "Este texto no contiene información"
        result = main.productoEntorno(data)
        self.assertEqual(result, [])

    def test_producto_entorno_invalid_data(self):
        data = "Producto: Producto2"
        result = main.productoEntorno(data)
        self.assertEqual(result, [])



if __name__ == '__main__':
    unittest.main()
