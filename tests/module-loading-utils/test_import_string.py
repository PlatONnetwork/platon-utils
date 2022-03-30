from platon_utils.decorators import combomethod
from platon_utils.module_loading import import_string


def test_import_string():
    imported_combomethod = import_string("platon_utils.decorators.combomethod")
    assert imported_combomethod is combomethod
