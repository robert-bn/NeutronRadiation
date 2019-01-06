#!/usr/bin/env python
# -*- coding: utf8 -*-
import numpy as np
import sys
import json

# Globals
prefix = {-15:'f', -12:'p', -9:'n', -6:'μ', -3:'m', 0:'', 3:'k', 6:'M', 9:'G', 12:'T', 15:'P'}


# Function definitions
def format_time(t):
    # Formats a time
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
    # Latex style superscript
    return "${}^{" + str(x) + "}$"


def format_isotope(X):
    # Formats an isotope name in latex
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
    # Formats a number in latex with correct SI prefixes, or in scientific notation
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


def saturation(n, L, beam_time=60):
    # returns the 1 min saturated *ACTIVITY*
    sat_n = n * (1 - np.exp(-L*beam_time)) / beam_time
    return sat_n


def sat_after(sat, err, t, L):
    return sat * np.exp(-L*t), err * np.exp(-L*t)


def latex_fmt(v, indent='', end=''):
    # formats list of things into latex format
    return indent + (("{} & "*len(v))[:-3] ).format(*v) + end


def mid(list):
    return (np.max(list) + np.min(list))/2


def error(list):
    return np.max(list) - np.min(list)


def make_table(fileNames, run=3, isotopes=["O15", "C10", "C11", "O14"], nProtons=1e11, indent=4):
    # Formats a latex table from the output json file of wateractivation/rangeshifter
    indt = indent * ' '

    # Opening command
    table = "\\begin{tabular}{c|c|c|c|c|c|c}\n"

    # Header
    header = ["Isotope", "Half Life", "Number (EOB)", "Activity (EOB)", "Activity (1m)", "Activity (2m)", "Activity (5m)"]
    table += latex_fmt(header, indent=indt, end=" \\\\\n")

    # Horizontal rule
    table += indt + "\\hline\n"

    # Table content
    for isotope in isotopes:
        sat_act_list = []
        half_life_list = []
        number_list = []

        # Loop though filenames
        for fileName in fileNames:
            # Load data
            with open(fileName) as f:
                data = json.load(f)

            number_list.append(nProtons * data[run]['isotopes'][isotope]['number']/data[run]['nEvents'])
            half_life_list.append(data[run]['isotopes'][isotope]['halfLife'])
            sat_act_list.append(saturation(number_list[-1], L=np.log(2)/half_life_list[-1]))

        number = mid(number_list)
        half_life = mid(half_life_list)
        sat_act = mid(sat_act_list)
        sat_err = error(sat_act)

        onemin, onemin_err = sat_after(sat_act, sat_err, 60, L=np.log(2)/half_life_list[-1])
        twomin, twomin_err = sat_after(sat_act, sat_err, 120, L=np.log(2)/half_life_list[-1])
        fivemin, fivemin_err = sat_after(sat_act, sat_err, 300, L=np.log(2)/half_life_list[-1])

        name = format_isotope(isotope)
        half_life_str = format_time(half_life)
        num_pm_error = formatnum(number, err=error(number_list))
        sat_act_str = formatnum(sat_act, unit='Bq', SIprefix=True, err=sat_err)
        onemin_str = formatnum(onemin, unit='Bq', SIprefix=True, err=onemin_err)
        twomin_str = formatnum(twomin, unit='Bq', SIprefix=True, err=twomin_err)
        fivemin_str  = formatnum(fivemin, unit='Bq', SIprefix=True, err=fivemin_err)

        row = [name, half_life_str, num_pm_error, sat_act_str, onemin_str, twomin_str, fivemin_str]

        table += latex_fmt(row, indent=indt, end=" \\\\\n")

    # Closing command
    table +="\\end{tabular}\n"
    return table


# Main
print(make_table(["rangeshifter_t1_BIC.json", "rangeshifter_t1_BERT.json"], 3))
