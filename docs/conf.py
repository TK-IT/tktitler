# -*- coding: utf-8 -*-
import datetime
import os
import pkginfo
import sys

sys.path.insert(0, os.path.abspath('..'))
pkg_info = pkginfo.Develop(os.path.join(os.path.dirname(__file__), '..'))


# -- General configuration ------------------------------------------------
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    ]

templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'

project = pkg_info.name
copyright = '1956-%s TAAGEKAMMERET' % datetime.datetime.now().year
author = 'TK-IT'

version = release = pkg_info.version

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
