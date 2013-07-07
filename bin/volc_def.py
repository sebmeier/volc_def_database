#!/usr/bin/env python
""" volc_def: a database of volcano deformation

This module contains the code that can be used to
process files containing information about volcano
deformation. These can be used, for example, to 
build a website of observations.

When used as a module a single class is exposed
which allows objects describing volcano 
defomation to be created and manipulated

When used as a script, the class is populated
by reading an file describing a single volcano
and an operation (validation, converting to
XML etc.) on the resulting data is undertaken.
"""

import re

class Volcano:
    """ A container and processor for volcano defomation """

    def __init__(self, filename=None, debug=False):
        # This is called when a new instance of
        # Volcano is created. First set all the 
        # possible data fields to 'null' values
        # so we can tell if data is missing.
        self.id = None
        self.name = None
        self.latitude = float('NaN')
        self.longitude = float('NaN')
        self.rocktype = None
        self.studies = []
        self.events = []
        self.references = []
        self.description = ""
        # NOTE: put new data holders here
        #       choosing a sensible null value

        # If we have a filename we can use it 
        # to populate the data now.
        if filename is not None:
            self._parse_file(filename, debug=debug)

    def _parse_file(self, filename, debug=False):
        # This is a simple state machine based
        # parser to read our data file format.
        # There are definatly better ways to do this
        # but this is simple!

        section_name = None # Are we in a section, which one?
        keyword = None # What is this line's keyword?
        multiline = False
        multiline_keyword = None

        f = open(filename, 'r')
        for line in f:

            new_section = re.match(r"\s*\[\s*Start\s+(\w+)\s*\]",line)
            if new_section:
                if section_name is None:
                    # New section in root of file... OK
                    section_name = new_section.group(1).strip().upper()
                    # Create new empty object for this section
                    if (section_name=="STUDY"):
                        self.studies.append(Study())
                    elif(section_name=="EVENT"):
                        self.events.append(Event()) 
                    continue 
                else:
                    raise Exception("Sections cannot be nested")

            end_section = re.match(r"\s*\[\s*End\s+(\w+)\s*\]",line)
            if end_section:
                if (end_section.group(1).strip().upper()==section_name):
                    # Ended this section OK
                    section_name = None
                    continue
                else:
                    raise Exception("End section did not match start")

            key_val = re.match(r"\s*(\w+)\s*:(.+?)$", line)
            if key_val:
                keyword = key_val.group(1).strip().upper()
                value = key_val.group(2).strip()
                if (value==">>"):
                    if multiline:
                        raise Exception("Cannot nest multiline blocks")
                    else:
                        multiline = True
                        multiline_keyword = keyword
                        continue
                elif (value=="<<"):
                    if not multiline:
                        raise Exception("Not in a multiline block")
                    elif (multiline_keyword != keyword):
                        raise Exception("End multiline mismatch")
                    else:
                        multiline = False
                        multiline_keyword = None
                        continue
                else:
                    if section_name is None:
                        # process this keyword value pair
                        # in file root.
                        if keyword=="ID":
                            self.id = value
                            continue
                        elif keyword=="NAME":
                            self.name = value
                            continue
                        elif keyword=="LATITUDE":
                            self.latitude = float(value)
                            continue
                        elif keyword=="LONGITUDE":
                            self.longitude = float(value)
                            continue
                        elif keyword=="ROCKTYPE":
                            self.rocktype = value
                            continue
                        elif keyword=="DESCRIPTION":
                            self.description = self.description+value
                            continue
                        else:
                            # Don't recognise this - skip
                            continue
                    elif section_name == "STUDY":
                        if keyword=="TYPE":
                            if self.studies[-1].type is None:
                                self.studies[-1].type = value
                            else:
                                raise Exception("Double study type")
                        elif keyword=="DESCRIPTION":
                            self.studies[-1].description = self.description+value
                            continue
                 
                    elif section_name == "EVENT":
                        if keyword=="TYPE":
                            if self.event[-1].type is None:
                                self.event[-1].type = vaue
                            else:
                                raise Exception("Double study type")
                        elif keyword=="DESCRIPTION":
                            self.event[-1].description = self.description+value
                            continue
                 
                    else:
                        raise Exception("In unrecognised section")
            else:
                # Error unless we are in a multilne block
                if multiline:
                    if section_name is None:
                        if multiline_keyword == "DESCRIPTION":
                            self.description = self.description+line.strip()+" "
                    elif section_name == "STUDY":
                        if multiline_keyword == "DESCRIPTION":
                            self.studies[-1].description = self.description+line.strip()+" "
                    elif section_name == "EVENT":
                        if multiline_keyword == "DESCRIPTION":
                            self.event[-1].description = self.description+line.strip()+" "

                # Should we error out here? 

    def dump(self):
        print "ID: " + self.id
        print "Name: " + self.name
        print "Latitude: " + str(self.latitude)
        print "Longitude: " + str(self.longitude)
        print "Rocktype: " + self.rocktype
        if self.description != "":
            print "Description: " + self.description

        for event in self.events:
            print "[Start event]"
            print "Type: " + event.type
            if event.description != "":
                print "Description: " + event.description
            print "[End event]"

        for study in self.studies:
            print "[Start study]"
            print "Type: " + study.type
            if study.description != "":
                print "Description: " + study.description
            print "[End study]"

class Event:
    "Something that happened to a volcano"

    def __init__(self):
        self.type = None
        self.description = ""
        self.reference = None
        self.startdate = None
        self.enddate = None

class Study:
    "An observation of volcanic deformation"

    def __init__(self):
        self.type = None
        self.description = ""
        self.reference = None
        self.startdate = None
        self.enddate = None
            
if __name__=="__main__":
    import sys
    mode = sys.argv[1]
    for file in sys.argv[2:]:
        volcano = Volcano(filename=file)
        if mode == "dump":
            volcano.dump()
              

    
