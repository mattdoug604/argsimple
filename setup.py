from setuptools import setup, find_packages


setup(
    name="argsimple",
    version="0.1.0",
    author="mattdoug604",
    author_email="mattdoug604@gmail.com",
    description="Build a command line interface with as little configuration as possible.",
    url="https://github.com/mattdoug604/argsimple.git",
    license="https://spdx.org/licenses/MIT.html",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
    ],
    python_requires=">=3.6",
    packages=find_packages(),
    install_requires=[],
    tests_require=[],
)
