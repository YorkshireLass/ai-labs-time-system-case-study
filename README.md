# AI Labs Time System Case Study

## Initialization

1. **Clone the repository:**
   ```
   git clone https://github.com/YorkshireLass/ai-labs-time-system-case-study.git
   cd ai-labs-time-system-case-study
   ```

2. **Create a virtual environment:**
    ```
    python -m venv venv
    ```

3. **Activate venv and install dependencies:**
    ```
    source venv/bin/activate
    pip install -r requirements.txt
    ```


## Start Dev Server

Ensure your virtual environment is activated before running the below.

```
uvicorn backend_main:app --reload
```

The server will be running at http://127.0.0.1:8000. Open your browser and navigate to this address to see the application in action.

### Calculating coordinates

Navigate to http://127.0.0.1:8000/calculate_coordinates to see the results. Note, if none or not all query parameters are provided then the defaults are used.

The following parameters can be provided (all are optional):

- x0 (float)      : User initial x coordinate
- y0 (float)      : User initial y coordinate
- z0 (float)      : User initial z coordinate
- sigma (float)   : User parameter
- rho (float)     : User parameter
- beta (float)    : User parameter
- delta_t (int)   : User time delta input
- max_n (int)     : Maximum time step

If providing parameters, the results would be queried as follows: http://127.0.0.1:8000/calculate_coordinates?x0=1&y0=1&z0=1&max_n=1

### Running Tests

All tests can be run using:

```
pytest
```

### API Documentation

Swagger documentation can be found at http://127.0.0.1:8000/docs and ReDoc at http://127.0.0.1:8000/redoc.