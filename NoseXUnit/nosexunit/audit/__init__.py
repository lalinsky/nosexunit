#-*- coding: utf-8 -*-
import os
import new
import logging
import unittest
import datetime
import traceback
import ConfigParser

import nosexunit.const as nconst
import nosexunit.tools as ntools
import nosexunit.excepts as nexcepts

# Get a logger
logger =  logging.getLogger('%s.%s' % (nconst.LOGGER, __name__))

try:
    import pylint.lint
    import pylint.config
    import pylint.reporters
except: pass

class AuditTestCase(unittest.TestCase):
    '''Super class for audit test case'''
    pass

class Entry(object):
    '''A PyLint Entry'''
    
    def __init__(self, eid, line, output):
        '''initialize the entry'''
        # Store the ID
        self.eid = eid
        # Store the line
        self.line = line
        # Store the content
        self.output = output
        
    def __str__(self):
        '''String representation'''
        return '%s: %d: %s' % (self.eid, self.line, self.output)

class Source(dict):
    '''Represent a source file'''

    def __init__(self, path, desc):
        '''Initialize the file system object'''
        # Call super
        dict.__init__(self)
        # Store the description
        self.i_desc = desc
        # Store the parent package
        self.i_father = None
        # Store the path
        self.i_path = path
        # Store the PyLint entries
        self.i_entries = []
        
    def desc(self):
        '''Get the description of the package'''
        return self.i_desc
    
    def path(self):
        '''Get the path of the file'''
        return self.i_path
    
    def father(self):
        '''Get the parent package'''
        return self.i_father

    def full(self):
        '''Full package description'''
        # Check if there is a parent package
        if self.i_father is None: return self.i_desc
        # There is actually a parent package
        else: return '%s.%s' % (self.father().full(), self.i_desc)

    def set(self, source):
        '''Append a FS to this object'''
        # Add to the list
        self[source.desc()] = source
        # Add father to children
        source.i_father = self
    
    def add(self, entry):
        '''Add an entry to the source'''
        self.i_entries.append(entry)
    
    def entries(self):
        '''Get all the PyLint entries'''
        return self.i_entries
    
    def count(self, filter):
        '''Count the pyLint entries for the provided filter'''
        return len(self.search(filter))
    
    def search(self, filter):
        '''Get all the entries corresponding to the filter'''
        try: return [ entry for entry in self.entries() if entry.line == int(filter) ]
        except: return [ entry for entry in self.entries() if entry.eid.startswith(filter) ]
    
    def __str__(self):
        '''String description'''
        if self.entries() == []: return '%s (%s)' % (self.full(), self.path())
        else: return '%s (%s)\n    %s' % (self.full(), self.path(), '\n    '.join([ str(entry) for entry in self.entries() ]))

class Sources(dict):
    '''Store all sources'''
    
    def get(self, path, desc):
        '''Get a source given its path and description'''
        # Get the right description by ignoring __init__
        desc = desc.replace('.__init__', '') 
        # Get package deep
        count = desc.count('.')
        # Start from head package
        current = self
        # Store current deep
        pos = 0
        # Go deeper and deeper in package tree
        for part in desc.split('.'):
            # Get the path
            c_path = path
            # Step out until package is reached
            for i in range(count-pos): c_path = os.path.dirname(c_path)
            # Check if source already defined
            if not current.has_key(part):
                # Source not already defined, create it. Here this is a module.
                if count-pos == 0: current.set(Source(c_path, part))
                # Here this is a package
                else: current.set(Source(os.path.join(c_path, '__init__.py'), part))
            # Set the current source
            current = current[part]
            # Go deeper
            pos += 1
        # Check the path
        if not ntools.identical(current.path(), path):
            # Invalid path
            raise nexcepts.AuditError('two path for %s, only one expected:\n- %s\n- %s' % (current.full(), current.path(), path))
        # Return the source
        return current

    def set(self, source):
        '''Set head source'''
        self[source.desc()] = source
            
    def listing(self):
        '''Get all the sources'''
        # Recursive function to search all sources
        def _internal(source, slist):
            # Add the current one
            slist.append(source)
            # Go threw its sub packages
            for child in source.keys():
                # Recursive process of each child
                _internal(source[child], slist)
        # Result list
        slist = []
        # Start listing
        for source in self.keys(): _internal(self[source], slist)
        # Return the result list
        return slist

    def count(self, filter):
        '''Count the PyLint entries for the provided filter in all sources'''
        # Get a counter
        counter = 0
        # Go threw the sources
        for source in self.listing():
            # Get answer for the source and add to counter
            counter += source.count(filter)
        # Return final number
        return counter

class AuditReporter(object):
    '''Reporter for NoseXUnit reports'''

    def __init__(self):
        # Store the sources packages
        self.sources = Sources()
        # Useless, only for PyLint
        self.extension = 'audit'

    def add_message(self, msg_id, location, msg):
        '''Add an id'''
        # Get the data from the location
        path, desc, useless, line = location
        # Get the source object
        source = self.sources.get(path, desc)
        # Create the entry for the data
        entry = Entry(msg_id, line, msg)
        # Add it to the source object
        source.add(entry)
    
    def display_results(self, layout):
        '''Display the results'''
        pass
    
    def set_output(self, fd):
        '''Set the output'''
        pass

class AuditWrapper(object):
    '''
    Reporter for NoseXUnit
    Wrap the selected PyLint reporter 
    '''
    
    def __init__(self, output, target):
        '''Initialize the reporter'''
        # Set the output
        self.output = output
        # Get the reporter
        if self.output not in outputs():
            # Unable to get the asked reporter
            raise nexcepts.AuditError('unable to get reporter for %s' % self.output)
        # Set the target folder
        self.target = target
        # Get the test cases
        self.cases = []
        # Store the package
        self.packages = []
        # Store the test id
        self.count = None
        # Get the reporter
        self.reporter = None

    def default(self):
        '''Return True if AuditReporter is used'''
        return isinstance(self.reporter, AuditReporter)

    def next(self, package):
        '''Enable wrapper for next package'''
        # Set the package
        self.packages.append(package)
        # Set the new test case
        self.cases.append(new.classobj('TestAudit%s' % package.capitalize(), (AuditTestCase, ), {}))
        # Set the test counter
        self.count = 1
        # Create the reporter
        if not self.default(): self.reporter = create_reporter(self.output)

    def add_message(self, msg_id, location, msg):
        '''
        Add a message of a given type:
        - Propagate to reporter
        - Add test if errors
        '''
        # Call reporter
        self.reporter.add_message(msg_id, location, msg)
        # Check if error and add a test
        if msg_id[0] in ['E', 'F', ]:
            # Create the test
            def test(cls):
                # Get the output
                output = """%s
location   : %s
line:      : %d
package    : %s
function   : %s
description: %s
""" % (msg_id, location[0], location[3], location[1], location[2], msg)
                # Actually fail
                cls.fail(output)
            # Set to the class
            setattr(self.cases[-1], 'test_%d' % self.count, test)
            # Add to counter
            self.count += 1

    def __getattr__(self, name):
        '''Delegate for getters'''
        return getattr(self.reporter, name)
    
    def set_output(self, fd=None):
        '''Override the method to store the files in the target folder'''
        # Check if output specified
        if fd is None: raise nexcepts.AuditError('file expected for output')
        # Check that output is a real file
        if not fd.fileno() > 2: raise nexcepts.AuditError('real file expected for output: got %s' % fd.name)
        # Get the base
        bn = fd.name
        # Close the file
        fd.close()
        # Drop it
        os.remove(bn)
        # Check if default reporter
        if not self.default():
            # Get the folder
            folder = os.path.join(self.target, self.packages[-1])
            # Check if target folder exists
            ntools.create(folder)
            # Get the file
            self.reporter.set_output(open(os.path.join(folder, bn), 'w'))

    def display_results(self, layout):
        '''Display results'''
        # Call super
        self.reporter.display_results(layout)

def audit(packages, output, target, config=None):
    '''Start PyLint'''
    # Check PyLint configuration file
    check_pylintrc()
    # Get a wrapper
    wrapper = AuditWrapper(output, target)
    # Go threw the packages
    for package in packages:
        # Set the next package
        wrapper.next(package)
        # Get the arguments
        argv = ['--include-ids=yes', # Set id
                '--files-output=yes', # Set file output
                '--reports=yes',
                '--comment=yes', ] # Do not generate report
        # Check if configuration
        if config is not None: argv.append('--rcfile=%s' % config)
        # Add the package
        argv.append(package)
        # Start PyLint
        pylint.lint.Run(argv, wrapper)
    # Create report
    report(target, wrapper.reporter.sources)
    # Return cases
    return wrapper.cases

def report(target, sources):
    '''Create report'''
    # Extract the Java Script and the CSS
    ntools.extract_js_css(target)
    # Get the date
    date = datetime.datetime.now()
    # Process the index
    ntools.kiding(__name__, 'index.html', target)
    # Process the listing
    ntools.kiding(__name__, 'listing.html', target, sources=sources, date=date)
    # Process the abstract
    ntools.kiding(__name__, 'abstract.html', target, sources=sources, date=date)
    # Go threw the sources
    for entity in sources.listing():
        # Try to process the package
        try:
            # Set the details of the errors
            ntools.kiding(__name__, 'detail.html', target, bn='%s-detail.html' % entity.full(), entity=entity, date=date)
            # Get the highlighted lines
            lines = ntools.highlight(ntools.load(entity.path()))
            # Process the code
            try: ntools.kiding(__name__, 'code.html', target, bn='%s-code.html' % entity.full(), entity=entity, lines=lines, date=date)
            # Unable to create source
            except:
                # Log the error
                logger.error(traceback.format_exc())
                # Create the error page
                ntools.kiding(__name__, 'error.html', target, bn='%s-code.html' % entity.full(), entity=entity, error='Failed to highlight source code', date=date)
        # Unable to process the package
        except: logger.error(traceback.format_exc())

def check_pylintrc(path=None):
    """
    Check that the PyLint configuration file
    doesn't contain parameters that override
    the NoseXUnit configuration
    """
    # Get the forbidden options
    forbid = {'REPORTS': ['output-format',
                          'include-ids',
                          'files-output',
                          'reports', ],
              'MASTER': ['rcfile', ], }
    # Check if path is specified
    if not path: path = pylint.config.PYLINTRC
    # Check if path is is defined
    if path:
        # Get the absolute path
        path = os.path.abspath(path)
        # Check if the file exists
        if os.path.isfile(path):
            # Get a parser
            parser = ConfigParser.ConfigParser()
            # Parse the file
            parser.read(path)
            # Go threw the sections
            for section in forbid.keys():
                # Check if has the section
                if parser.has_section(section):
                    # Go threw the options
                    for option in forbid[section]:
                        # Check if has the option
                        if parser.has_option(section, option):
                            # Forbidden option
                            raise nexcepts.AuditError("%s of [%s] can't be on following PyLint's configuration file: %s" % (option, section, path))

def outputs():
    '''Get the available output for PyLint'''
    # Add the NoseXUnit output
    out = [nconst.AUDIT_DEFAULT_REPORTER, ]
    # Add default outputs
    out.extend(pylint.lint.REPORTER_OPT_MAP.keys())
    # Return the available outputs
    return out

def create_reporter(output):
    '''Create a reporter for the provided output'''
    # Check if default reporter selected
    if output == nconst.AUDIT_DEFAULT_REPORTER: return AuditReporter()
    # Get PyLint reporter
    else: return pylint.lint.REPORTER_OPT_MAP[output]()     

def available():
    '''Check if PyLint is available'''
    # Try to get PyLint
    try:
        # All needed modules
        import kid
        import pygments
        import pylint.lint
        import pylint.config
        import pygments.lexers
        import pylint.reporters
        import pygments.formatters
    # Unable to get it
    except: return False
    # OK, it's available
    return True
