from setuptools import setup

exec(open('vncdesk/version.py').read())

setup(
    name = "vncdesk",
    version = __version__,
    author = "Felix E. Klee",
    author_email = "felix.klee@inka.de",
    url = "https://github.com/feklee/vncdesk",
    packages = ["vncdesk"],
    scripts = ["bin/vncdesk"],
    license = "WTFPL",
    description = "Runs applications via VNC. Allows scaling applications.",
    long_description = open('README.rst').read(),
    zip_safe = True
)
