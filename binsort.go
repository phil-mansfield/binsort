package main

import (
	"C"
    "unsafe"
)

//export cApprox 
func cApprox(
	cN C.longlong, cBins *C.longlong,
	cOrder *C.longlong,
) {
	n := int(cN)
	bins := unsafe.Slice((*int)(unsafe.Pointer(cBins)), int(n))
    order := unsafe.Slice((*int)(unsafe.Pointer(cOrder)), int(n))

	approx(bins, order)
}

func approx(bins []int, order []int) {
	nBins := 0
	for i := range bins {
		order[i] = i
		if nBins <= bins[i] {
			nBins = bins[i]+1
		}
	}

	counts := make([]int, nBins+1)
	for i := range bins { counts[1 + bins[i]]++ }
	
	for i := 1; i < len(counts); i++ {
		counts[i] += counts[i-1]
	}
	
	starts := counts[:len(counts) - 1]
	
	for i := range bins {
		j := starts[bins[i]]
		order[j] = i
		starts[bins[i]]++
	}
}
   
func main() { }
