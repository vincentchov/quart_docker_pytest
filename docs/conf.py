"""Sphinx configuration."""
project = "Quart Docker Pytest"
author = "Vincent Chov"
copyright = "2022, Vincent Chov"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_click",
    "myst_parser",
]
autodoc_typehints = "description"
html_theme = "furo"
