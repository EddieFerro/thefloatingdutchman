import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="TheFloatingDutchman",
    version="0.0.6",
    author="Eddie Ferro",
    author_email="eferro1@ufl.edu",
    description="Package for The Floating Dutchman game",
    long_description = long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/EddieFerro/the-floating-dutchman",
    packages=setuptools.find_namespace_packages(include=['thefloatingdutchman','thefloatingdutchman.*']),
    install_requires=['pygame==2.0.0.dev8','numpy>=1.19.0','networkx==2.4'],
    entry_points={'console_scripts': ['TheFloatingDutchman=thefloatingdutchman.main:main']},
    package_data={'':['*.png','*.jpg']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent"
    ],
    python_requires='>=3.8',
)