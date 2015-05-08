from distutils.core import setup

setup(
    name = "vncdesk",
    version = "1.0.0",
    author = "Felix E. Klee",
    author_email = "felix.klee@inka.de",
    url = "https://github.com/feklee/vncdesk",
    packages = ["vncdesk"],
    scripts = ["bin/vncdesk"],
    license = "WTFPL",
    description = "Runs applications via VNC. Allows scaling applications.",
    long_description = open('README.rst').read()
)
