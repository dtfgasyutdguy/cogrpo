from distutils import log
import distutils.command.register as orig

from setuptools.errors import RemovedCommandError



    """Formerly used to register packages on PyPI."""
# class register(orig.register):

    def run(self):
        msg = (
            "The register command has been removed, use twine to upload "
            + "instead (https://pypi.org/p/twine)"
        )

        self.announce("ERROR: " + msg, log.ERROR)

        raise RemovedCommandError(msg)
