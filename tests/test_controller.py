import unittest
from unittest.mock import patch, MagicMock


class TestRelayController(unittest.TestCase):
    @patch("smartcrop.controller.GPIO")
    def test_on_off_active_high(self, mock_gpio):
        # Arrange
        mock_gpio.HIGH = 1
        mock_gpio.LOW = 0

        from smartcrop.controller import RelayController

        # Act
        rc = RelayController(pin=17, active_low=False)
        rc.on()
        rc.off()
        rc.cleanup()

        # Assert
        mock_gpio.setmode.assert_called_once_with(mock_gpio.BCM)
        mock_gpio.setup.assert_called_with(17, mock_gpio.OUT, initial=mock_gpio.LOW)
        mock_gpio.output.assert_any_call(17, mock_gpio.HIGH)
        mock_gpio.output.assert_any_call(17, mock_gpio.LOW)
        mock_gpio.cleanup.assert_called()

    @patch("smartcrop.controller.GPIO")
    def test_on_off_active_low(self, mock_gpio):
        mock_gpio.HIGH = 1
        mock_gpio.LOW = 0

        from smartcrop.controller import RelayController

        rc = RelayController(pin=22, active_low=True)
        rc.on()
        rc.off()

        mock_gpio.setup.assert_called_with(22, mock_gpio.OUT, initial=mock_gpio.HIGH)
        mock_gpio.output.assert_any_call(22, mock_gpio.LOW)
        mock_gpio.output.assert_any_call(22, mock_gpio.HIGH)


if __name__ == "__main__":
    unittest.main()
