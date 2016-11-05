import unittest
import texas


class TestTexasMethods(unittest.TestCase):
    def test_is_straight_flush(self):
        cards = texas.Card.create('2A 3A 4A 5A 6A')
        self.assertTrue(texas.is_straight_flush(cards))

        cards = texas.Card.create('2A 7A 4A 5B 6A')
        self.assertFalse(texas.is_straight_flush(cards))

    def test_is_four_of_a_kind(self):
        cards = texas.Card.create('2A 2B 2C 2D 3D')
        self.assertTrue(texas.is_four_of_a_kind(cards))

        cards = texas.Card.create('2A 2B 2B 3B 3A')
        self.assertFalse(texas.is_four_of_a_kind(cards))

    def test_is_full_house(self):
        cards = texas.Card.create('2A 2B 2C 3A 3B')
        self.assertTrue(texas.is_full_house(cards))

        cards = texas.Card.create('2A 3A 4A 5B 6A')
        self.assertFalse(texas.is_full_house(cards))

    def test_is_flush(self):
        cards = texas.Card.create('2A 3A 4A 5A 6A')
        self.assertTrue(texas.is_flush(cards))

        cards = texas.Card.create('2A 3A 4A 5B 6A')
        self.assertFalse(texas.is_flush(cards))

    def test_is_straight(self):
        cards = texas.Card.create('2A 3A 4A 5A 6A')
        self.assertTrue(texas.is_straight(cards))

        cards = texas.Card.create('2A 3A 4A 5B 7A')
        self.assertFalse(texas.is_straight(cards))

    def test_is_three_of_a_kind(self):
        cards = texas.Card.create('2A 2B 2B 5A 6A')
        self.assertTrue(texas.is_three_of_a_kind(cards))

        cards = texas.Card.create('2A 2B 3A 3B 6A')
        self.assertFalse(texas.is_three_of_a_kind(cards))

    def test_is_two_pairs(self):
        cards = texas.Card.create('2A 2B 4A 4B 6A')
        self.assertTrue(texas.is_two_pairs(cards))

        cards = texas.Card.create('2A 3A 4A 5B 6A')
        self.assertFalse(texas.is_two_pairs(cards))

    def test_is_one_pair(self):
        cards = texas.Card.create('2A 2B 4A 5A 6A')
        self.assertTrue(texas.is_one_pair(cards))

        cards = texas.Card.create('2A 3A 4A 5B 6A')
        self.assertFalse(texas.is_one_pair(cards))


if __name__ == '__main__':
    unittest.main()
