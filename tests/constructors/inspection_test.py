# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2023 Scipp contributors (https://github.com/scipp)

import pytest

from appstract.constructors import Empty, UnknownType
from appstract.constructors.inspectors import DependencySpec, ProductSpec


def test_product_spec_compare():
    _left_spec = ProductSpec(int)
    _right_spec = ProductSpec(int)
    assert _left_spec == _right_spec


def test_product_spec_compare_false():
    _left_spec = ProductSpec(int)
    _right_spec = ProductSpec(float)
    assert _left_spec != _right_spec


def test_product_spec_compare_with_wrong_type_raises():
    _seed_spec = ProductSpec(int)
    with pytest.raises(NotImplementedError):
        assert _seed_spec != int  # noqa: E721
        # This test is for testing if the comparison is implemented correctly


def test_nested_product_spec_not_allowed():
    _seed_spec = ProductSpec(int)
    _wrapped_again = ProductSpec(_seed_spec)
    assert _seed_spec is not _wrapped_again
    assert _seed_spec == _wrapped_again


def test_new_type_underlying_type_retrieved():
    from typing import NewType

    new_type = NewType("new_type", int)
    product_spec = ProductSpec(new_type)
    assert product_spec.product_type is new_type
    assert product_spec.returned_type is int


def test_multi_inheritied_new_type_underlying_type_retrieved():
    from typing import NewType

    new_type = NewType("new_type", int)
    new_new_type = NewType("new_new_type", new_type)
    product_spec = ProductSpec(new_new_type)
    assert product_spec.product_type is new_new_type
    assert product_spec.returned_type is int


def test_dependency_spec():
    dep_spec = DependencySpec(int, 0)
    assert dep_spec.dependency_type is int
    assert dep_spec.default_product == 0
    assert dep_spec.is_optional()


def test_dependency_spec_unknown():
    unknown_spec = DependencySpec(UnknownType, 0)
    assert unknown_spec.is_optional()
    unknown_spec = DependencySpec(UnknownType, Empty)
    assert unknown_spec.is_optional()


def test_dependency_spec_not_optional():
    empty_spec = DependencySpec(type(Empty), Empty)
    assert not empty_spec.is_optional()


def test_dependency_spec_optional_annotation():
    union_int_spec = DependencySpec(None | int, None)
    assert union_int_spec.dependency_type is int
    optional_int_spec = DependencySpec(int | None, None)
    assert optional_int_spec.dependency_type is int
