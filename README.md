binsort is a simple Python package for using binning-based approximate sorting.

To build binsort, you need a Go compiler. For stafnrod users, there is already one one sherlock, but otherwise, you should follow the instructions [here](https://go.dev/doc/install). Then, run `./build.sh` to compile the library. To test if things are working, run binsort.py: this will run tests and benchmarks.

There's only one function in the Python library, `binsort.binsort(x, bins=-1, log_bins=-1)`. `x` is the data being sorted, and the number of bins used is specified by either `bins` or `log_bins` (which uses logarithmically-spaced bins). It returns the order of the sorted array in the same way as `np.argsort()`.

Here's a table showing performance with uniform distributions and `bins=10000`.

```
100000 - argsort: 0.009 s binsort: 0.001 s
 1e+06 - argsort: 0.109 s binsort: 0.008 s
 1e+07 - argsort: 1.603 s binsort: 0.114 s
 1e+08 - argsort: 21.277 s binsort: 1.460 s
```

Note that setting `log_bins` takes a logarithm of all values, which costs more than the sorting itself.