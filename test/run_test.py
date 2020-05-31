import unittest
import sys
sys.path.append('../')


testmodules = [
   "basic.aggregator_test",
    "basic.generate_test",
   "basic.preprocess_test",
   "basic.filter_test",
   "basic.filter_24m_quantile_test",
   "basic.prepro_time_interval_test",
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
