"""
    Copyright 2023 Contributors

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""
import os

import numpy as np
import torch as th

from graphstorm.gconstruct.utils import _estimate_sizeof, _to_numpy_array, _to_shared_memory

def gen_data():
    data_th = th.zeros((1024, 16), dtype=th.float32)
    data_np = np.ndarray(shape=(1024, 16), dtype=np.single)

    data_dict = {
        "th": data_th,
        "np": data_np
    }

    data_list = [data_th, data_np]
    data_tuple = (data_th, data_np)

    data_mixed = {
        "list": [data_dict, data_dict],
        "tuple": (data_list, data_tuple),
    }

    return data_th, data_np, data_dict, data_list, data_tuple, data_mixed

def test_estimate_sizeof():
    data_th, data_np, data_dict, data_list, data_tuple, data_mixed = gen_data()
    # object is torch tensor
    data_th_size = data_th.nelement() * 4
    assert _estimate_sizeof(data_th) == data_th_size

    # object is numpy array
    data_np_size = data_np.size * 4
    assert _estimate_sizeof(data_np) == data_np_size

    # object is a dict
    data_dict_size = data_th_size + data_np_size
    assert _estimate_sizeof(data_dict) == data_dict_size

    # object is a list
    data_list_size = data_th_size + data_np_size
    assert _estimate_sizeof(data_list) == data_list_size

    # object is a tuple
    data_tuple_size = data_th_size + data_np_size
    assert _estimate_sizeof(data_tuple) == data_tuple_size

    # object is recursive obj
    data_mixed_size = data_dict_size * 2 + data_list_size + data_tuple_size
    assert _estimate_sizeof(data_mixed) == data_mixed_size

def test_object_conversion():
    data_th, data_np, data_dict, data_list, data_tuple, data_mixed = gen_data()

    def check_is_shared(data):
        assert th.is_tensor(data)
        assert data.is_shared()
    def check_is_numpy(data):
        assert isinstance(data, np.ndarray)

    new_data = _to_shared_memory(data_th)
    check_is_shared(new_data)
    new_data = _to_numpy_array(new_data)
    check_is_numpy(new_data)

    new_data = _to_shared_memory(data_np)
    check_is_shared(new_data)
    new_data = _to_numpy_array(new_data)
    check_is_numpy(new_data)

    new_data = _to_shared_memory(data_dict)
    assert isinstance(new_data, dict)
    check_is_shared(new_data["th"])
    check_is_shared(new_data["np"])
    new_data = _to_numpy_array(new_data)
    assert isinstance(new_data, dict)
    check_is_numpy(new_data["th"])
    check_is_numpy(new_data["np"])

    new_data = _to_shared_memory(data_list)
    assert isinstance(new_data, list)
    check_is_shared(new_data[0])
    check_is_shared(new_data[1])
    new_data = _to_numpy_array(new_data)
    assert isinstance(new_data, list)
    check_is_numpy(new_data[0])
    check_is_numpy(new_data[1])

    new_data = _to_shared_memory(data_tuple)
    assert isinstance(new_data, tuple)
    check_is_shared(new_data[0])
    check_is_shared(new_data[1])
    new_data = _to_numpy_array(new_data)
    assert isinstance(new_data, tuple)
    check_is_numpy(new_data[0])
    check_is_numpy(new_data[1])

    new_data = _to_shared_memory(data_mixed)
    assert isinstance(new_data, dict)
    assert isinstance(new_data["list"], list)
    assert isinstance(new_data["list"][0], dict)
    check_is_shared(new_data["list"][0]["th"])
    check_is_shared(new_data["list"][0]["np"])
    assert isinstance(new_data["list"][1], dict)
    check_is_shared(new_data["list"][1]["th"])
    check_is_shared(new_data["list"][1]["np"])
    assert isinstance(new_data["tuple"], tuple)
    assert isinstance(new_data["tuple"][0], list)
    check_is_shared(new_data["tuple"][0][0])
    check_is_shared(new_data["tuple"][0][1])
    assert isinstance(new_data["tuple"][1], tuple)
    check_is_shared(new_data["tuple"][0][0])
    check_is_shared(new_data["tuple"][0][1])
    new_data = _to_numpy_array(new_data)
    assert isinstance(new_data, dict)
    assert isinstance(new_data["list"], list)
    assert isinstance(new_data["list"][0], dict)
    check_is_numpy(new_data["list"][0]["th"])
    check_is_numpy(new_data["list"][0]["np"])
    assert isinstance(new_data["list"][1], dict)
    check_is_numpy(new_data["list"][1]["th"])
    check_is_numpy(new_data["list"][1]["np"])
    assert isinstance(new_data["tuple"], tuple)
    assert isinstance(new_data["tuple"][0], list)
    check_is_numpy(new_data["tuple"][0][0])
    check_is_numpy(new_data["tuple"][0][1])
    assert isinstance(new_data["tuple"][1], tuple)
    check_is_numpy(new_data["tuple"][0][0])
    check_is_numpy(new_data["tuple"][0][1])

if __name__ == '__main__':
    test_estimate_sizeof()
    test_object_conversion()