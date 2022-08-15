from pathlib import Path
import sys

# Add project root directory to python path...
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


project = 'matplotview'
copyright = '2022, Isaac Robinson'
author = 'Isaac Robinson'
release = '1.0.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.doctest',
    'sphinx.ext.intersphinx',
    'sphinx.ext.viewcode',
    'numpydoc',
    'matplotlib.sphinxext.mathmpl',
    'matplotlib.sphinxext.plot_directive',
    'sphinx_gallery.gen_gallery'
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

from sphinx_gallery.sorting import FileNameSortKey

sphinx_gallery_conf = {
    "examples_dirs": "../examples",
    "gallery_dirs": "examples",
    "line_numbers": True,
    "within_subsection_order": FileNameSortKey
}

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']
html_css_files = ['gallery_mods.css']

plot_include_source = True
