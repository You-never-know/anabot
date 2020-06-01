from anabot.runtime.actionresult import ActionResultPass as Pass
from anabot.runtime.actionresult import ActionResultFail as Fail

def assertLabelEquals(node, expected_text, label_name, message_format="%s label text (%s) is different then expected (%s)."):
    label_text = node.name
    if label_text != expected_text:
        return Fail(message_format % (label_name, label_text, expected_text))
    return Pass()

def assertTextInputEquals(node, expected_text, input_name, message_format="%s input text (%s) is different then expected (%s)."):
    input_text = node.text
    if input_text != expected_text:
        return Fail(message_format % (input_name, input_text, expected_text))
    return Pass()

BLACK_CIRCLE = u'\u25cf'
def assertPasswordTextInputEquals(node, expected_text, input_name, message_format="%s password input text (%s) is different then expected (%s).", trippled=False):
    password_text = node.text
    expected_text = BLACK_CIRCLE*len(expected_text)
    if trippled:
        expected_text *= 3
    try:
        if expected_text != password_text.decode('utf8'):
            return Fail(message_format % (input_name, password_text, expected_text))
    except (UnicodeDecodeError, AttributeError):
        if expected_text != password_text:
            return Fail(message_format % (input_name, password_text, expected_text))
    return Pass()