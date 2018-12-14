#!/usr/bin/env python
# -*- coding: utf8 -*-
import numpy as np
import json

# Globals
ist_name = {'Be7':'Be', 'C10':'C', 'C11':'C', 'O14':'O', 'O15':'O', 'F17':'F'}
ist_num = {'Be7':7, 'C10':10, 'C11':11, 'O14':14, 'O15':15, 'F17':15}

prefix = {-6:'μ', -3:'m', 0:'', 3:'k', 6:'M', 9:'G'}

indt = 4 * " "
nProtons = 1e11


# Function definitions
def format_hl(t):
    if t < 60:
        # seconds
        unit = "s"
    elif 60 < t < 3600:
        # minutes
        t = t / 60.0
        unit = 'm'
    elif 3600 < t < 24 * 3600:
        # days
        t = t / (24 * 3600)
        unit = 'd'
    else:
        # years
        t = t / (24 * 3600 * 365.25)
        unit = 'yr'

    return "{:.2f} {}".format(t, unit)


def superscript(x):
    # Latex style
    return "${}^{" + str(x) + "}$"


def format_isotope(X):
    if X == "triton":
        return X
    else:
        sym = ''
        A_num = ''
        for char in X:
            if char.isdigit():
                A_num += char
            else:
                sym += char
        return superscript(A_num) + sym


def formatnum(x, unit='', SIprefix=False, err=None):
    if x < 1e-9:
        return 0
    exponent = int(np.floor(np.log10(x)))
    if SIprefix:
        prefix_exponent = int(3*np.floor(exponent / 3))
        y = x / np.power(10., prefix_exponent)
        if err is not None:
            erry = err / np.power(10., prefix_exponent)
            return "({:.2f} $\\pm$ {}) ".format(y, round(erry,2)) + prefix[prefix_exponent] + unit
        else:
            return "{:.2f} ".format(y) + prefix[prefix_exponent] + unit
    else:
        y = x / np.power(10, exponent)
        if err is not None:
            erry = err / np.power(10, exponent)
            return "({:.2f} $\\pm$ {}) $\\times$ 10 {} ".format(y, round(erry,2), superscript(exponent)) + unit
        else:
            return "{:.2f} $\\times$ 10{} ".format(y, superscript(exponent)) + unit


def saturation(n, error, L, beam_time=60):
    sat_n = n * (1 - np.exp(-L*beam_time)) / beam_time
    sat_err = error * (1 - np.exp(-L*beam_time)) / beam_time
    return sat_n, sat_err


def latex_fmt(v, indent='', end=''):
    # formats list of things into latex format
    return indent + (("{} & "*len(v))[:-3] ).format(*v) + end


def make_table(fileName):
    # Load data
    with open(fileName) as f:
        data = json.load(f)

    # Main
    table = "\\begin{tabular}{c|c|c|c}"

    # Header
    table += indt + "Isotope & Half Life & Total number produced & Saturated activity \\\\\n"
    table += indt + "\\hline\n"
    # Print content
    for isotope in data['isotopes'].keys():
        number = nProtons * data['isotopes'][isotope]['number']/data['nEvents']
        error =  nProtons * np.sqrt(data["isotopes"][isotope]['number'])/data['nEvents']
        half_life = data['isotopes'][isotope]['halfLife']
        name = format_isotope(isotope)
        num_pm_error = formatnum(number, err=error)
        half_life_str = format_hl(half_life)
        sat_act = saturation(number, error, L=np.log(2)/half_life)
        sat_act_str = formatnum(sat_act[0], unit='Bq', SIprefix=True, err=sat_act[1])

        row = [name, half_life_str, num_pm_error, sat_act_str]

        table += latex_fmt(row, indent=indt, end=" \\\\\n")

    # Closing command
    table +="\\end{tabular}\n"
    return table
