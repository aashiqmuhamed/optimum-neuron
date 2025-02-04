# coding=utf-8
# Copyright 2023 The HuggingFace Inc. team. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Version utilities."""
from typing import Optional

from packaging import version

from .import_utils import is_neuron_available, is_neuronx_available


_neuronxcc_version: Optional[str] = None
_neuroncc_version: Optional[str] = None


def get_neuronxcc_version() -> str:
    global _neuronxcc_version
    if _neuronxcc_version is not None:
        return _neuronxcc_version
    try:
        import neuronxcc
    except ImportError:
        raise ValueError("NeuronX Compiler python package is not installed.")
    _neuronxcc_version = neuronxcc.__version__
    return _neuronxcc_version


def get_neuroncc_version() -> str:
    global _neuroncc_version
    if _neuroncc_version is not None:
        return _neuroncc_version
    try:
        import neuroncc
    except ImportError:
        raise ValueError("Neuron Compiler python package is not installed.")
    _neuroncc_version = neuroncc.__version__
    return _neuroncc_version


def check_compiler_compatibility(compiler_type: str, compiler_version: str):
    if compiler_type == "neuron-cc":
        compiler_available_fn = is_neuron_available
        installed_compiler_version_fn = get_neuroncc_version
    elif compiler_type == "neuronx-cc":
        compiler_available_fn = is_neuronx_available
        installed_compiler_version_fn = get_neuronxcc_version
    else:
        raise RuntimeError(f"Pretrained model compiler type {compiler_type} not recognized.")

    if not compiler_available_fn():
        raise RuntimeError(f"Pretrained model was compiled for {compiler_type}, but {compiler_type} is not installed.")

    if version.parse(compiler_version) > version.parse(installed_compiler_version_fn()):
        raise RuntimeError(
            f"Pretrained model is compiled with {compiler_type}({compiler_version}) newer than current compiler ({installed_compiler_version_fn()}),"
            " which may cause runtime incompatibilities."
        )
