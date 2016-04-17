from os import walk

__doc__ = """

"""

_, _, f = next(walk(__path__[0]))


for name in f:
    if name.endswith(".py") and not name.startswith("__"):
        __doc__ = """{doc}
{module}
{underscores}
    .. automodule:: extensions.{module}
        :members:
""".format(doc=__doc__, module=name[:-3], underscores="=" * (len(name) - 3))
