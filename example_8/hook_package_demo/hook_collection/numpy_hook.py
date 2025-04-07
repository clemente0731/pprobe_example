def numpy_func_warpper(original_function):
    # function to replace numpy.add with numpy.sub
    def wrapped_f(a, b):
        # call numpy.sub directly instead of add
        print(f"debug: ><>>>>>>> original function being called: {original_function}")
        c = original_function(a, b)
        print(f"debug: ><>>>>>>> result after function execution: {c}")
        print("debug: ><>>>>>>> function execution completed successfully")
        return c
    return wrapped_f