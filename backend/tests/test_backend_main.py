import json
import pytest
from fastapi.testclient import TestClient

from backend.backend_main import app

client = TestClient(app)


class TestBackendMainClass:
    """
    Class to define tests for backend_main.
    """
    def test_root(self):
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "Welcome!"}


    @pytest.mark.parametrize(
            "input,expected",
            [
                ( # test empty input
                    '',
                    {
                        'response_code': 200,
                        'result': {"Results":[{"n":0,"x":0,"y":0,"z":0},{"n":"1","x":"0","y":"0","z":"0"},{"n":"2","x":"0","y":"0","z":"0"},{"n":"3","x":"0","y":"0","z":"0"},{"n":"4","x":"0","y":"0","z":"0"},{"n":"5","x":"0","y":"0","z":"0"},{"n":"6","x":"0","y":"0","z":"0"},{"n":"7","x":"0","y":"0","z":"0"},{"n":"8","x":"0","y":"0","z":"0"},{"n":"9","x":"0","y":"0","z":"0"},{"n":"10","x":"0","y":"0","z":"0"},{"n":"11","x":"0","y":"0","z":"0"},{"n":"12","x":"0","y":"0","z":"0"},{"n":"13","x":"0","y":"0","z":"0"},{"n":"14","x":"0","y":"0","z":"0"},{"n":"15","x":"0","y":"0","z":"0"},{"n":"16","x":"0","y":"0","z":"0"},{"n":"17","x":"0","y":"0","z":"0"},{"n":"18","x":"0","y":"0","z":"0"},{"n":"19","x":"0","y":"0","z":"0"},{"n":"20","x":"0","y":"0","z":"0"}]}
                    }
                )
                ,( # test default input
                    '{"x0" : 0, "y0" : 0, "z0" : 0, "sigma" : 1, "rho" : 1, "beta" : 1, "delta_t" : 1, "max_n" : 0}',
                    {
                        'response_code': 200,
                        'result': {"Results":[{"n":0,"x":0.0,"y":0.0,"z":0.0}]}
                    }
                )
                ,( # test negative input
                    '{"x0" : -2, "y0" : -999999, "z0" : -0.789365738, "max_n" : 0}',
                    {
                        'response_code': 200,
                        'result': {"Results":[{"n":0,"x":-2.0,"y":-999999.0,"z":-0.789365738}]}
                    }
                )
                ,( # test incorrect parameter passed
                    '{"x" : 1, "max_n" : 0}',
                    {
                        'response_code': 400,
                        'result': {"detail":"Parameters ['x'] are not accepted. Accepted parameters are ['x0', 'y0', 'z0', 'sigma', 'rho', 'beta', 'delta_t', 'max_n']."}
                    }
                )
            ]
    )
    def test_calculate_coordinates(self, input, expected):
        # formatting input otherwise create empty input
        try:
            input_dict = json.loads(input)
        except json.decoder.JSONDecodeError:
            input_dict = {}

        # build query based on input data provided
        request_params = [f"&{key}={input_dict[key]}" for key in input_dict]
        query = "/calculate_coordinates?"
        for param in request_params:
            query += param
        
        # obtain response
        response = client.get(query)

        # check expected response code and result
        assert response.status_code == expected['response_code']
        assert response.json() == expected['result']