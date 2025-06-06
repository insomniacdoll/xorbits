# Copyright 2022-2023 XProbe Inc.
# derived from copyright 1999-2021 Alibaba Group Holding Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import numpy as np
import pytest

from ...lib.mmh3 import hash_from_buffer as mmh3_hash_from_buffer
from ..utils import hash_on_axis, normalize_axis_tuple


def test_hash_on_axis():
    def hash_from_buffer(x):
        return mmh3_hash_from_buffer(memoryview(x))

    a = np.random.rand(10)

    result = hash_on_axis(a, 0, 3)
    expected = np.array([mmh3_hash_from_buffer(element) % 3 for element in a])

    np.testing.assert_array_equal(result, expected)

    result = hash_on_axis(a, 0, 1)
    expected = np.array([0 for _ in a])

    np.testing.assert_array_equal(result, expected)

    a = np.random.rand(10, 5)

    result = hash_on_axis(a, 0, 3)
    expected = np.array([hash_from_buffer(a[i, :]) % 3 for i in range(a.shape[0])])

    np.testing.assert_array_equal(result, expected)

    result = hash_on_axis(a, 1, 3)
    expected = np.array([hash_from_buffer(a[:, i]) % 3 for i in range(a.shape[1])])

    np.testing.assert_array_equal(result, expected)

    a = np.random.rand(10, 5, 4)

    result = hash_on_axis(a, 2, 3)
    expected = np.array([hash_from_buffer(a[:, :, i]) % 3 for i in range(a.shape[2])])

    np.testing.assert_array_equal(result, expected)


def test_normalize_axis_tuple():
    assert normalize_axis_tuple(-1, 3) == (2,)
    assert normalize_axis_tuple([0, -2], 3) == (0, 1)
    assert sorted(normalize_axis_tuple({0, -2}, 3)) == [0, 1]

    with pytest.raises(ValueError) as cm:
        normalize_axis_tuple((1, -2), 3, argname="axes")
    assert "axes" in str(cm.value)

    with pytest.raises(ValueError):
        normalize_axis_tuple((1, -2), 3)
