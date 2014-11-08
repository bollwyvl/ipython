# Markdown → IPython Notebook

Kinda like how [docco](http://jashkenas.github.io/docco/) is written in a
markdown file where the the blocks get turned into CoffeeScript, this file 
should be turned into an IPython Notebook with some Markdown cells as well
as some python cells.

    import sys
    sys.argv

That cell would just have some (python) output

[Doctests](https://docs.python.org/2/library/doctest.html) would be really 
cool too...

    >>> [n*n for n in range(6)]
    [0, 1, 4, 9, 16, 25]
    >>> [n**3 for n in range(6)]
    [0, 1, 8, 27, 64, 125]

... that should become have two cells. Who needs multiple outputs? Or widgets?

Fenced code blocks would be great, too:

```python
print "Hello World"
```

That should not output a `%%python` magic, as this is _still_ IPython, after
all.

Non-python things hoping for a magic:

```javascript
alert("hello world");
```

Should have some `%%javascript`, while...

```ruby
>>> print "Hello World"
Hello World
```

..should be `%%ruby`.