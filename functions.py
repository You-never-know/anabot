#!/bin/env python2

import os, time
import libxml2

import dogtail
from dogtail.predicate import GenericPredicate

_SCREENSHOT_NUM = 0

class TimeoutError(Exception):
    pass

def waiton(node, predicates, timeout=7, make_screenshot=False):
    "wait unless item shows on the screen"
    count = 0
    if type(predicates) is not list:
        predicates = [predicates]
    while count < timeout:
        count += 1
        for predicate in predicates:
            found = node.findChild(predicate, retry=False, requireResult=False)
            if found is not None and found.showing and found.sensitive:
                if make_screenshot:
                    screenshot()
                return found
        time.sleep(1)
    screenshot()
    raise TimeoutError("No predicate matches within timeout period")

def waiton_all(node, predicates, timeout=7, make_screenshot=False):
    "wait unless items show on the screen"
    count = 0
    if type(predicates) is not list:
        predicates = [predicates]
    while count < timeout:
        count += 1
        for predicate in predicates:
            found = [ x for x in node.findChildren(predicate)
                      if x.showing and x.sensitive ]
            if len(found):
                if make_screenshot:
                    screenshot()
                return found
        time.sleep(1)
    screenshot()
    raise TimeoutError("No predicate matches within timeout period")

def getnode(parent, node_type=None, node_name=None, timeout=None):
    predicates = {}
    if node_type is not None:
        predicates['roleName'] = node_type
    if node_name is not None:
        predicates['name'] = node_name
    if timeout is not None:
        return waiton(parent, GenericPredicate(**predicates), timeout)
    return waiton(parent, GenericPredicate(**predicates))

def getnodes(parent, node_type=None, node_name=None, timeout=None):
    predicates = {}
    if node_type is not None:
        predicates['roleName'] = node_type
    if node_name is not None:
        predicates['name'] = node_name
    if timeout is not None:
        return waiton_all(parent, GenericPredicate(**predicates), timeout)
    return waiton_all(parent, GenericPredicate(**predicates))

def screenshot(wait=None):
    global _SCREENSHOT_NUM
    _SCREENSHOT_NUM += 1
    if wait is not None:
        time.sleep(wait)
    os.system("/opt/screenshot /var/run/anabot/%d-screenshot.png 1" % _SCREENSHOT_NUM)

def get_attr(element, name, default=None):
    try:
        xpath = "./@%s" % name
        return str(element.xpathEval(xpath)[0].getContent())
    except libxml2.xpathError:
        raise Exception("Incorrect xpath expression: '%s'" % xpath)
    except IndexError:
        if default is None:
            raise KeyError("No attribute named '%s'" % name)
        return default
