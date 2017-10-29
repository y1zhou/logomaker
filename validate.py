from __future__ import division, print_function
import numpy as np
import pandas as pd
import ast
import inspect
import re
import sys
import numbers
import matplotlib.pyplot as plt

from matplotlib.font_manager import FontProperties
from matplotlib.textpath import TextPath
from character import font_manager

# Need for testing colors
import color
import matplotlib.pyplot as plt
from matplotlib.colors import to_rgb, to_rgba

import warnings

# Revise warning output to just show warning, not file name or line number
def _warning(message, category = UserWarning, filename = '', lineno = -1):
    print('Warning: ' + str(message), file=sys.stderr)

# Comment this line if you want to see line numbers producing warnings
warnings.showwarning = _warning

# Comment this line if you don't want to see warnings multiple times
# warnings.simplefilter('always', UserWarning)


def _try_some_code(code_lines, **kwargs):
    """
    Returns True if any of the supplied lines of code do not throw an error.
    """
    is_valid = False
    for code_line in code_lines:
        try:
            exec(code_line)
            is_valid = True
        except:
            pass
    return is_valid

#
# Parameter specifications
#

# Valid values for matrix_type and logo_type
LOGOMAKER_TYPES = {'counts', 'probability', 'enrichment', 'information'}

# Names of parameters that can take on any float value
params_with_float_values = {
    'shift_first_position_to',
    'xtick_anchor',
    'xtick_rotation',
    'ytick_rotation',
}

# Names of numerical parameters that must be > 0
params_greater_than_0 = {
    'dpi',
    'xtick_spacing',
}

# Names of numerical parameters that must be >= 0
params_greater_or_equal_to_0 = {
    'pseudocount',
    'counts_threshold',
    'edgewidth',
    'boxedgewidth',
    'highlight_edgewidth',
    'highlight_boxedgewidth',
    'max_alpha_val',
    'hpad',
    'vpad',
    'gridline_width',
    'baseline_width',
    'xtick_length',
    'ytick_length',
}

# Names of numerical parameters in the interval [0,1]
params_between_0_and_1 = {
    'alpha',
    'edgealpha',
    'boxalpha',
    'boxedgealpha',
    'highlight_alpha',
    'highlight_edgealpha',
    'highlight_boxalpha',
    'highlight_boxedgealpha',
    'below_shade',
    'below_alpha',
    'width',
    'gridline_alpha',
    'baseline_alpha',
}

# Names of parameters allowed to take on a small number of specific values
params_with_values_in_dict = {
    'matrix_type': LOGOMAKER_TYPES,
    'logo_type': LOGOMAKER_TYPES,
    'enrichment_logbase': [2, np.e, 10],
    'information_units': ['bits', 'nats'],
    'sequence_type': ['dna','DNA', 'rna', 'RNA', 'protein', 'PROTEIN'],
    'stack_order': ['big_on_top', 'small_on_top', 'fixed'],
    'axes_type': ['classic', 'naked', 'everything', 'rails'],
    'gridline_axis': ['x','y','both'],
}

# Names of parameters whose values are True or False
params_with_boolean_values = {
    'enrichment_centering',
    'draw_now',
    'use_transparency',
    'below_flip',
    'uniform_stretch',
    'show_gridlines',
    'show_baseline',
    'show_binary_yaxis',
    'left_spine',
    'right_spine',
    'top_spine',
    'bottom_spine',
    'use_tightlayout',
}

# Names of parameters whose values are strings
params_with_string_values = {
    'save_to_file',
    'characters',
    'ignore_characters',
    'highlight_sequence',
    'max_stretched_character',
    'style_sheet',
    'xtick_format',
    'xlabel',
    'ytick_format',
    'ylabel',
    'title',
}

# Names of parameters whose values specify a numerical interval
params_that_specify_intervals = {
    'position_range',
    'xlim',
    'ylim'
}

# Names of parameters whose values are ordered numerical arrays
params_that_are_ordered_arrays = {
    'xticks',
    'yticks'
}

# Names of parameters that specify color schemes
params_that_specify_colorschemes = {
    'colors',
    'edgecolors',
    'boxcolors',
    'boxedgecolors',
    'highlight_colors',
    'highlight_edgecolors',
    'highlight_boxcolors',
    'highlight_boxedgecolors',
}

# Names of parameters that specify colors:
params_that_specify_colors = {
    'gridline_color',
    'baseline_color',
}


# Names of parameters that specify fontsize
params_that_specify_FontProperties = {
    'font_file': 'fname',
    'font_family': 'family',
    'font_weight': 'weight',
    'font_style': 'style',

    'axes_fontfile': 'fname',
    'axes_fontfamily': 'family',
    'axes_fontweight': 'weight',
    'axes_fontstyle': 'style',
    'axes_fontsize': 'size',

    'tick_fontfile': 'fname',
    'tick_fontfamily': 'family',
    'tick_fontweight': 'weight',
    'tick_fontstyle': 'style',
    'tick_fontsize': 'size',

    'label_fontfile': 'fname',
    'label_fontfamily': 'family',
    'label_fontweight': 'weight',
    'label_fontstyle': 'style',
    'label_fontsize': 'size',

    'title_fontfile': 'fname',
    'title_fontfamily': 'family',
    'title_fontweight': 'weight',
    'title_fontstyle': 'style',
    'title_fontsize': 'size',
}

# Names of parameters that cannot have None value
params_that_cant_be_none = {
    'matrix',
    'matrix_type',
    'pseudocount',
    'enrichment_logbase',
    'enrichment_centering',
    'information_units',
    'counts_threshold',
    'draw_now',
    'shift_first_position_to',
    'colors',
    'alpha',
    'edgecolors',
    'edgealpha',
    'edgewidth',
    'boxcolors',
    'boxalpha',
    'boxedgecolors',
    'boxedgealpha',
    'boxedgewidth',
    'stack_order',
    'use_transparency',
    'below_shade',
    'below_alpha',
    'below_flip',
    'hpad',
    'vpad',
    'width',
    'uniform_stretch',
    'axes_type',
    'rcparams',
    'show_gridlines',
    'show_baseline',
    'xtick_anchor',
    'show_binary_yaxis',
    'use_tightlayout',
}

# Names of parameters to leave for later validatation
params_for_later_validation = {
    'font_family',
    'font_weight',
    'gridline_style',
    'baseline_style',
    'axes_fontfamily',
    'axes_fontweight',
    'tick_fontfamily',
    'tick_fontweight',
    'tick_fontize',
    'label_fontfamily',
    'label_fontweight',
    'title_fontfamily',
    'title_fontweight',
}

#
# Primary validation function
#


def validate_parameter(name, user, default):
    """
    Validates any parameter passed to make_logo or Logo.__init__.
    If user is valid of parameter name, silently returns user.
    If user is invalid, issues warning and retuns default instead
    """

    # Skip if value is none
    if user is None:
        if name in params_that_cant_be_none:
            raise ValueError("Parameter '%s' cannot be None." % name)
        else:
            value = user

    #  If value is in a set
    elif name in params_with_values_in_dict:
        value = _validate_in_set(name, user, default,
                                 params_with_values_in_dict[name])

    # If value is boolean
    elif name in params_with_boolean_values:
        value = _validate_bool(name, user, default)

    # If value is str
    elif name in params_with_string_values:
        value = _validate_str(name, user, default)

    # If value is float
    elif name in params_with_float_values:
        value = _validate_float(name, user, default)

    # If value is float > 0
    elif name in params_greater_than_0:
        value = _validate_float(name, user, default,
                                greater_than=0.0)

    # If value is float >= 0
    elif name in params_greater_or_equal_to_0:
        value = _validate_float(name, user, default,
                                greater_than_or_equal_to=0.0)

    # If value is float in [0,1]
    elif name in params_between_0_and_1:
        value = _validate_float(name, user, default,
                                greater_than_or_equal_to=0.0,
                                less_than_or_equal_to=1.0)

    # If value is an interval
    elif name in params_that_specify_intervals:
        value = _validate_array(name, user, default, length=2)

    # If value is an ordered array
    elif name in params_that_are_ordered_arrays:
        value = _validate_array(name, user, default, increasing=True)

    # If value specifies a color scheme
    elif name in params_that_specify_colorschemes:
        value = _validate_colorscheme(name, user, default)

    # If value specifies a color
    elif name in params_that_specify_colors:
        value = _validate_color(name, user, default)

    # If value specifies FontProperties object
    elif name in params_that_specify_FontProperties:
         passedas = params_that_specify_FontProperties[name]
         value = _validate_FontProperties_parameter(name, user, default,
                                                    passedas=passedas)

    # Special case: matrix
    elif name == 'matrix':
        value = validate_mat(user)

    # Special case: figsize
    elif name == 'figsize':
        value = _validate_array(name, user, default, length=2)

    # Special case: rcparams
    elif name == 'rcparams':
        if type(user)==dict:
            value = user
        else:
            message = "rcparams = %s is not a dictionary. Using %s instead." \
            % (repr(user), repr(default))
            warnings.warn(message, UserWarning)

    # Parameters left for validation later on
    elif name in params_for_later_validation:
        value = user

    # Otherwise, warn if parameter passed through all filters
    else:
        warnings.warn("'%s' parameter not validated." % name, UserWarning)
        value = user

    return value

#
# Private validation functions
#


def _validate_float(name,
                    user,
                    default,
                    greater_than=-np.Inf,
                    greater_than_or_equal_to=-np.Inf,
                    less_than=np.Inf,
                    less_than_or_equal_to=np.Inf,
                    in_set=None):
    """ Validates a floating point parameter. """

    # Test whether parameter can be interpreted as a float
    try:
        value = float(user)

    except ValueError:
        value = default
        message = "Cannot interpret value %s for parameter '%s' as float. " +\
                  "Using default value %s instead."
        message = message % (repr(user), name, repr(default))
        warnings.warn(message, UserWarning)

    # Test inequalities
    if not value > greater_than:
        value = default
        message = "Value %s for parameter '%s' is not greater than %s. " + \
                  "Using default value %s instead."
        message = message % (repr(user), name, repr(greater_than),
                             repr(default))
        warnings.warn(message, UserWarning)

    elif not value >= greater_than_or_equal_to:
        value = default
        message = "Value %s for parameter '%s' is not greater or equal to %s." + \
                  " Using default value %s instead."
        message = message % (repr(user), name, repr(greater_than_or_equal_to),
                             repr(default))
        warnings.warn(message, UserWarning)

    elif not value < less_than:
        value = default
        message = "Value %s for parameter '%s' is not less than %s. " + \
                  "Using default value %s instead."
        message = message % (repr(user), name, repr(less_than),
                             repr(default))
        warnings.warn(message, UserWarning)

    elif not value <= less_than_or_equal_to:
        value = default
        message = "Value %s for parameter '%s' is not less or equal to %s. " + \
                  "Using default value %s instead."
        message = message % (repr(user), name, repr(less_than_or_equal_to),
                             repr(default))
        warnings.warn(message, UserWarning)

    elif (in_set is not None) and not (value in in_set):
        value = default
        message = "Value %s for parameter '%s' is not within the set. " + \
                  "of valid values %s. Using default value %s instead."
        message = message % (repr(user), name, repr(in_set),
                             repr(default))
        warnings.warn(message, UserWarning)

    return value


def _validate_bool(name, user, default):
    """ Validates a floating point parameter. """

    # Test whether parameter is already a boolean
    # (not just whether it can be interpreted as such)
    if isinstance(user, bool):
        value = user

    # If not, return default value and raise warning
    else:
        value = default
        message = "Parameter '%s' assigned a non-boolean value. " +\
                  "Using default value %s instead."
        message = message % (name, repr(default))
        warnings.warn(message, UserWarning)

    return value


def _validate_in_set(name, user, default, in_set):
    """ Validates a parameter with a finite number of valid values. """

    # If user is valid, use that
    if user in in_set:
        value = user

    # If user value is not valid, set to default and issue warning
    else:
        value = default
        message = "Invalid value %s for parameter '%s'. " + \
                           "Using default value %s instead."
        message = message % (repr(user), name, repr(default))
        warnings.warn(message, UserWarning)

    # Return valid value to user
    return value


def _validate_str(name, user, default):
    """ Validates a string parameter. """

    # Test whether parameter can be interpreted as a string
    try:
        value = str(user)

    # If user value is not valid, set to default and issue warning
    except ValueError:
        value = default
        message = "Cannot interpret value %s for parameter '%s' as string. " +\
                  "Using default value %s instead."
        message = message % (repr(user), name, repr(default))
        warnings.warn(message, UserWarning)

    # Return valid value to user
    return value


def _validate_array(name, user, default, length=None, increasing=False):
    """ Validates an array of numbers. """

    try:
        if length is not None:
            assert len(user) == length

        for i in range(len(user)):
            user[i] = float(user[i])

        if increasing:
            for i in range(1, len(user)):
                assert user[i - 1] < user[i]

        value = np.array(user).copy()

    except AssertionError:
        value = default
        message = "Improper value %s for parameter '%s'. " + \
                  "Using default value %s instead."
        message = message % (repr(user), name, repr(default))
        warnings.warn(message, UserWarning)
    # Return valid value to user
    return value

def _validate_colorscheme(name, user, default):
    """ Tests whether user input can be interpreted as a colorschme. """

    # Check whether any of the following lines of code execute without error
    code_lines = [
        'color.color_scheme_dict[user]',
        'plt.get_cmap(user)',
        'to_rgb(user)',
        'expand_color_dict(user)'
    ]

    # Test lines of code
    is_valid = False
    for code_line in code_lines:
        try:
            eval(code_line)
            is_valid = True
        except:
            pass

    # For some reason, this needs to be tested separately.
    if user == 'random':
        is_valid = True

    # If so, then colorscheme is valid
    if is_valid:
        value = user

    # Otherwise, use default colorscheme
    else:
        value = default
        message = "Improper value %s for parameter '%s'. " + \
                  "Using default value %s instead."
        message = message % (repr(user), name, repr(default))
        warnings.warn(message, UserWarning)

    # Return valid value to user
    return value


def _validate_color(name, user, default):
    """ Tests whether user input can be interpreted as an RGBA color. """

    # Check whether any of the following lines of code execute without error
    try:
        to_rgba(user)
        is_valid = True
    except ValueError:
        is_valid = False

    # If so, then colorscheme is valid
    if is_valid:
        value = user

    # Otherwise, use default colorscheme
    else:
        value = default
        message = "Improper value %s for parameter '%s'. " + \
                  "Using default value %s instead."
        message = message % (repr(user), name, repr(default))
        warnings.warn(message, UserWarning)

    # Return valid value to user
    return value

def _validate_FontProperties_parameter(name, user, default, passedas):
    """ Validates any parameter passed to the FontProperties constructor. """

    try:
        # Create a FontProperties object and try to use it for something
        prop = FontProperties(**{passedas:user})
        TextPath((0,0), 'A', size=1, prop=prop)

        value = user
    except ValueError:
        value = default
        message = ("Invalid string specification '%s' for parameter '%s'. "
                   + "Using default value %s instead.") \
                  % (user, name, default)
        warnings.warn(message, UserWarning)

    # Return valid value to user
    return value


def validate_mat(matrix):
    '''
    Runs assert statements to verify that df is indeed a motif dataframe.
    Returns a cleaned-up version of df if possible
    '''

    # Copy and preserve logomaker_type
    matrix = matrix.copy()

    assert type(matrix) == pd.core.frame.DataFrame, 'Error: df is not a dataframe'
    cols = matrix.columns

    for i, col_name in enumerate(cols):
        # Ok to have a 'pos' column
        if col_name=='pos':
            continue

        # Convert column name to simple string if possible
        assert isinstance(col_name,basestring), \
            'Error: column name %s is not a string'%col_name
        new_col_name = str(col_name)

        # If column name is not a single chracter, try extracting single character
        # after an underscore
        if len(new_col_name) != 1:
            new_col_name = new_col_name.split('_')[-1]
            assert (len(new_col_name)==1), \
                'Error: could not extract single character from colum name %s'%col_name

        # Make sure that colun name is not a whitespace character
        assert re.match('\S',new_col_name), \
            'Error: column name "%s" is a whitespace charcter.'%repr(col_name)

        # Set revised column name
        matrix.rename(columns={col_name:new_col_name}, inplace=True)

    # If there is a pos column, make that the index
    if 'pos' in cols:
        matrix.set_index('pos', drop=True, inplace=True)

    # Remove name from index column
    matrix.index.names = [None]

    # Alphabetize character columns
    char_cols = list(matrix.columns)
    char_cols.sort()
    matrix = matrix[char_cols]

    # Return cleaned-up df
    return matrix

def validate_probability_mat(matrix):
    '''
    Verifies that the df is indeed a probability motif dataframe.
    Returns a normalized and cleaned-up version of df if possible
    '''

    # Validate as motif
    matrix = validate_mat(matrix)

    # Validate df values as info values
    assert (all(matrix.values.ravel() >= 0)), \
        'Error: not all values in df are >=0.'

    # Normalize across columns
    matrix.loc[:, :] = matrix.values / matrix.values.sum(axis=1)[:, np.newaxis]

    return matrix
