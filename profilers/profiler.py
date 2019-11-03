# -*- coding: utf-8 -*-
"""Profiling module

This module contains wrapper functions for python code profiling.
Those wrapper functions can both be used as decorators and as regular wrapper functions.
Profiling are saved as csv files under the folder profiling/.

As a decorator :

@<wrapper_func>
def <to_profile_func>(input):
    <code>
    return <output>

As a regular function :

<to_profile_func_output> = <wrapper_func>(<to_profile_func>,<wrapper_func_args>)(<to_profile_func_input>)

"""

import os
import re
import cProfile
import pstats
import io
from line_profiler import LineProfiler


def _line_prof_tocsv(line_prof):
    line_prof = line_prof.replace(';','')
    line_prof = 'Line #' + line_prof.split('Line #')[-1]
    line_prof = ''.join(line_prof.split('='*62+'\n'))
    line_prof = line_prof.split('\n')

    code_index = re.search("Line Contents", line_prof[0]).start()

    out = []
    for line in line_prof:
        num_part = line[:code_index]
        code_part = line[code_index:]
        code_part = ' ' if not code_part else code_part

        if line:
            split = [i.strip() for i in num_part.split('  ') if i]
            if len(split) < 5:
                split[1:1] = ['']*3
            out.append(';'.join(split + [code_part]))
    return '\n'.join(out)


def profileit(func, n_run=1):
    """Profile all functions used in func
    """

    def wrapper(*args, **kwargs):
        datafn = os.path.join('profiling_files',
                              func.__name__ + '_profile.csv')  # Name the data file sensibly
        if 'profiling_files' not in os.listdir(os.getcwd()): os.makedirs('profiling_files')

        pr = cProfile.Profile()
        pr.enable()
        for i in range(n_run):
            retval = func(*args, **kwargs)
        pr.disable()

        result = io.StringIO()
        pstats.Stats(pr, stream=result).print_stats()
        result = result.getvalue()
        result = 'ncalls' + result.split('ncalls')[-1]
        result = result.replace('percall filename:lineno(function)', 'cum_percall function')
        result = '\n'.join([';'.join(line.rstrip().split(None, 5)) for line in result.split('\n')])

        # save it to disk
        with open(datafn, 'w+') as f:
            f.write(result)
            f.close()

        return retval

    return wrapper


def line_profileit(func):
    """ Profile all lines of func
    """
    def wrapper(*args, **kwargs):
        datafn = os.path.join('profiling_files',
                              func.__name__ + '_line_profile.csv')  # Name the data file sensibly
        if 'profiling_files' not in os.listdir(os.getcwd()): os.makedirs('profiling_files')

        lp = LineProfiler()
        lp_wrapper = lp(func)
        retval = lp_wrapper(*args, **kwargs)

        result = io.StringIO()
        lp.print_stats(stream=result)
        result = result.getvalue()

        result = _line_prof_tocsv(result)

        # save it to disk
        with open(datafn, 'w+') as f:
            f.write(result)
            f.close()

        return retval

    return wrapper
