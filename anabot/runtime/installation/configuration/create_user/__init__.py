# -*- coding: utf-8 -*-
import logging
logger = logging.getLogger('anabot')

from anabot.runtime.decorators import handle_action, handle_check
from anabot.runtime.default import default_handler
from anabot.runtime.functions import get_attr, getnode, TimeoutError, getparent, getsibling
from anabot.runtime.translate import tr
from anabot.runtime.hooks import run_posthooks

# import advanced dialog
import advanced

_local_path = '/installation/configuration/create_user'
handle_act = lambda x: handle_action(_local_path + x)
handle_chck = lambda x: handle_check(_local_path + x)

@handle_act('')
def user_spoke_handler(element, app_node, local_node):
    user_spoke = getnode(app_node, "spoke selector",
                                  tr("_USER CREATION", context="GUI|Spoke"))
    user_spoke.click()
    try:
        user_panel = getnode(app_node, "panel", tr("CREATE USER"))
    except TimeoutError:
        return (False, "User creation spoke not found")
    default_handler(element, app_node, user_panel)

@handle_act('/full_name')
def user_full_name_handler(element, app_node, local_node):
    entry = getnode(local_node, 'text', tr('Full Name'))
    value = get_attr(element, 'value')
    entry.typeText(value)

@handle_chck('/full_name')
def user_full_name_check(element, app_node, local_node):
    entry = getnode(local_node, 'text', tr('Full Name'))
    value = get_attr(element, 'value')
    if (value is None):
        value = ''
    if entry.text == value:
        return True
    return (False, "users full name ('%s') differs from expected one ('%s')" % (entry.text, value))

@handle_act('/username')
def user_username_handler(element, app_node, local_node):
    entry = getnode(local_node, 'text', tr('User name'))
    value = get_attr(element, 'value')
    if not (value is None):
        entry.typeText(value)

@handle_chck('/username')
def user_username_check(element, app_node, local_node):
    entry = getnode(local_node, 'text', tr('User name'))
    value = get_attr(element, 'value')
    if (value is None):
        value = ''
    if entry.text == value:
        return True
    return (False, "username ('%s') differs from expected one ('%s')" % (entry.text, value))

@handle_act('/is_admin')
def user_is_admin_handler(element, app_node, local_node):
    checkbox = getnode(local_node, "check box", tr('Make this user administrator', context="GUI|User")) # translation bug: "Udělat tohot uživatele správcem"
    value = get_attr(element, 'checked')
    if value == 'yes':
        value = True
    else:
        value = False
    if checkbox.checked != value:
        checkbox.click()

@handle_chck('/is_admin')
def user_is_admin_check(element, app_node, local_node):
    checkbox = getnode(local_node, "check box", tr('Make this user administrator', context="GUI|User"))
    value = get_attr(element, 'checked')
    if value == 'yes':
        value = True
    else:
        value = False
    if checkbox.checked == value:
        return True
    return False
        

@handle_act('/require_password')
def user_require_passwd_handler(element, app_node, local_node):
    checkbox = getnode(local_node, "check box", tr('Require a password to use this account', context="GUI|User"))
    value = get_attr(element, 'checked')
    if value == 'yes':
        value = True
    else:
        value = False
    if checkbox.checked != value:
        checkbox.click()

@handle_chck('/require_password')
def user_require_passwd_check(element, app_node, local_node):
    checkbox = getnode(local_node, "check box", tr('Require a password to use this account', context="GUI|User"))
    value = get_attr(element, 'checked')
    if value == 'yes':
        value = True
    else:
        value = False
    if checkbox.checked == value:
        return True
    return False

@handle_act('/password')
def user_password_handler(element, app_node, local_node):
    entry = getnode(local_node, "password text", tr('_Password', context="GUI|User"))
    password = get_attr(element, 'value')
    entry.typeText(password)
    return True #cannot verify password via ATK

@handle_act('/confirm_password')
def user_confirm_password_handler(element, app_node, local_node):
    print "searching for %s" % tr('Confirm password')
    entry = getnode(local_node, "password text", tr('Confirm Password')) # translation error  label "_Povrďte heslo"
    password = get_attr(element, 'value')
    entry.typeText(password)
    return True #cannot verify password via ATK

@handle_act('/done')
def user_done_handler(element, app_node, local_node):
    try:
        done_btn = getnode(local_node, "push button",
                                     tr("_Done", False))
    except TimeoutError:
        return (False, "Done button not found or not clickable")
    done_btn.click()
    try:
        user_panel = getnode(app_node, "panel", tr("CREATE USER"))
        return (False, "User spoke is still present")
    except TimeoutError:
        return True
    return False
