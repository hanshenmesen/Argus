from __future__ import annotations

from types import SimpleNamespace

import pytest

from argus_skill.core.runner_errors import (
    is_pre_provider_refusal_error,
    is_unrecoverable_resume_error,
    result_has_pre_provider_refusal,
    result_has_unrecoverable_resume_state,
)


def test_encrypted_manager_thread_failure_is_unrecoverable() -> None:
    error = (
        '{"error":{"message":"The encrypted content gAAA... could not be '
        'verified. Reason: Encrypted content could not be decrypted or parsed.",'
        '"code":"invalid_request_body"}}'
    )

    assert is_unrecoverable_resume_error(error)
    assert result_has_unrecoverable_resume_state(
        SimpleNamespace(fatal_error=error, stderr_lines=[])
    )


def test_ordinary_provider_failure_does_not_rotate_resume_state() -> None:
    error = "rate limit exceeded; retry later"

    assert not is_unrecoverable_resume_error(error)
    assert not result_has_unrecoverable_resume_state(
        SimpleNamespace(fatal_error=error, stderr_lines=[])
    )


@pytest.mark.parametrize("error", [
    "Error: Access denied by policy settings. Your Copilot CLI policy is disabled.",
    "Your Copilot subscription does not include this feature",
    "Required policies have not been enabled for Copilot CLI",
])
def test_copilot_startup_policy_refusal_is_recognized(error: str) -> None:
    assert is_pre_provider_refusal_error(error)
    assert result_has_pre_provider_refusal(
        SimpleNamespace(exit_code=0, fatal_error=None, stderr_lines=[error])
    )


def test_generic_policy_failure_is_not_assumed_to_be_before_provider() -> None:
    assert not is_pre_provider_refusal_error("The generated change failed repository policy checks")
