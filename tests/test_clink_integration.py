import json
import shutil

import pytest

from tools.clink import CLinkTool


@pytest.mark.integration
@pytest.mark.asyncio
async def test_clink_agy_single_digit_sum():
    if shutil.which("agy") is None:
        pytest.skip("agy CLI is not installed or on PATH")

    tool = CLinkTool()
    prompt = "Respond with a single digit equal to the sum of 2 + 2. Output only that digit."

    results = await tool.execute(
        {
            "prompt": prompt,
            "cli_name": "agy",
            "role": "default",
            "absolute_file_paths": [],
            "images": [],
        }
    )

    assert results, "clink tool returned no outputs"
    payload = json.loads(results[0].text)
    status = payload["status"]

    if status == "error":
        metadata = payload.get("metadata") or {}
        reason = payload.get("content") or metadata.get("message") or "Antigravity CLI reported an error"
        # Skip only for environmental causes. A parser regression, a bad flag,
        # or broken prompt delivery must fail rather than report green.
        environmental = ("unauthorized", "not logged in", "credential", "quota", "rate limit", "network")
        if any(marker in reason.lower() for marker in environmental):
            pytest.skip(f"Skipping Antigravity integration test: {reason}")
        pytest.fail(f"Antigravity CLI returned an error: {reason}")

    assert status in {"success", "continuation_available"}

    content = payload.get("content", "").strip()
    # agy appends a <SUMMARY> block, so assert on the answer line rather than the whole body.
    first_line = content.split("\n")[0].strip()
    assert first_line == "4", f"Expected '4' as the first line, got: {content[:100]}"

    metadata = payload.get("metadata") or {}
    assert metadata.get("cli_name") == "agy"
