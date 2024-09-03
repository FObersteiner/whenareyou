import unittest

from whenareyou import whenareyou, whenareyou_IATA


class TestWhenareyou(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # to run before all tests
        pass

    @classmethod
    def tearDownClass(cls):
        # to run after all tests
        pass

    def setUp(self):
        # to run before each test
        pass

    def tearDown(self):
        # to run after each test
        pass

    def test_whenareyou(self):
        print("\ntesting whenareyou.whenareyou")
        # valid queries
        expected = "Europe/Brussels"
        actual = whenareyou("Brussel, Belgium")
        self.assertEqual(expected, actual)

        expected = "Asia/Taipei"
        actual = whenareyou("Tainan")
        self.assertEqual(expected, actual)

        expected = "America/Chicago"
        actual = whenareyou("Springfield")
        self.assertEqual(expected, actual)

    def test_whenareyou_ivd(self):
        # invalid queries
        ivd = "an invalid address"
        expected = ValueError
        self.assertRaises(expected, whenareyou, ivd)

    def test_whenareyou_IATA(self):
        print("\ntesting whenareyou.whenareyou_IATA")
        # valid queries
        expect = "Asia/Novosibirsk"
        actual = whenareyou_IATA("OVB")
        self.assertEqual(expect, actual)

        expect = "America/Vancouver"
        actual = whenareyou_IATA("yvr")
        self.assertEqual(expect, actual)

        expect = "Asia/Shanghai"
        actual = whenareyou_IATA("  PVG")
        self.assertEqual(expect, actual)

    def test_whenareyou_IATA_ivd(self):
        # invalid queries
        ivd = "123"
        expected = ValueError
        self.assertRaises(expected, whenareyou_IATA, ivd)


if __name__ == "__main__":
    unittest.main()
