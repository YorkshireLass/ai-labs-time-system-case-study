"""
Backend application to calculate coordinates at discrete time steps until a maximum number of time steps is reached.
"""
import sys
import logging
from fastapi import FastAPI, Request, HTTPException

from backend.helpers import generate_next

# Set up log
log = logging.getLogger()
log.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
handler.setFormatter(formatter)
log.addHandler(handler)

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Welcome!"}


@app.get("/calculate_coordinates")
async def calculate_coordinates(request: Request):
    """
    Calls generator to calculate coordinates until max time step is reached (default max_N = 20).

    Args:
        x0 (float)      : User initial x coordinate
        y0 (float)      : User initial y coordinate
        z0 (float)      : User initial z coordinate

        sigma (float)   : User parameter
        rho (float)     : User parameter
        beta (float)    : User parameter

        delta_t (int)   : User time delta input
        max_n (int)     : Maximum time step

    Returns:
        calculate_coordinates (dict) : Dictionary of resulting coordinates for each step n until max_n is reached
        {"Results":[{"n":0,"x":0,"y":0,"z":0}, ..., {"n":max_n, ...}]}
    """
    request_query_params = {item[0]: item[1] for item in request.query_params.multi_items()}
    log.info(f"Received request.")

    # checking for additional parameters provided
    accepted_params = ['x0', 'y0', 'z0', 'sigma', 'rho', 'beta', 'delta_t', 'max_n']
    extra_params = [key for key in request_query_params if key not in accepted_params]
    if extra_params:
        message = f"Parameters {extra_params} are not accepted. Accepted parameters are {accepted_params}."
        log.error(message)
        raise HTTPException(status_code=400, detail=message)

    # checking if infinate value has been given for any parameter
    inf_values = [key for key in request_query_params if request_query_params[key] == "inf"]
    if inf_values:
        message = f"Infinite value given for {inf_values}. Enter Real numbers only."
        log.error(message)
        raise HTTPException(status_code=422, detail=message)

    # formatting inputted values for step 0 - try each parameter key otherwise set the default
    try:
        x       = float(request_query_params['x0'])     if 'x0' in request_query_params else 0
        y       = float(request_query_params['y0'])     if 'y0' in request_query_params else 0
        z       = float(request_query_params['z0'])     if 'z0' in request_query_params else 0
        sigma   = float(request_query_params['sigma'])  if 'sigma' in request_query_params else 1
        rho     = float(request_query_params['rho'])    if 'rho' in request_query_params else 1
        beta    = float(request_query_params['beta'])   if 'beta' in request_query_params else 1
        delta_t = int(request_query_params['delta_t'])  if 'delta_t' in request_query_params else 1
        max_n   = int(request_query_params['max_n'])    if 'max_n' in request_query_params else 20
    except ValueError as e:
        message = f"{e}"
        log.error(message)
        raise HTTPException(status_code=422, detail=message)
    except Exception as e:
        message = f"{e}"
        log.error(message)
        raise HTTPException(status_code=500, detail=message)

    # initialise step 0 counter and coordinates output for n=0
    n = 0 
    results = [{
            "n": n,
            "x": x,
            "y": y,
            "z": z
        }]

    # while step counter n is less than max time step, calculate next coordinates
    while n < max_n:
        coordinates = list(generate_next(x, y, z, sigma, rho, beta, delta_t))
        x = coordinates[0][0]
        y = coordinates[0][1]
        z = coordinates[0][2]
        n += delta_t
        results.append({
            "n": str(n),
            "x": str(x),
            "y": str(y),
            "z": str(z)
        })
    
    log.info(f"Successfully calculated coordinates.")
    return {"Results": results}
    