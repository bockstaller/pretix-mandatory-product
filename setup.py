import os
from distutils.command.build import build

from django.core import management
from setuptools import find_packages, setup

from pretix_mandatory_product import __version__


try:
    with open(
        os.path.join(os.path.dirname(__file__), "README.rst"), encoding="utf-8"
    ) as f:
        long_description = f.read()
except Exception:
    long_description = ""


class CustomBuild(build):
    def run(self):
        management.call_command("compilemessages", verbosity=1)
        build.run(self)


cmdclass = {"build": CustomBuild}


setup(
    name="pretix-mandatory-product",
    version=__version__,
    description="Add questions to the contact info section",
    long_description=long_description,
    url="https://github.com/bockstaller/pretix-mandatory-product",
    author="Lukas Bockstaller",
    author_email="lukas.bockstaller@posteo.de",
    license="Apache",
    install_requires=["pretix", "Django"],
    packages=find_packages(exclude=["tests", "tests.*"]),
    include_package_data=True,
    cmdclass=cmdclass,
    entry_points="""
[pretix.plugin]
pretix_mandatory_product=pretix_mandatory_product:PretixPluginMeta
""",
)
