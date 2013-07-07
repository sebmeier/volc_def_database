#!/usr/bin/env python

def lookupDOA(doi, dx='dx.doi.org'):
    """Use CrossRef to lookup bibliographic data given a DOI

    This uses the (quite new) citation formatting service.
    Useful docs:
    http://www.crossref.org/CrossTech/2011/04/content_negotiation_for_crossr.html
    http://labs.crossref.org/citation-formatting-service/
    http://www.crosscite.org/cn/
    An alternitive dx is data.datacite.org/ - should I check multiple services?
    -- no, it seesm they cross redirect, so only worry if dx.doi.org is down
    (data.doi.org being down only matters for the crosref database.
    """
    import urllib2
    import json
    # Should probabluy url encode the doi? and strip off "doi:"
    c = urllib2.Request("http://" + dx + "/" + doi)
    c.add_header("Accept", "application/vnd.citationstyles.csl+json")
    # This follows 30* redirects automatically
    r = urllib2.urlopen(c)
    #print r.info(), r.getcode()
    #print r.read()
    # Translate JSON response to a python dict.
    j = json.load(r)
    return j


if __name__=="__main__":
    """Command line for testing. e.g. run with 10.1126/science.1157784 as an argument
    of (for datacite) 10.5284/1000418"""
    import sys
    bibdict = lookupDOA(sys.argv[1])
    print bibdict
    
