# Contains the rate limiting class and API call function
import time
from queue import Queue
from threading import Lock

class RateLimiter:
    def __init__(self, max_calls, period):
        """
        Initializes the RateLimiter with a maximum number of calls and a time period.
        
        :param max_calls: Maximum number of calls allowed within the time period.
        :param period: Time period in seconds within which the max_calls limit applies.
        """
        self.max_calls = max_calls
        self.period = period
        self.calls = Queue(maxsize=max_calls)
        self.lock = Lock()

    def can_call(self):
        """
        Determines if an API call can be made at the current time.
        It checks the timestamp of the oldest call and ensures the rate limit is not exceeded.
        
        :return: True if the call can be made, False otherwise.
        """
        with self.lock:
            current_time = time.time()
            if self.calls.full():
                oldest_call_time = self.calls.queue[0]
                if current_time - oldest_call_time < self.period:
                    return False
                else:
                    self.calls.get()  # Remove the oldest call to make space
            self.calls.put(current_time)  # Record the current call time
            return True

    def wait_and_call(self, call_me_function, input_data):
        """
        Processes each item in input_data by calling call_me_function within rate limits.
        
        :param call_me_function: The function to call (simulating the API).
        :param input_data: List of data to be passed to the function in each call.
        """
        for data in input_data:
            while not self.can_call():
                time.sleep(1)  # Wait until a call can be made
            call_me_function(data)

def call_me(input_data):
    """
    Simulates an API call with the provided input data.
    
    :param input_data: The input data to pass to the API.
    """
    print(f"Calling API with input: {input_data}")
