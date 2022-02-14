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
"""Tests for simulations with sequence modulation."""

import numpy as np
import pytest
import qutip
from qutip import Qobj

from pulser import Pulse, Register, Sequence
from pulser.channels import Rydberg
from pulser.devices import Device
from pulser.simulation import Simulation
from pulser.waveforms import BlackmanWaveform, RampWaveform


@pytest.fixture
def modulated_mock_device() -> Device:
    """A Mock device with only one modulated channel."""
    chan = Rydberg(
        "Global",
        1000,
        200,
        clock_period=1,
        min_duration=1,
        mod_bandwidth=4.00,  # MHz
    )

    return Device(
        name="ModDevice",
        dimensions=3,
        rydberg_level=70,
        max_atom_num=2000,
        max_radial_distance=1000,
        min_atom_distance=1,
        _channels=(("rydberg_global", chan),),
    )


@pytest.fixture
def single_atom_register() -> Register:
    return Register.from_coordinates([(0.0, 0.0)], prefix="atom")


@pytest.fixture
def input_seq(modulated_mock_device, single_atom_register) -> Sequence:
    """An input sequence for ramps running on a modulated mock device."""
    Omega_max = 2.3 * 2 * np.pi
    U = Omega_max / 2.3
    delta_0 = -3 * U
    delta_f = 1 * U
    t_rise = 2000  # ns
    t_fall = 2000
    t_sweep = int(5000 * ((delta_f - delta_0) / (2 * np.pi * 10)))  # ns

    rise = Pulse.ConstantDetuning(
        RampWaveform(t_rise, 0.0, Omega_max), delta_0, 0.0
    )
    sweep = Pulse.ConstantAmplitude(
        Omega_max, RampWaveform(t_sweep, delta_0, delta_f), 0.0
    )
    fall = Pulse.ConstantDetuning(
        RampWaveform(t_fall, Omega_max, 0.0), delta_f, 0.0
    )

    seq = Sequence(single_atom_register, modulated_mock_device)
    seq.declare_channel("ch0", "rydberg_global")
    seq.add(rise, "ch0")
    seq.add(sweep, "ch0")
    seq.add(fall, "ch0")

    return seq


@pytest.fixture
def wanted_final_state() -> Qobj:
    """The final state of the simulation with modulation."""
    ...
    return Qobj()


# @pytest.fixture
# def single_blackman


def test_blackman_modulated_samples(input_seq):
    ...


# ! Pas très utile: il ne fail pas avant l'implémentation !!!
def test_blackman_final_state(single_atom_register, modulated_mock_device):
    """Test that the modulation of a Blackman pi pulse indeed gives a |1>."""
    seq = Sequence(single_atom_register, modulated_mock_device)
    seq.declare_channel("ch0", "rydberg_global")
    seq.add(
        Pulse.ConstantDetuning(BlackmanWaveform(1000, np.pi), 0.0, 0),
        "ch0",
    )
    seq.measure("ground-rydberg")

    sim = Simulation(seq, mod_output=True)
    sim.initial_state = "all-ground"
    print(f"The inititial state is {sim.initial_state}")
    res = sim.run()

    got = res.get_final_state()
    want = qutip.basis(2, 0)
    np.testing.assert_allclose(got, want, 0.0, 1e-5)


def test_final_state(input_seq, wanted_final_state):
    # Simulate the sequence with output modulation
    # sim =...
    # result = sim.run(output_mod=True)
    ...
    # Compare the final state with the expected one
    # got = result.final_state
    # assert got == want
    ...


# UNUSED FOR NOW

# @pytest.fixture
# def modulated_samples(input_seq) -> Sequence:
#     """Hand crafting the modulated samples of the sequence."""
#     return seq


# @pytest.fixture
# def modulated_samples(input_seq) -> Sequence:
#     """Hand crafting the modulated samples of the sequence."""
#     return seq


# # @pytest.mark.usefixtures("input_seq")
# class TestSimulationWithModulation:
#     """Tests for the simulation of sequences with modulated pulses.

#     That is pulses on channels that have a modulation bandwith, modeling real
#     amplitude modulators.
#     """

#     pass
