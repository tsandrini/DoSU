"""
__/\\\\\\\\\\\\______________________/\\\\\\\\\\\____/\\\________/\\\_
 _\/\\\////////\\\__________________/\\\/////////\\\_\/\\\_______\/\\\_
  _\/\\\______\//\\\________________\//\\\______\///__\/\\\_______\/\\\_
   _\/\\\_______\/\\\_____/\\\\\______\////\\\_________\/\\\_______\/\\\_
    _\/\\\_______\/\\\___/\\\///\\\_______\////\\\______\/\\\_______\/\\\_
     _\/\\\_______\/\\\__/\\\__\//\\\_________\////\\\___\/\\\_______\/\\\_
      _\/\\\_______/\\\__\//\\\__/\\\___/\\\______\//\\\__\//\\\______/\\\__
       _\/\\\\\\\\\\\\/____\///\\\\\/___\///\\\\\\\\\\\/____\///\\\\\\\\\/___
        _\////////////________\/////_______\///////////________\/////////_____

Created by Tomáš Sandrini
"""


import setuptools


try:
    import dosu
except (ImportError, SyntaxError):
    print("error: dosu requires Python 3.5 or greater.")
    quit(1)



VERSION = dosu.__version__
DOWNLOAD = "https://github.com/tsandrini/dosu/archive/%s.tar.gz" % VERSION


setuptools.setup(
    name="dosu",
    version=VERSION,
    author="Tomáš Sandrini",
    author_email="tomas.sandrini@seznam.cz",
    description="Small utility for writing notes in vim-pandoc environment",
    long_description="Small utility for writing notes in vim-pandoc environment",
    license="MIT",
    url="https://github.com/tsandrini/dosu",
    download_url=DOWNLOAD,
    classifiers=[
        "Environment :: X11 Applications",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ],
    packages=["dosu"],
    entry_points={
        "console_scripts": ["dosu=dosu.__main__:main"]
    },
    python_requires=">=3.5",
    test_suite="tests",
    include_package_data=True
)
