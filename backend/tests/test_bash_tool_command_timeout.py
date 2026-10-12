from types import SimpleNamespace

from deerflow.sandbox.tools import bash_tool


def test_non_local_bash_forwards_configured_command_timeout(monkeypatch):
    runtime = SimpleNamespace(
        state={"sandbox": {"sandbox_id": "e2b:test"}},
        context={"thread_id": "thread-1"},
        config={},
    )
    captured = {}

    class Sandbox:
        def execute_command(self, command, env=None, timeout=None):
            captured["timeout"] = timeout
            return "done"

    monkeypatch.setattr(
        "deerflow.config.app_config.get_app_config",
        lambda: SimpleNamespace(sandbox=SimpleNamespace(bash_output_max_chars=20000, bash_command_timeout=37.5)),
    )
    monkeypatch.setattr("deerflow.sandbox.tools.ensure_sandbox_initialized", lambda runtime: Sandbox())
    monkeypatch.setattr("deerflow.sandbox.tools.ensure_thread_directories_exist", lambda runtime: None)

    result = bash_tool.func(runtime=runtime, description="run command", command="sleep 1")

    assert result == "done"
    assert captured["timeout"] == 37.5
