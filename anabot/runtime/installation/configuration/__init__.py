# -*- coding: utf-8 -*-
import time
import logging
logger = logging.getLogger('anabot')
import teres
reporter = teres.Reporter.get_reporter()

from anabot.runtime.decorators import handle_action, handle_check
from anabot.runtime.default import default_handler
from anabot.runtime.functions import get_attr, getnode, TimeoutError, getparent, getsibling, log_screenshot
from anabot.runtime.translate import tr
from anabot.runtime.hooks import run_posthooks

_local_path = '/installation/configuration'
handle_act = lambda x: handle_action(_local_path + x)
handle_chck = lambda x: handle_check(_local_path + x)

import root_password, create_user

@handle_act('')
def base_handler(element, app_node, local_node):
    default_handler(element, app_node, local_node)

@handle_act('wait_until_complete')
def wait_until_complete_handler(element, app_node, local_node):
    reporter.log_debug("Looking for installation progress bar.")
    try:
        progress = getnode(app_node, "progress bar")
    except:
        return (False, "Couldn't find progress bar")
    reporter.log_debug("WAITING FOR REBOOT")
    while progress.value < 1:
        time.sleep(1)
    return True

@handle_act('/reboot')
def reboot_handler(element, app_node, local_node):
    try:
        reboot_button = getnode(app_node, "push button",
                                tr("_Reboot", context="GUI|Progress"),
                                timeout=15)
    except TimeoutError:
        return (False, "Couldn't find clickable Reboot button.")

    run_posthooks()
    reporter.test_end()
    reboot_button.click()

