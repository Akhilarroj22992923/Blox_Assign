 # Main script to execute the rate limiting functionality

from rate_limit import RateLimiter, call_me
from data import input_data

# Instantiate the RateLimiter with a limit of 15 calls per minute (60 seconds)
rate_limiter = RateLimiter(max_calls=15, period=60)

# Execute the rate limiter with the sample data
rate_limiter.wait_and_call(call_me, input_data)
