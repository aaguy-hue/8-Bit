// Taken largely from pyConnect4
// https://github.com/nwestbury/pyConnect4/blob/644d1adcaf9b5c40090d76ff817c86308b0cba9b/Player.py#L21

// #include <Python.h>
#include <stdbool.h>
#include <stdio.h>


// static PyObject *method_fputs(PyObject *self, PyObject *args)
// {
    
// }

static int best_column(unsigned long long mask, unsigned long long position)
{
    unsigned long long opp_board = mask ^ position;


    return 1;
}

bool canPlay(int col, unsigned long long mask)
{
    
    if (mask ) {
        return false;
    } else {
        return true;
    }
}

static unsigned long long top_mask(int col, int height) {
    return UINT64_C(1) << ;
}