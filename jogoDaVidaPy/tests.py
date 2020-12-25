import unittest
from Category import Category

"""
python3 -m unittest tests.TestStringMethods.test_nodes
python3 -m unittest tests.TestStringMethods.test_category
python3 -m unittest tests.TestStringMethods.test_inside_of_category

"""

class TestStringMethods(unittest.TestCase):
    tipos = Category()
    # tipos.get_categories()["entity"]["True"] = {}

    def test_exists(self):
        self.assertTrue( self.tipos.category_exists("entity") )
        self.assertTrue( self.tipos.category_exists("person") )
        self.assertTrue( self.tipos.category_exists("robber") )
        self.assertTrue( self.tipos.category_exists("building") )
        # self.assertTrue( self.tipos.category_exists("True") )

        self.assertFalse( self.tipos.category_exists("bulding") )
        self.assertFalse( self.tipos.category_exists("") )
        self.assertFalse( self.tipos.category_exists("PERSON") )
        self.assertFalse( self.tipos.category_exists(True) )

    def test_nodes(self):
        entity = self.tipos.get_categories()["entity"]
        obj = self.tipos.get_categories()["object"]
        cake = self.tipos.get_categories()["cake"]

        self.assertEqual(self.tipos.node_category(entity), "entity")
        self.assertEqual(self.tipos.node_super_category(entity), None)
        self.assertEqual(self.tipos.node_sub_categories(entity), ["person", "object", "animal"])

        self.assertEqual(self.tipos.node_category(obj), "object")
        self.assertEqual(self.tipos.node_super_category(obj), "entity")
        self.assertEqual(self.tipos.node_sub_categories(obj), ["food", "weapon"])

        self.assertEqual(self.tipos.node_category(cake), "cake")
        self.assertEqual(self.tipos.node_super_category(cake), "food")
        self.assertEqual(self.tipos.node_sub_categories(cake), [])
    
    def test_category(self):
        entity = "entity"
        obj = "object"
        cake = "cake"

        self.assertEqual(self.tipos.get_super_category(entity), None)
        self.assertEqual(self.tipos.get_sub_categories(entity), ["person", "object", "animal"])

        self.assertEqual(self.tipos.get_super_category(obj), "entity")
        self.assertEqual(self.tipos.get_sub_categories(obj), ["food", "weapon"])

        self.assertEqual(self.tipos.get_super_category(cake), "food")
        self.assertEqual(self.tipos.get_sub_categories(cake), [])
    
    def test_inside_of_category(self):
        self.assertFalse(self.tipos.inside_of_category("machine_gun", "machine_gun"))
        self.assertTrue(self.tipos.inside_of_category("machine_gun", "firearm"))
        self.assertTrue(self.tipos.inside_of_category("machine_gun", "entity"))

        self.assertTrue(self.tipos.inside_of_category("object", "entity"))
        self.assertFalse(self.tipos.inside_of_category("object", "object"))
        self.assertFalse(self.tipos.inside_of_category("object", "firearm"))

if __name__ == '__main__':
    unittest.main()


