argsimple
=========

Argsimple is Python package for making clean and useful command line interfaces with as little configuration as humanly possible.

Some of the key features of the packages are:
- Automatic generation of a help page
- Easy declaration of mutually exclusive arguments
- Lazy loading of arguments during runtime

# How to install

Argsimple requires Python version 3.6 or higher.

Install using [pip](https://pip.pypa.io/en/stable/quickstart):

```shell
pip install argsimple
```

# How to use

Here's a simple example:

```python
import argsimple

argsimple.add("-w", "--word", help="a word to print")
argsimple.add("-c", "--count", type=int, help="print this many times")

print(argsimple.word * argsimple.count)
```

```shell
$ python my_scipt.py -w spam -c 3
spamspamspam
```
