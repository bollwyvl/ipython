# IPython Blockly
Write and execute (very basic) Python visually in the [IPython][ip] web 
notebook using the [Blockly][blk] visual programming language.

# Motivation
A proof of concept for a non-trivial custom web notebook cell.

# Dependencies
Well, IPython. At present, this only works with
[ellisonbg's jsonhandlers branch][jh]. I also pull in an unofficial mirror of 
Blockly, which is hosted in SVN. Still working on making this easier.

# Installation (more like Experimentation)
Working on making this easier...

    git clone -branch jsonhandlers --single-branch \
        https://github.com/ellisonbg/ipython.git
    git clone -branch blockly --single-branch \
        https://github.com/bollwyvl/ipython.git ipython-blockly
    cd ipython-blockly
    git submodule init
    git submodule update
    python setup.py develop
    cd ../ipython
    easy_install pyzmq
    pip install tornado
    python setup.py develop
  
# Usage
From where you installed IPython above, run:

    python ipython.py notebook
    
Then, when inside a new notebook, make a cell with this content:

    %load blockly
    from IPython.display import display
    from blockly import Blockly
    display(Blockly())
    
Run (shift+enter) and you will see... nothing. Still working out the 
assets thing. Save it anyway (ctrl+s).

Kill the command line with ctrl+c, and restart it: now it should load all the 
assets, and re-running that cell should throw up a Blockly editor. As you move 
blocks around, it will fill the cell below it with the generated text... and 
slowly get longer. Not sure what that is about.

# Known Limitations
- I didn't even test it with multiple blockly cells on one page.
- The above-mentioned growing cell thing
- It doesn't know anything about the variables you already have, and always
    initializes new variables to `None`
- A bunch of assets don't load... might be a thing with the notebook server 
    though
- Probably a ton of other things

# Roadmap
- test suite
- look at multiple Blockly cells on a page
- maybe not have each cell generate another cell
- side-by-side cells?
- auto execution?
- build system

# License
Right now [Apache Public License 2.0](COPYING), as it seems more likely that 
this will bundle Blockly eventually, rather than become part of IPython (which 
is BSD). Insights welcome!

[jh]: https://github.com/ellisonbg/ipython/tree/jsonhandlers
[ip]: http://ipython.org
[blk]: http://code.google.com/p/blockly