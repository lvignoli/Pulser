# Copyright 2020 Pulser Development Team
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import numpy as np
import pytest

import qutip
from copy import deepcopy

from pulser import Sequence, Pulse, Register, Simulation
from pulser.devices import Chadoq2
from pulser.waveforms import BlackmanWaveform
from pulser.simresults import SimulationResults

q_dict = {"A": np.array([-4., 0.]),
          "B": np.array([0., 4.]),
          }
reg = Register(q_dict)

duration = 1000
pi = Pulse.ConstantDetuning(BlackmanWaveform(duration, np.pi), 0., 0)

seq = Sequence(reg, Chadoq2)

# Declare Channels
seq.declare_channel('ryd', 'rydberg_local', 'A')
seq.add(pi, 'ryd')
seq_no_meas = deepcopy(seq)
seq.measure('ground-rydberg')

sim = Simulation(seq)
results = sim.run()

state = qutip.tensor([qutip.basis(2, 0), qutip.basis(2, 0)])


def test_initialization():
    with pytest.raises(ValueError, match="`basis_name` must be"):
        SimulationResults(state, 2, 2, 'bad_basis')
    with pytest.raises(ValueError, match="`meas_basis` must be"):
        SimulationResults(state, 2, 2, 'ground-rydberg',
                          'wrong_measurement_basis')

    assert results.dim == 2
    assert results.size == 2
    assert results.basis_name == 'ground-rydberg'
    assert results.meas_basis == 'ground-rydberg'


def test_expect():
    with pytest.raises(TypeError, match="must be a list"):
        results.expect('bad_observable')
    with pytest.raises(TypeError, match="Incompatible type"):
        results.expect(['bad_observable'])
    with pytest.raises(ValueError, match="Incompatible shape"):
        results.expect([np.array(3)])


def test_sample_final_state():
    with pytest.raises(ValueError, match="undefined measurement basis"):
        sim_no_meas = Simulation(seq_no_meas)
        results_no_meas = sim_no_meas.run()
        results_no_meas.sample_final_state()
    with pytest.raises(ValueError, match="can only be"):
        results_no_meas.sample_final_state('wrong_measurement_basis')
    with pytest.raises(NotImplementedError, match="dimension > 3"):
        results_large_dim = deepcopy(results)
        results_large_dim.dim = 7
        results_large_dim.sample_final_state()

    results.sample_final_state(N_samples=1234)
    assert results.N_samples == 1234
