# coding=utf-8
# Copyright 2015 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

from __future__ import (absolute_import, division, generators, nested_scopes, print_function,
                        unicode_literals, with_statement)

import pytest
from pants_test.pants_run_integration_test import PantsRunIntegrationTest

from pants.contrib.cpp.toolchain.cpp_toolchain import CppToolchain


class CppIntegrationTest(PantsRunIntegrationTest):
  """Integration test for cpp which builds libraries and builds and runs binaries."""

  TEST_SIMPLE_BINARY_TARGET = 'contrib/cpp/examples/src/cpp/example:hello_pants'
  TEST_BINARY_WITH_LIBRARY_TARGET = 'contrib/cpp/examples/src/cpp/calcsqrt'
  TEST_LIBRARY_TARGET = 'contrib/cpp/examples/src/cpp/example/hello'
  TEST_RUN_TARGET = TEST_SIMPLE_BINARY_TARGET

  @classmethod
  def has_compiler(cls):
    try:
      compiler = CppToolchain().compiler
    except Exception:
      return False
    return True

  @pytest.mark.skipif('not CppIntegrationTest.has_compiler()',
                      reason='cpp integration tests require compiler')
  def test_cpp_library(self):
    self._binary_test(self.TEST_LIBRARY_TARGET)

  @pytest.mark.skipif('not CppIntegrationTest.has_compiler()',
                      reason='cpp integration tests require compiler')
  def test_cpp_binary(self):
    self._binary_test(self.TEST_SIMPLE_BINARY_TARGET)

  @pytest.mark.skipif('not CppIntegrationTest.has_compiler()',
                      reason='cpp integration tests require compiler')
  def test_cpp_binary_with_library(self):
    self._binary_test(self.TEST_BINARY_WITH_LIBRARY_TARGET)

  @pytest.mark.skipif('not CppIntegrationTest.has_compiler()',
                      reason='cpp integration tests require compiler')
  def test_cpp_run(self):
    pants_run = self.run_pants(['run', self.TEST_RUN_TARGET])
    self.assert_success(pants_run)
    self.assertIn('[cpp-run]Hello, pants!\nGoodbye, pants!\n',
                  pants_run.stdout_data)

  def _binary_test(self, target):
    pants_run = self.run_pants(['binary', target])
    self.assert_success(pants_run)
