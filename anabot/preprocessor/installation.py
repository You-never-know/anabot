import logging

logger = logging.getLogger('anabot.preprocessor')

import re

from .decorators import replace
from .functions import load_snippet, has_property, pop_property, copy_content
from .defaults import delete_element
from anabot.variables import get_variable
from anabot.conditions import has_feature_hub_config
from anabot.conditions import is_anaconda_version_ge, is_distro, is_distro_version_ge

def has_new_root_psswd_spoke():
    return is_anaconda_version_ge('35.22.1')

@replace("/installation")
def replace_installation(element):
    if len(element.xpathEval('./welcome')) == 0:
        new_welcome = element.addChild(load_snippet("/installation/welcome", element, tag_name='_default_for'))
        first_el = element.xpathEval("./*")[0]
        if first_el != new_welcome:
            first_el.addPrevSibling(new_welcome)
        replace_welcome(new_welcome, element)
    if len(element.xpathEval('./hub')) == 0:
        new_hub = element.addChild(load_snippet("/installation/hub", element, tag_name='_default_for'))
        welcome_el = element.xpathEval("./*")[0]
        welcome_el.addNextSibling(new_hub)
        replace_hub(new_hub, element)
    if len(element.xpathEval('./configuration')) == 0:
        new_conf = element.addChild(load_snippet("/installation/configuration", element, tag_name='_default_for'))
        replace_configuration(new_conf, element)

@replace("/installation/welcome")
def replace_welcome(element, default_for=None):
    if default_for is None:
        default_for = element
    lang_re = re.compile(r"(?P<lang>[^(]*) (?:\((?P<loc>[^)]*)\))?")
    lang_prop = pop_property(element, "language")
    if lang_prop is not None:
        new = load_snippet("/installation/welcome@language", element, True)
        copy_content(new, element, prepend=True)
        match = lang_re.match(lang_prop.content)
        lang = match.group("lang")
        element.xpathEval("./language")[0].setProp("value", lang)
        loc = match.group("loc")
        element.xpathEval("./locality")[0].setProp("value", loc)
    if len(element.xpathEval('./continue')) == 0:
        new_continue = load_snippet("/installation/welcome/continue", default_for, tag_name="_default_for")
        element.addChild(new_continue)
        try:
            beta_dialog = element.xpathEval('./beta_dialog')[0]
            beta_dialog.addPrevSibling(new_continue)
        except IndexError:
            pass
    if len(element.xpathEval('./beta_dialog')) == 0:
        new_beta_dialog = element.addChild(load_snippet("/installation/welcome/beta_dialog", default_for, tag_name="_default_for"))
        replace_beta_dialog(new_beta_dialog, default_for)

@replace("/installation/welcome/beta_dialog")
def replace_beta_dialog(element, default_for=None):
    tag_name="_default_for"
    if default_for is None:
        default_for = element
        tag_name="_replacing"
    new = load_snippet("/installation/welcome/beta_dialog", default_for, tag_name=tag_name)
    if get_variable('beta', '0') == '1':
        new.setProp("policy", "should_pass")
    else:
        new.setProp("policy", "should_fail")
    element.replaceNode(new)

@replace("/installation/hub")
def replace_hub(element, default_for=None):
    if default_for is None:
        default_for = element
    if len(element.xpathEval('./partitioning')) == 0:
        new = load_snippet("/installation/hub/autopart", default_for, tag_name="_default_for")
        element.addChild(new)
    if len(element.xpathEval("./root_password")) == 0 and has_feature_hub_config():
        new = load_snippet("/installation/hub/root_password", default_for, tag_name="_default_for")
        if has_new_root_psswd_spoke():
            new = load_snippet("/installation/hub/new_root_password", default_for, tag_name="_default_for")
        element.addChild(new)
    if len(element.xpathEval('./begin_installation')) == 0:
        new = load_snippet("/installation/hub/begin_installation", default_for, tag_name="_default_for")
        element.addChild(new)

@replace("/installation/hub/autopart")
def replace_autopart(element, default_for=None):
    new = load_snippet("/installation/hub/autopart", element)
    element.replaceNode(new)

@replace("/installation/hub/root", cond=has_feature_hub_config())
def replace_hub_rootpw(element):
    try:
        password = element.xpathEval("./@password")[0].content
    except IndexError:
        # no password specified, just use full preset
        new = load_snippet("/installation/hub/root_password", element)
        if has_new_root_psswd_spoke():
            new = load_snippet("/installation/hub/new_root_password", element)
        element.replaceNode(new)
        return
    new = load_snippet("/installation/hub/root", element)
    if has_new_root_psswd_spoke():
        new = load_snippet("/installation/hub/new_root", element)
    element.replaceNode(new)
    new.xpathEval("./password")[0].setProp("value", password)
    new.xpathEval("./confirm_password")[0].setProp("value", password)

@replace("/installation/configuration")
def replace_configuration(element, default_for=None):
    if default_for is None:
        default_for = element
    if len(element.xpathEval("./root_password")) == 0 and not(has_feature_hub_config()):
        new = load_snippet("/installation/configuration/root_password", default_for, tag_name="_default_for")
        element.addChild(new)
        first_el = element.xpathEval("./*")[0]
        if first_el != new:
            first_el.addPrevSibling(new)
    if len(element.xpathEval("./reboot")) == 0:
        if len(element.xpathEval("./wait_until_complete")) == 0:
            new = load_snippet("/installation/configuration/wait_until_complete", default_for, tag_name="_default_for")
            element.addChild(new)
        new = load_snippet("/installation/configuration/reboot", default_for, tag_name="_default_for")
        element.addChild(new)

@replace("/installation/configuration/root", cond=not(has_feature_hub_config()))
def replace_rootpw(element):
    new = load_snippet("/installation/configuration/root", element)
    element.replaceNode(new)
    password = element.xpathEval("./@password")[0].content
    new.xpathEval("./password")[0].setProp("value", password)
    new.xpathEval("./confirm_password")[0].setProp("value", password)
