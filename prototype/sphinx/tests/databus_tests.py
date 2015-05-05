# -*- coding: utf-8 -*- {{{
# vim: set fenc=utf-8 ft=python sw=4 ts=4 sts=4
# APBS -- Adaptive Poisson-Boltzmann Solver
#
#  Nathan A. Baker (nathan.baker@pnnl.gov)
#  Pacific Northwest National Laboratory
#
#  Additional contributing authors listed in the code documentation.
#
# Copyright (c) 2010-2015 Battelle Memorial Institute. Developed at the
# Pacific Northwest National Laboratory, operated by Battelle Memorial
# Institute, Pacific Northwest Division for the U.S. Department of Energy.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# Redistributions of source code must retain the above copyright notice, this
# list of conditions and the following disclaimer.
#
# Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# Neither the name of the developer nor the names of its contributors may be
# used to endorse or promote products derived from this software without
# specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF
# THE POSSIBILITY OF SUCH DAMAGE.
#}}}

from nose.tools import *

from sphinx.databus import SDBController, SphinxTypeError
from sphinx.plugin import BasePlugin

__author__ = 'Keith T. Star <keith@pnnl.gov>'


def setup_plugins():
	global databus

	databus = SDBController()
	databus.add_plugin(TestPlugin)


def test_validate_type():
	databus = SDBController()
	databus.validate_type({'type': 'file_extension', 'value': {'ext': '.in'}})


@raises(SphinxTypeError)
def test_validate_type_fail_bad_type():
	databus = SDBController()
	databus.validate_type({'type': 'ile_extension', 'value': {'ext': '.in'}})


@raises(SphinxTypeError)
def test_validate_type_fail_bad_value():
	databus = SDBController()
	databus.validate_type({'type': 'file_extension', 'value': {'ext': 'in'}})


@with_setup(setup_plugins)
def test_add_plugin():
	pass
# 	# Test that the sources are properly captured.
# 	foo_sources = databus.sources_for({'type': 'file/.foo'})
# 	assert_equal(2, len(foo_sources))
# 	assert_in(TestPlugin, foo_sources)
# 	assert_in(DuplicateTestPlugin, foo_sources)
#
# 	bar_sources = databus.sources_for({'type': 'bar'})
# 	assert_equal(1, len(bar_sources))
# 	assert_in(SymmetricTestPlugin, bar_sources)
#
# 	baz_sources = databus.sources_for({'type': 'baz'})
# 	assert_equal(1, len(baz_sources))
# 	assert_in(SymmetricTestPlugin, baz_sources)
#
# 	# Test that the sinks are properly captured.
# 	foo_sinks = databus.sinks_for({'type': 'file/.foo'})
# 	assert_equal(1, len(foo_sinks))
# 	assert_in(SymmetricTestPlugin, foo_sinks)
#
# 	bar_sinks = databus.sinks_for({'type': 'bar'})
# 	assert_equal(2, len(bar_sinks))
# 	assert_in(TestPlugin, bar_sinks)
# 	assert_in(DuplicateTestPlugin, bar_sinks)
#
# 	baz_sinks = databus.sinks_for({'type': 'baz'})
# 	assert_equal(2, len(baz_sinks))
# 	assert_in(TestPlugin, baz_sinks)
# 	assert_in(DuplicateTestPlugin, baz_sinks)


class TestPlugin(BasePlugin):
	'''Super simple plugin that has sources and sinks
	'''
	def __init__(self):
		super().__init__()

	@classmethod
	def sinks(cls):
		return [{'type': 'file_extension', 'value': {'ext': '.in'}}]

	@classmethod
	def sources(cls):
		return [{'type': 'file/.foo'}]

	def run(self):
		pass
