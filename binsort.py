import ctypes
import numpy as np
import numpy.ctypeslib as ctypeslib
import os.path as path

file_name = path.abspath(__file__)
lib_name = path.join(path.dirname(file_name), "binsort.so")
binsort_lib = ctypes.cdll.LoadLibrary(lib_name)

def _wrap_c_func(c_func, arg_string):
    """ _wrap_c_function is an internal helper function which sets up result
    and argument types. c_func is an external function from a LoadLibrary
    call. arg_string is a string with one character for each argument. Those
    characters give the types of each argument:
    i - integer
    I - integer array
    d - double
    D - double array
    You can add more as needed.

    It returns the input function to make one-liners easier.
    """
    # If you are copy-and-pasting this code into a new project, note that
    # sometimes you don't want restype = None. Read up on how this stuff works
    # before modifying it.
    c_func.restype = None
    args = []
    for c in arg_string:
        if c == "i":
            args.append(ctypes.c_longlong)
        elif c == "d":
            args.append(ctypes.c_double)
        elif c == "I":
            args.append(
                ctypeslib.ndpointer(ctypes.c_longlong, flags="C_CONTIGUOUS")
            )
        elif c == "D":
            args.append(
                ctypeslib.ndpointer(ctypes.c_double, flags="C_CONTIGUOUS")
            )
        else:
            raise ValueError("Unrecognized type character, '%s'", c)
    c_func.argtypes = args
    return c_func
        

_c_binsort = _wrap_c_func(binsort_lib.cApprox, "iII")

def binsort(x, log_bins=-1, bins=-1):
    """ binsort performs an approximate binning-based sort of x and returns
    the order of elements in the same way as np.argsort.
    """
    if bins == -1 and log_bins == -1:
        raise ValueError("Must set log_bins or bins")
    elif bins == -1:
        bins = log_bins
        x = np.log(x)
        
    low, high = np.min(x), np.max(x)
    dx = (high - low)/bins
    idx = np.asarray((x - low)/dx, dtype=int)
    order = np.zeros(len(x), dtype=int)

    _c_binsort(len(idx), idx, order)
    
    return order
    

def test():
    tests = [
        ([0, 1, 2, 3, 4], [0, 1, 2, 3, 4]),
        ([4, 3, 2, 1, 0], [4, 3, 2, 1, 0]),
        ([40, 30, 20, 10, 0], [4, 3, 2, 1, 0]),
        ([0, 0, 2, 2, 1, 1], [0, 1, 4, 5, 2, 3]),
    ]

    random.seed(0)
    for i in range(len(tests)):
        idx, out = tests[i]
        idx, out = np.asarray(idx, dtype=int), np.asarray(out, dtype=int)
        order = np.zeros(len(idx), dtype=int)
        _c_binsort(len(idx), idx, order)

        if not np.all(order == out):
            print("Test %d:" % i)
            print("idx", idx)
            print("out", out)
            print("order", order)
            assert(0)

    print("All _c_binsort tests passed")

    tests = [
        ((1e5, 1e0, 1e10, 1e3, 1e2), (1, 4, 3, 0, 2))
    ]

    for i in range(len(tests)):
        x, out = tests[i]
        x, out = np.array(x), np.asarray(out, dtype=int)
        order = binsort(x, log_bins=20)

        if not np.all(order == out):
            print("Test %d:" % i)
            print("x", x)
            print("out", out)
            print("order", order)
            assert(0)

    print("All binsort tests passed")

    n = int(200)
    x = random.random(n)

    order_1 = binsort(x, bins=1000)
    order_2 = np.argsort(x)
    idx = np.arange(n, dtype=int)
    
    plt.figure()
    plt.plot(idx, x[order_1], ".", c="tab:red")
    plt.savefig("order_comp.png")
    plt.xlabel(r"${\rm order}$")
    plt.ylabel(r"$x$")
    
    benchmarks = [
        (1e5, 100),
        (1e6, 10),
        (1e7, 10),
        (1e8, 1),
    ]

    for i in range(len(benchmarks)):
        n, trials = benchmarks[i]
        n = int(n)

        dt1, dt2 = 0, 0
        for j in range(trials):
            x = random.random(n)
            t0 = time.time()

            np.argsort(x)
            
            t1 = time.time()

            binsort(x, bins=n)
            
            t2 = time.time()
            
            dt1 += t1 - t0
            dt2 += t2 - t1

        dt1 /= trials
        dt2 /= trials
            
        print("%7g - argsort: %6.3f s binsort: %6.3f" % (n, dt1, dt2))
        
if __name__ == "__main__":
    import numpy.random as random
    import time
    import matplotlib.pyplot as plt
    
    test()
