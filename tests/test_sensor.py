import unittest
from unittest.mock import patch, MagicMock


class TestDHTSensor(unittest.TestCase):
    @patch("smartcrop.sensor.adafruit_dht")
    @patch("smartcrop.sensor.board")
    def test_read_success(self, mock_board, mock_dht):
        # Arrange: mock DHT11 object
        mock_board.D4 = "D4"
        fake_device = MagicMock()
        fake_device.temperature = 31.2
        fake_device.humidity = 45.6
        mock_dht.DHT11.return_value = fake_device

        from smartcrop.sensor import DHTSensor

        s = DHTSensor(pin=mock_board.D4, sensor_type="DHT11")
        t, h = s.read()

        self.assertAlmostEqual(t, 31.2)
        self.assertAlmostEqual(h, 45.6)

    @patch("smartcrop.sensor.adafruit_dht")
    @patch("smartcrop.sensor.board")
    def test_read_runtime_error(self, mock_board, mock_dht):
        mock_board.D4 = "D4"
        # Simulate the sensor raising RuntimeError when accessing temperature
        fake_device = MagicMock()

        def raise_runtime():
            raise RuntimeError("timed out")

        type(fake_device).temperature = property(lambda self: raise_runtime())
        mock_dht.DHT11.return_value = fake_device

        from smartcrop.sensor import DHTSensor

        s = DHTSensor(pin=mock_board.D4, sensor_type="DHT11")
        with self.assertRaises(RuntimeError):
            s.read()


if __name__ == "__main__":
    unittest.main()
