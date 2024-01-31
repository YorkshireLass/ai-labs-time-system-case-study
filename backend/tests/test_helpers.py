import json
import pytest

from backend.helpers import generate_next


class TestHelpersClass:
    """
    Class to define tests for helpers.
    """

    @pytest.mark.parametrize(
            "input,expected",
            [
                (
                    '{"x" : 0, "y" : 0, "z" : 0, "sigma" : 1, "rho" : 1, "beta" : 1, "delta_t" : 1}',
                    (0.0, 0.0, 0.0)
                )
                ,(
                    '{"x" : 1, "y" : 4000, "z" : -200, "sigma" : -1, "rho" : 0.5, "beta" : 3.14, "delta_t" : 2}',
                    (1599601.0, 1604401.0, 9056.0)
                )
            ]
    )
    def test_generate_next(self, input, expected):
        # formatting input
        input_dict = json.loads(input)
            
        # obtaining next generated step
        coordinates = list(generate_next(input_dict['x'], input_dict['y'], input_dict['z'], input_dict['sigma'], input_dict['rho'], input_dict['beta'], input_dict['delta_t']))

        # formatting coordinates
        x = coordinates[0][0]
        y = coordinates[0][1]
        z = coordinates[0][2]
        
        # checking result is as expected
        assert (x, y, z) == expected