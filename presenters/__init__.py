from os import scandir


class BasePresenter():
    """
        Acts as a non-functional foundation for a presenter
    """

    def choice(round, colours):
        raise NotImplementedError("Please implement this function in your custom class.")

    def printboard(state):
        raise NotImplementedError("Please implement this function in your custom class.")

    def warn(msg):
        raise NotImplementedError("Please implement this function in your custom class.")


__all__ = []
with scandir("/".join(__file__.split("/")[:-1])) as dirs:
    for entry in dirs:
        if entry.name[-3:] == ".py" and entry.name not in __file__:
	           __all__.append(entry.name[:-3])
