#!/bin/env python2

import time
import libxml2

import dogtail
import dogtail.utils
from dogtail.predicate import GenericPredicate

from .errors import TimeoutError

_SCREENSHOT_NUM = 0

def inrange(what, border1, border2):
    if border1 == border2:
        return what == border1
    if border1 < border2:
        return border1 <= what and what < border2
    return border2 <= what and what < border1

def visibility(node, value):
    return (value is None) or (bool(value) == node.showing)

def sensitivity(node, value):
    return (value is None) or (bool(value) == node.sensitive)

def waiton(node, predicates, timeout=7, make_screenshot=False, visible=True, sensitive=True, recursive=True):
    "wait unless item shows on the screen"
    count = 0
    if type(predicates) is not list:
        predicates = [predicates]
    while count < timeout:
        count += 1
        for predicate in predicates:
            found = node.findChild(predicate, retry=False, requireResult=False, recursive=recursive)
            if found is not None and visibility(found, visible) and sensitivity(found, sensitive):
                if make_screenshot:
                    screenshot()
                return found
        time.sleep(1)
    screenshot()
    raise TimeoutError("No predicate matches within timeout period")

def waiton_all(node, predicates, timeout=7, make_screenshot=False, visible=True, sensitive=True, recursive=True):
    "wait unless items show on the screen"
    count = 0
    if type(predicates) is not list:
        predicates = [predicates]
    while count < timeout:
        count += 1
        for predicate in predicates:
            found = [x for x in node.findChildren(predicate,
                                                  recursive=recursive) if
                     visibility(x, visible) and sensitivity(x, sensitive)]
            if len(found):
                if make_screenshot:
                    screenshot()
                return found
        time.sleep(1)
    screenshot()
    raise TimeoutError("No predicate matches within timeout period")

def getnode(parent, node_type=None, node_name=None, timeout=None,
            predicates=None, visible=True, sensitive=True, recursive=True):
    if predicates is None:
        predicates = {}
    if node_type is not None:
        predicates['roleName'] = node_type
    if node_name is not None:
        predicates['name'] = node_name
    if timeout is not None:
        return waiton(parent, GenericPredicate(**predicates), timeout,
                      visible=visible, sensitive=sensitive, recursive=recursive)
    return waiton(parent, GenericPredicate(**predicates), visible=visible,
                  sensitive=sensitive, recursive=recursive)

def getnodes(parent, node_type=None, node_name=None, timeout=None,
             predicates=None, visible=True, sensitive=True, recursive=True):
    if predicates is None:
        predicates = {}
    if node_type is not None:
        predicates['roleName'] = node_type
    if node_name is not None:
        predicates['name'] = node_name
    if timeout is not None:
        return waiton_all(parent, GenericPredicate(**predicates), timeout,
                          visible=visible, sensitive=sensitive,
                          recursive=recursive)
    return waiton_all(parent, GenericPredicate(**predicates), visible=visible,
                      sensitive=sensitive, recursive=recursive)

def getparent(child, node_type=None, node_name=None, predicates=None):
    if predicates is None:
        predicates = {}
    if node_type is not None:
        predicates['roleName'] = node_type
    if node_name is not None:
        predicates['name'] = node_name
    return child.findAncestor(GenericPredicate(**predicates))

def getparents(child, node_type=None, node_name=None, predicates=None):
    parents = []
    while True:
        parent = getparent(child, node_type, node_name, predicates)
        if parent is None:
            return parents
        parents.append(parent)
        child = parent

def getsibling(node, vector, node_type=None, node_name=None, visible=True,
               sensitive=True):
    """
    Get n'th (vector is negative or positive number specifying direction and
    distance of search) sibling node that passes given criterie (node_type,
    node_name, visible and sensitive).
    """
    parent = getparent(node)
    index = node.indexInParent
    nodes = getnodes(parent, node_type, node_name, visible=visible,
                     sensitive=sensitive, recursive=False)
    if len(nodes) == 0:
        return
    if vector < 0:
        nodes = sorted(nodes, reverse=True)
        index *= -1
    located = False
    lastId = nodes[0].indexInParent
    for sibling in nodes:
        curId = sibling.indexInParent
        if located:
            index -= 1
        elif inrange(index, lastId, curId):
            located = True
            index -= 1
        else:
            lastId = curId
        if index == 0:
            return sibling

def getselected(parent):
    return [child for child in getnodes(parent) if child.selected]

def screenshot(wait=None):
    # DISABLED ATM
    return
    global _SCREENSHOT_NUM
    _SCREENSHOT_NUM += 1
    if wait is not None:
        time.sleep(wait)
    dogtail.utils.screenshot('/var/run/anabot/%02d-screenshot.png' %
                             (_SCREENSHOT_NUM), timeStamp=False)

def get_attr(element, name, default=None):
    try:
        xpath = "./@%s" % name
        return str(element.xpathEval(xpath)[0].getContent())
    except libxml2.xpathError:
        raise Exception("Incorrect xpath expression: '%s'" % xpath)
    except IndexError:
        return default
