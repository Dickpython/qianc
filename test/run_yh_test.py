import unittest
import sys
sys.path.append('../')


testmodules = [
   "yh.yh_1_identity_test",
   "yh.yh_2_profession_test",
   "yh.yh_3_residence_test",
#    "yh.yh_4_recordsummary_test",
   "yh.yh_5_recorddeta_test",
   "yh.yh_6_creditscore_test",
   "yh.yh_7_creditsummary_test",
   "yh.yh_8_overduesummary_test",
   "yh.yh_9_shareanddebt_test",
   "yh.yh_10_loan_test",
   "yh.yh_11_loancard_test",
   "yh.yh_13_latest24mon_test",
   "yh.yh_16_specialtrade_test",
]

suite = unittest.TestSuite()

for t in testmodules:
    try:
        # If the module defines a suite() function, call it to get the suite.
        mod = __import__(t, globals(), locals(), ['suite'])
        suitefn = getattr(mod, 'suite')
        suite.addTest(suitefn())
    except (ImportError, AttributeError):
        # else, just load all the test cases from the module.
        suite.addTest(unittest.defaultTestLoader.loadTestsFromName(t))

unittest.TextTestRunner().run(suite)
