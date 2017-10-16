#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
test oracle functions.s
"""

from ..timing import TimedTestCase
from ..censorable import random, hexify, phony, pick_range


class test_censor_harness(TimedTestCase):

    def test_random(self):
        """No actual test, just if functions run..."""
        self.threshold = .1
        sentance = phony(hexify(random()))
        type(sentance)

    def test_range(self):
        """no assert"""
        self.threshold = .1
        ranges = pick_range(10)
        type(ranges[1])
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Yaml Config Loading - & default configs
"""
from __future__ import absolute_import
from __future__ import unicode_literals
from ...utils.timing import TimedTestCase
from ..config import configArr, generateConfig, writeConfig, openTest


class test_config(TimedTestCase):

    def test_config(self):
        """Grab Configuration From File"""
        self.threshold = .4
        newConf = configArr()
        existsConf = configArr()
        assert newConf == existsConf

    def test_bad_config(self):  # test for 38-39
        """corrupt yaml -> blank config IMPLEMENT"""
        self.threshold = .1

    def test_generate_config(self):
        """create config objects NO ASSERT"""
        self.threshold = .1
        config = {}
        config = generateConfig(config)

    def test_write_config(self):
        """writes YAML to file NO ASSERT"""
        self.threshold = .1
        config = generateConfig({})
        writeConfig('.test', config)

    def test_open_test_lacks_keys(self):
        """openTest checks for admins & users NO ASSERT"""
        self.threshold = .1
        openTest('.test')
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
test logger
## all code should be importing from ..logger, not using import logging.
"""
from __future__ import absolute_import
from __future__ import unicode_literals
from ...utils.timing import TimedTestCase
from ..logger import formatLevel, passLevel, logger
import logging


def check_level():
    logging_code = logger.getEffectiveLevel()
    human_readable = logging.getLevelName(logging_code)
    print ((logging_code, human_readable))
    return (logging_code, human_readable)


class test_logger(TimedTestCase):

    def test_logger_level(self):
        """Changing FormatLevel"""
        # need to check if this is logging correctly
        self.threshold = .4
        formatLevel('INFO')
        formatLevel('DEBUG')

    def test_pass_args(self):
        """tests for options"""
        self.threshold = .3

        class args(object):
            quiet = False
            verbose = False
            debug = False
        passLevel(args)
        assert check_level() == (30, 'WARNING')
        # should set quiet
        args.quiet = True
        passLevel(args)
        assert check_level() == (50, 'CRITICAL')
        # should set to verbose
        args.verbose = True
        passLevel(args)
        assert check_level() == (20, 'INFO')
        # should set to debug
        args.debug = True
        passLevel(args)
        assert check_level() == (10, 'DEBUG')
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
options testing
"""
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
from ...utils.timing import TimedTestCase
from ..options import MainOptions
import argparse
goodOpts = {
    'client': ['client'],
    'peer': ['peer']
}
badOpts = {
    'client': ['client', '8088'],
    'peer': ['pelt', '-p', '8080']
}


class test_options(TimedTestCase):

    def test_good_options(self):
        """All of these options should be good: NO ASSERT"""
        self.threshold = .4
        for opts in goodOpts.values():
            print(opts)
            MainOptions.parse_args(opts)

    def test_bad_options(self):
        """All of these options should fail and be caught to continue:"""
        self.threshold = .4
        for opts in badOpts.values():
            try:
                MainOptions.parse_args(opts)
            except (argparse.ArgumentError, SystemExit) as ex:
                print(("Caught: %s" % ex))
                continue
            raise Exception("Didn't fail when I expected...")
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
progress test (count to 1000)
"""
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
from ...utils.timing import TimedTestCase
from ..progress import together


class test_progress(TimedTestCase):

    def test_prog(self):
        self.threshold = 0.1
        together(1000)
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Timing tests, not using assert (need to test color?)
"""
from ..timing import TimedTestCase
import time


class test_timing(TimedTestCase):

    def test_example_no_warning(self):
        self.threshold = 3
        time.sleep(2)

    def test_example_warning(self):
        self.threshold = 1
        time.sleep(2)
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
error utilities tests

    whoops (traceback)
    CongrediError (an error class)
        - pull in all subclasses into these error class tests
"""
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
from ...utils.timing import TimedTestCase
from ..whoops import CongrediError, whoops


class test_whoops(TimedTestCase):

    def test_whoops(self):
        """The stack-trace printer needs work"""
        print('IMPLEMENT utils/test/test_whoops - MISSING ASSERT')
        self.threshold = .4
        whoops('hello')


class test_CongrediErrors(TimedTestCase):

    def test_CongrediErrors(self):
        """Raising a CongrediError class - fail if no error"""
        self.threshold = .4
        try:
            raise CongrediError('Well then')
        except CongrediError as E:
            assert isinstance(E, CongrediError)
            return True
        assert True is False
