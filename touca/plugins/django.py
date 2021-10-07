#!/usr/bin/env python

# Copyright 2021 Touca, Inc. Subject to Apache-2.0 License.

from django.test.runner import DiscoverRunner
from unittest import ToucaTestSuite, ToucaTestRunner
import touca


class ToucaRunner(DiscoverRunner):
    def __init__(
        self, api_key=None, api_url=None, revision=None, offline=None, **kwargs
    ):
        super().__init__(**kwargs)
        self.touca_options = {
            "api_key": api_key,
            "api_url": api_url,
            "version": revision,
            "offline": True if offline in [True, "True", "true"] else False,
        }
        self.touca_options = {
            k: v for k, v in self.touca_options.items() if v is not None
        }
        print(self.touca_options)

    def setup_test_environment(self, **kwargs):
        super(ToucaRunner, self).setup_test_environment(**kwargs)
        touca.configure(**self.touca_options)

    def run_tests(self, test_labels, extra_tests=None, **kwargs):
        self.test_suite = ToucaTestSuite
        self.test_loader.suiteClass = ToucaTestSuite
        self.test_runner = ToucaTestRunner
        super().run_tests(test_labels, extra_tests, **kwargs)

    @classmethod
    def add_arguments(cls, parser):
        DiscoverRunner.add_arguments(parser)
        parser.add_argument("--api-key", dest="api_key", help="Touca API Key")
        parser.add_argument("--api-url", dest="api_url", help="Touca API URL")
        parser.add_argument("--revision", dest="revision", help="Touca Test Version")
        parser.add_argument(
            "--offline",
            action="store",
            default=False,
            help="Disables all communications with the Touca server",
        )
