# -*- coding: utf-8 -*-
import ast
import datetime
import os
import sys


def get_package_info(filename):
    '''Get the keyword arguments in the call to setuptools.setup()'''
    with open(filename) as fp:
        tree = ast.parse(fp.read())
    # We assume the module imports setup from setuptools
    # and calls setup() in the last statement of the file.
    last_stm = tree.body[-1]
    assert isinstance(last_stm, ast.Expr)
    setup_call = last_stm.value
    assert isinstance(setup_call, ast.Call)
    assert isinstance(setup_call.func, ast.Name)
    setup_name = 'setup'
    assert setup_call.func.id == setup_name
    # Change "setup(...)" to "setup = dict(...)"
    setup_call.func.id = 'dict'
    tree.body[-1] = ast.Assign([ast.Name(setup_name, ast.Store())], setup_call)
    # Evaluate module and return value of setup variable
    ast.fix_missing_locations(tree)
    globs = {'__file__': filename}
    locs = {}
    eval(compile(tree, filename, 'exec'), globs, locs)
    return locs[setup_name]


module_dir = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(0, module_dir)
pkg_info = get_package_info(os.path.join(module_dir, 'setup.py'))


# -- General configuration ------------------------------------------------
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    ]

templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'

project = pkg_info['name']
copyright = '1956-%s TAAGEKAMMERET' % datetime.datetime.now().year
author = 'TK-IT'

version = release = pkg_info['version']

language = 'da'
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
pygments_style = 'sphinx'
todo_include_todos = False


# -- Options for intersphinx ----------------------------------------------
intersphinx_mapping = {'https://docs.python.org/3/': None}


# -- Options for HTML output ----------------------------------------------
html_static_path = ['_static']


# -- Options for HTMLHelp output ------------------------------------------
htmlhelp_basename = project+'doc'
