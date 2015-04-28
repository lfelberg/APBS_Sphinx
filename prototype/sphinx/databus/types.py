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

import simplejson as json
from jsl import Document, DocumentField, NumberField, DictField, ArrayField
from jsonschema import validate
import msgpack

import logging

class Position(Document):
	class Options():
		title = "3-D Position Tuple"
		description = "General 3 dimensional position information."

	x = NumberField(description="x location", required=True)
	y = NumberField(description="y location", required=True)
	z = NumberField(description="z location", required=True)

class Charge(Document):
	class Options():
		title = "Charge"
		description = "Electrostatic charge, in electrons."

	charge = NumberField(required=True)

class Atom(Position, Charge):
	class Options():
		title = "An atom"
		description = "Properties of an atom."

	radius = NumberField(required=True, minimum=0.0, exclusive_minimum=True)

class Molecule(Document):
	class Options():
		title = "A molecule"
		description = "All things molecular..."

	atoms = ArrayField(description="Atom list", items=Atom)

class DataBus(Document):
	class Options():
		title = "APBS Data Bus"
		description = "Used to store types for plugins, as well as plugin output."

	types = DictField(description="These are the base types that may be instantiated.")
	data = DictField(description="These are runs of a pipeline, indexed by a UUID.")

print(json.dumps(DataBus.get_schema(), indent=4 * ' '))

# foo = {"position":
# 		{"x": 0.0, "y": -10.0, "z": 10.0},
# 		"radius": 0.00001,
# 		"charge": {'q': 1.0}}
foo = {'x': 0.0, 'y': -10.0, 'z': 10.0,
		'radius': 0.00001,
		'charge': 1.0}
validate(foo, Atom.get_schema())
mol = {'atoms': [foo]}
validate(mol, Molecule.get_schema())

json_str = json.dumps(foo, indent=4 * ' ')
print(json_str)
packed = msgpack.packb(foo, use_bin_type=True)
print(len(packed), packed)
print(msgpack.unpackb(packed))
print("packed by {}%.".format(len(packed)/len(json_str)*100))

orig = msgpack.unpackb(packed, encoding='utf-8')
print(type(orig))
print(orig['charge'])

bar = {'types': {'position': Position.get_schema(), 'charge': Charge.get_schema(),
		'atom': Atom.get_schema(), 'molecule': Molecule.get_schema()}}
bar['data'] = {'foo': mol}
print(json.dumps(bar, indent=4 * ' '))
validate(bar, DataBus.get_schema())
