# Copyright (c) 2026 Edgar-Ramírez Mondragón

"""Tests standard target features using the built-in SDK tests library."""

from __future__ import annotations

import typing as t
import uuid

from singer_sdk.testing import get_target_test_class

from target_firebase.target import TargetFirebase

SAMPLE_CONFIG: dict[str, t.Any] = {
    "firebase_app": f"app-{uuid.uuid4().hex}",
}


# Run standard built-in target tests from the SDK:
StandardTargetTests = get_target_test_class(
    target_class=TargetFirebase,
    config=SAMPLE_CONFIG,
)


class TestTargetFirebase(StandardTargetTests):  # type: ignore[misc, valid-type]  # ty:ignore[unsupported-base]
    """Standard Target Tests."""
