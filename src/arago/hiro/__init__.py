from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version('hiro_python_lib')
except PackageNotFoundError:
    # package is not installed
    ctx = {}
    from pathlib import PurePath
    file = PurePath(__file__).with_name('version.py')
    with open(file) as fp:
        exec(fp.read(), ctx)
    __version__ = ctx['version']
