import copy
from person import Person
import unittest
from utils import *

class UnitTestMethods(unittest.TestCase):

    def test_person_attribute(self):
        print("TEST: Person Attribute Functionality")
        std_person = Person()
        person1 = copy.deepcopy(std_person)
        person1.set_name("Amy")
        person2 = copy.deepcopy(std_person)
        person2.set_name("Bob")
        self.assertEqual(person1.get_name(), "Amy")
        self.assertEqual(person2.get_name(), "Bob")
        self.assertEqual(person1.get_timestep(), 0)
        person1.update_timestep(status=-1)
        self.assertEqual(person1.get_status(), -1)
        self.assertEqual(person1.get_status_name(), "Recovered")
        self.assertEqual(person1.get_timestep(), 1)

    def test_person_relation(self):
        print("TEST: Person Relationship Functionality")
        std_person = Person()
        person1 = copy.deepcopy(std_person)
        person1.set_name("Amy")
        person2 = copy.deepcopy(std_person)
        person2.set_name("Bob")
        person3 = copy.deepcopy(std_person)
        person3.set_name("Carl")
        person1.add_children("Bob")
        person1.add_children("Carl")
        person2.add_parents("Amy")
        person3.add_parents("Amy")
        self.assertEqual(person1.get_parents(), [])
        self.assertEqual(sorted(person1.get_children()), sorted(["Bob", "Carl"]))
        self.assertEqual(person2.get_parents(), ["Amy"])
        self.assertEqual(person2.get_children(), [])
        self.assertEqual(person3.get_parents(), ["Amy"])
        self.assertEqual(person3.get_children(), [])
        person4 = copy.deepcopy(std_person)
        person4.set_name("Dave")
        person4.add_parents("Amy")
        person4.add_children("Bob")
        self.assertEqual(sorted(person4.get_connected()), sorted(["Amy", "Bob"]))

    def test_utils_probability(self):
        print("TEST: Utils Probability Functionality")
        self.assertTrue(if_success(rate=1)[0])
        self.assertFalse(if_success(rate=0)[0])
        self.assertEqual(get_result(1, 0)[0], 1)
        self.assertEqual(get_result(0, 1)[0], 0)
        self.assertEqual(get_result(0, 0)[0], -1)

if __name__ == '__main__':
    unittest.main()
