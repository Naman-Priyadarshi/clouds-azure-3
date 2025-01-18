from flask import Flask, jsonify
import numpy as np
import time
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)

def numerical_integrate(f, lower, upper, N):
    dx = (upper - lower) / N
    x = np.linspace(lower, upper, N)
    return float(sum(f(x) * dx))

def abs_sin(x):
    return np.abs(np.sin(x))

@app.route('/')
def home():
    routes = []
    for rule in app.url_map.iter_rules():
        routes.append({
            'endpoint': rule.endpoint,
            'methods': list(rule.methods),
            'path': str(rule)
        })
    
    return jsonify({
        'status': 'online',
        'message': 'Numerical Integration Service is running',
        'usage': '/numericalintegral/<lower>/<upper>',
        'registered_routes': routes
    })

# Changed from float:lower to string parameters
@app.route('/numericalintegral/<lower>/<upper>')
def compute_integral(lower, upper):
    logger.info(f"Received request with lower={lower}, upper={upper}")
    
    try:
        # Convert string parameters to float
        lower_bound = float(lower)
        upper_bound = float(upper)
        
        results = []
        N_values = [10, 100, 1000, 10000, 100000, 1000000]
        
        for N in N_values:
            start_time = time.time()
            result = numerical_integrate(abs_sin, lower_bound, upper_bound, N)
            end_time = time.time()
            
            results.append({
                'N': N,
                'result': result,
                'computation_time': end_time - start_time
            })
        
        response = {
            'status': 'success',
            'input': {
                'lower_bound': lower_bound,
                'upper_bound': upper_bound
            },
            'results': results
        }
        
        logger.info("Successfully computed integral")
        return jsonify(response)
    
    except ValueError as e:
        logger.error(f"Invalid input: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': 'Invalid input: Please provide valid numbers for lower and upper bounds'
        }), 400
    except Exception as e:
        logger.error(f"Error: {str(e)}", exc_info=True)
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 400

if __name__ == '__main__':
    port = 6969
    logger.info(f"Starting server on port {port}")
    app.run(host='0.0.0.0', port=port, debug=True)
