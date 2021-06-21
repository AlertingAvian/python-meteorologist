"""
Copyright (C) 2021 Patrick Maloney
"""

import unittest
from python_meteorologist import forecast as fc


class ForecastTest(unittest.TestCase):
    def test_missing_user_agent(self):
        with self.assertRaises(TypeError) as context:
            fc.Forecaster()

        self.assertTrue('User Agent is required.' in str(context.exception))

    def test_forecast_properties(self):
        forecaster = fc.Forecaster('Test Application, alertingavian@vivaldi.net')
        forecast = forecaster.get_forecast(20017)
        # properties
        # make sure all are of the correct type
        self.assertEqual(type(forecast.properties.updated), str)
        self.assertEqual(type(forecast.properties.generated_at), str)
        self.assertEqual(type(forecast.properties.update_time), str)
        self.assertEqual(type(forecast.properties.valid_times), str)
        self.assertEqual(type(forecast.properties.elevation), float)
        # make sure all are > 0
        self.assertGreater(len(forecast.properties.updated), 0)
        self.assertGreater(len(forecast.properties.generated_at), 0)
        self.assertGreater(len(forecast.properties.update_time), 0)
        self.assertGreater(len(forecast.properties.valid_times), 0)

    def test_forecast_periods(self):  # do i really have to do it again for the hourly test. plz no
        forecaster = fc.Forecaster('Test Application, alertingavian@vivaldi.net')
        forecast = forecaster.get_forecast(20017)
        # periods list
        for period in forecast.periods:
            # check type
            self.assertEqual(type(period), fc.Period)
        # individual periods
        for period in forecast.periods:
            # number
            self.assertEqual(type(period.number), int, msg=f'Expected type number: int, actual: {type(period.number)}')
            self.assertGreater(period.number, 0)
            # name
            self.assertEqual(type(period.name), str, msg=f'Expected type name: str, actual: {type(period.name)}')
            self.assertGreater(len(period.name), 0)
            # start_time
            self.assertEqual(type(period.start_time), str, msg=f'Expected type start_time: str, actual: '
                                                               f'{type(period.start_time)}')
            self.assertGreater(len(period.start_time), 0)
            # end_time
            self.assertEqual(type(period.end_time), str, msg=f'Expected type end_time: str, actual: '
                                                             f'{type(period.end_time)}')
            self.assertGreater(len(period.end_time), 0)
            # is_day_time
            self.assertEqual(type(period.is_daytime), bool, msg=f'Expected type is_daytime: int, actual: '
                                                                f'{type(period.number)}')
            # temperature
            self.assertEqual(type(period.temperature), int, msg=f'Expected type temperature: int, actual: '
                                                                f'{type(period.temperature)}')
            # temp_unit
            self.assertEqual(type(period.temp_unit), str, msg=f'Expected type temp_unit: str, actual: '
                                                              f'{type(period.temp_unit)}')
            self.assertEqual(len(period.temp_unit), 1)
            # wind_speed
            self.assertEqual(type(period.wind_speed), str, msg=f'Expected type wind_speed: str, actual: '
                                                               f'{type(period.wind_speed)}')
            self.assertGreater(len(period.wind_speed), 0)
            # wind_direction
            self.assertEqual(type(period.wind_direction), str, msg=f'Expected type wind_direction: str, actual: '
                                                                   f'{type(period.wind_direction)}')
            self.assertGreater(len(period.wind_direction), 0)  # what happens if wind speed is 0 and there is no dir
            # icon
            self.assertEqual(type(period.icon), str, msg=f'Expected type icon: str, actual: {type(period.icon)}')
            self.assertTrue('http' in period.icon)
            self.assertGreater(len(period.icon), 0)
            # short_forecast
            self.assertEqual(type(period.short_forecast), str, msg=f'Expected type short_forecast: str, actual: '
                                                                   f'{type(period.short_forecast)}')
            self.assertGreater(len(period.short_forecast), 0)
            # long_forecast
            self.assertEqual(type(period.long_forecast), str, msg=f'Expected type long_forecast: str, actual: '
                                                                  f'{type(period.long_forecast)}')
            self.assertGreater(len(period.long_forecast), 0)


if __name__ == '__main__':
    unittest.main()
