#-*- coding: utf-8 -*-
import os
import logging
import pkg_resources

import nosexunit.const as nconst
import nosexunit.excepts as nexcepts

# Get a logger
logger =  logging.getLogger('%s.%s' % (nconst.LOGGER, __name__))

class Singleton(object):
    '''
    Singleton implementation
    On: http://www.python.org/download/releases/2.2.3/descrintro/
    '''
    
    def __new__(cls, *args, **kwds):
        '''
        Return the instance of the singleton
        Call init method if not yet initialized
        '''
        it = cls.__dict__.get('__it__')
        if it is not None:
            return it
        it = object.__new__(cls)
        it.init(cls, *args, **kwds)
        cls.__it__ = it
        return it
    
    def init(self, *args, **kwds):
        '''Initialization on first call'''
        pass
    
    def reset(cls):
        '''
        Reset the instance of the singleton
        Call close on the instance
        '''
        if cls.__dict__.get('__it__') is not None:
            it = cls.__it__
            cls.__it__ = None
            it.close()
    reset = staticmethod(reset)
    
    def close(self):
        '''Close the instance of the singleton'''
        pass

def packages(root, search=False, exclude=nconst.SEARCH_EXCLUDE):
    '''Return the package list contained by the folder'''
    # Store the list of packages
    pkgs = {}
    # Check that source folder is not in a package
    if os.path.exists(os.path.join(root, nconst.INIT)):
        # The root package can't be a part of a package
        raise nexcepts.ToolError('following folder can not contain %s file: %s' % (nconst.INIT, root))
    # Go threw the folders
    for folder, folders, files in os.walk(root):
        # Filter on pattern
        for bn in exclude:
            # Check if pattern in and drop it
            if bn in folders: folders.remove(bn)
        # Folders to pop
        pops = []
        # Go threw the folders
        for fld in [ os.path.join(folder, fld) for fld in folders ]:
            # Check if folder has an __init__
            if os.path.exists(os.path.join(fld, nconst.INIT)):
                # This is a package, get the full description
                entry = package(fld)
                # Check if already exists
                if pkgs.has_key(entry): logger.warn('package %s already exists in following folder tree: %s' % (entry, root))
                # Else add it
                else: pkgs[entry] = fld
            # Add the folders to pop
            else: pops.append(os.path.basename(fld))
        # Check if pop
        if not search:
            # Go threw the folder to pop
            for pop in pops: folders.remove(pop)
        # Go threw the files
        for path in [ os.path.join(folder, fn) for fn in files ]:
            # Check if this is a module
            if split(path)[1] == 'py' and os.path.basename(path) != nconst.INIT:
                # Get the full description
                entry = package(path)
                # Check if already exists
                if pkgs.has_key(entry): logger.warn('module %s already exists in following folder tree: %s' % (entry, root))
                # Else add it
                else: pkgs[entry] = path
    # Return the packages
    return pkgs

def package(source):
    '''Get the package that contains the source'''
    # Check if source exists
    if not os.path.exists(source): raise nexcepts.ToolError("source doesn't exists: %s" % source)
    # Check if folder contains an __init__
    folder = os.path.dirname(source)
    # Get the base
    base = split(os.path.basename(source))[0]
    # Check if exists
    if os.path.exists(os.path.join(folder, nconst.INIT)):
        # Source is contained in a package
        return '%s.%s' % (package(folder), base)
    # Source not contained in a folder
    else: return base

def split(fn):
    '''Return the extension of the provided base file'''
    # Get the parts of the file
    sf = fn.split('.')
    # Get the length 
    l = len(sf)
    # Check if not extension
    if l == 1: return (fn, None)
    # Else, there is an extension
    else:
        # Get the last part as extension
        ext = sf[-1]
        # Join to get base
        bn = '.'.join(sf[0:l-1])
    # Return the 2-UPLE: base, extension
    return (bn, ext)

def save(content, path, binary=False):
    '''Save the provided content in a file'''
    # Get the mode, here binary
    if binary: mode = 'wb'
    # Here, textual
    else: mode = 'w'
    # Open the file
    fd = open(path, mode)
    # Set the content
    fd.write(content)
    # Close the file
    fd.close()

def load(path, binary=False):
    '''Return the content of the file'''
    # Get the mode, here binary
    if binary: mode = 'rb'
    # Here, textual
    else: mode = 'r'
    # Open the file
    fd = open(path, mode)
    # Get the content
    content = fd.read()
    # Close the file
    fd.close()
    # Return the content
    return content

def create(folder):
    '''Create a folder'''
    # If not exists, create the folders
    if not os.path.exists(folder): os.makedirs(folder)
    # If exists and is a file, raise
    elif os.path.isfile(folder): raise nexcepts.ToolError('following path exists but is not a folder: %s' %folder)

def clean(folder, prefix=None, ext=None):
    '''Clean all file with the given extension and/or prefix in specified folder'''
    # Check if folder exists
    if not os.path.isdir(folder): raise nexcepts.ToolError("folder doesn't exist: %s" % folder)
    # Go threw the folder
    for bn in os.listdir(folder):
        # Get the full path
        full = os.path.join(folder, bn)
        # Check if file
        if os.path.isfile(full) and (not prefix or (prefix and bn.startswith(prefix))) and (not ext or (ext and split(bn)[1] == ext)):
            # Clean the file
            os.remove(full)

def get_test_id(test):
    '''Get the ID of the provided test'''
    # Try to call the id
    try: return test.id()
    # Failed to get it ! Get an unique test entry
    except:
        # Get the default base
        entry = 'nose.nose'
        # Check if UUID is available
        try:
            # Get UUID
            import uuid
            # Get the value
            return '%s.%s' % (entry, uuid.uuid1())
        # Else use id(...)
        except: return '%s.%s' % (entry, id(test))

def identical(file1, file2):
    '''Return True if it is the same file'''
    # Check if on UNIX
    if on_posix(): return os.path.samefile(file1, file2)
    # On Win32
    else: return os.path.normpath(file1) == os.path.normpath(file2)

def on_posix():
    '''Return True if run on POSIX platform'''
    # Check OS name
    return os.name == 'posix'

def extract(package, entry, folder, bn=None):
    '''Extract file with provided entry from the provided package'''
    # Get the content of the entry
    content = pkg_resources.resource_string(package, entry)
    # Check if base is specified: here yes
    if bn: path = os.path.join(folder, bn)
    # Here no
    else: path = os.path.join(folder, entry)
    # Save content
    save(content, path, binary=False)

def kiding(package, entry, folder, bn=None, output='html', **kwarg):
    '''Extract file with provided entry from the provided package and process the template'''
    # Get the kid package
    import kid
    # Get the content of the entry
    content = pkg_resources.resource_string(package, entry)
    # Check if base is specified: here yes
    if bn: path = os.path.join(folder, bn)
    # Here no
    else: path = os.path.join(folder, entry)
    # Open the file
    fd = open(path, 'w')
    # Create the template
    kid.Template(content, **kwarg).write(file=fd, output=output)
    # Close the file descriptor
    fd.close()

def extract_js_css(target):
    '''Extract the CSS and the Java Script in the target folder'''
    # Get package
    import pygments.formatters
    # Extract the Java Script
    extract(__name__, 'nosexunit.js', target)
    # Extract the CSS
    extract(__name__, 'nosexunit.css', target)
    # Get the highlight CSS
    save(pygments.formatters.HtmlFormatter().get_style_defs('.highlight'), os.path.join(target, 'highlight.css'), binary=False)

def highlight(content):
    '''Highlight source code'''
    # Get packages
    import pygments
    import pygments.lexers
    import pygments.formatters
    # Get a LEXER
    lexer = pygments.lexers.PythonLexer()
    # Get a formatter class
    class HPyF(pygments.formatters.HtmlFormatter):
        '''Class override to avoid &gt; &lt; changing in report'''
        def wrap(self, source, outfile): return source
    # Get a formatter
    formatter = HPyF()
    # Highlight
    return pygments.highlight(content, lexer, formatter).splitlines()
