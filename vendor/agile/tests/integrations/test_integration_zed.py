"""Tests for ZedIntegration."""

import json

import pytest

from agile_cli.integrations import get_integration

from .test_integration_base_skills import SkillsIntegrationTests


class TestZedIntegration(SkillsIntegrationTests):
    KEY = "zed"
    FOLDER = ".agents/"
    COMMANDS_SUBDIR = "skills"
    REGISTRAR_DIR = ".agents/skills"

    def test_options_include_skills_flag(self):
        """Not applicable to Zed — Zed is always skills-based with no --skills flag."""
        pytest.skip("Zed is always skills-based and does not expose a --skills option")

    def test_options_do_not_include_skills_flag(self):
        """Zed is always skills-based; no --skills option is exposed."""
        i = get_integration(self.KEY)
        assert i is not None
        opts = i.options()
        skills_opts = [o for o in opts if o.name == "--skills"]
        assert len(skills_opts) == 0, (
            "Zed is always skills-based and should not expose a --skills option"
        )

    def test_requires_cli_is_false(self):
        """Zed is IDE-based; requires_cli must remain False."""
        i = get_integration(self.KEY)
        assert i is not None
        assert i.config is not None
        assert i.config["requires_cli"] is False


class TestZedHookInvocations:
    """Zed hook messages should reference slash-invokable skills."""

    def test_hooks_render_skill_invocation(self, tmp_path):
        """Zed is always skills-based: renders /agile-plan even with ai_skills=False."""
        from agile_cli.extensions import HookExecutor

        project = tmp_path / "zed-hooks"
        project.mkdir()
        init_options = project / ".agile" / "init-options.json"
        init_options.parent.mkdir(parents=True, exist_ok=True)
        init_options.write_text(json.dumps({"ai": "zed", "ai_skills": False}))

        hook_executor = HookExecutor(project)
        message = hook_executor.format_hook_message(
            "before_plan",
            [
                {
                    "extension": "test-ext",
                    "command": "agile.plan",
                    "optional": False,
                }
            ],
        )

        assert "EXECUTE_COMMAND_INVOCATION: /agile-plan" in message

    def test_init_persists_ai_skills_for_zed(self, tmp_path, monkeypatch):
        """agile init --integration zed must persist ai_skills: true,
        so HookExecutor renders slash-skill invocations without manual
        init-options manipulation."""
        from typer.testing import CliRunner

        from agile_cli import app
        from agile_cli.extensions import HookExecutor

        project = tmp_path / "zed-init-test"
        project.mkdir()
        monkeypatch.chdir(project)
        runner = CliRunner()
        result = runner.invoke(
            app,
            [
                "init",
                "--here",
                "--integration",
                "zed",
                "--script",
                "sh",
                "--ignore-agent-tools",
            ],
            catch_exceptions=False,
        )

        assert result.exit_code == 0, f"init failed: {result.output}"

        opts_path = project / ".agile" / "init-options.json"
        assert opts_path.exists()
        opts = json.loads(opts_path.read_text(encoding="utf-8"))
        assert opts.get("ai") == "zed"
        assert opts.get("ai_skills") is True, (
            f"init must persist ai_skills=true for Zed, got: {opts.get('ai_skills')}"
        )

        hook_executor = HookExecutor(project)
        message = hook_executor.format_hook_message(
            "before_plan",
            [
                {
                    "extension": "test-ext",
                    "command": "agile.plan",
                    "optional": False,
                }
            ],
        )
        assert "Executing: `/agile-plan`" in message, (
            "Hook rendering must produce /agile-plan for Zed without hint injection"
        )
        assert "EXECUTE_COMMAND_INVOCATION: /agile-plan" in message


class TestSlashSkillsSets:
    """Parameterized coverage for ALWAYS_SLASH_AGENTS / CONDITIONAL_SLASH_AGENTS."""

    @staticmethod
    def _render_invocation(project_path, ai: str, ai_skills: bool) -> str:
        """Return the rendered invocation for ``agile.plan`` via HookExecutor."""
        from agile_cli.extensions import HookExecutor

        init_options = project_path / ".agile" / "init-options.json"
        init_options.parent.mkdir(parents=True, exist_ok=True)
        init_options.write_text(json.dumps({"ai": ai, "ai_skills": ai_skills}))
        hook_executor = HookExecutor(project_path)
        result = hook_executor.execute_hook(
            {"extension": "test-ext", "command": "agile.plan", "optional": False}
        )
        return result.get("invocation", "")

    @pytest.mark.parametrize(
        ("ai", "ai_skills", "expected"),
        [
            # ALWAYS_SLASH_AGENTS — unconditional on ai_skills
            ("devin", True, "/agile-plan"),
            ("devin", False, "/agile-plan"),
            ("grok", True, "/agile-plan"),
            ("grok", False, "/agile-plan"),
            ("qodercli", True, "/agile-plan"),
            ("qodercli", False, "/agile-plan"),
            ("trae", True, "/agile-plan"),
            ("trae", False, "/agile-plan"),
            ("zed", True, "/agile-plan"),
            ("zed", False, "/agile-plan"),
            # CONDITIONAL_SLASH_AGENTS — only when ai_skills is enabled
            ("agy", True, "/agile-plan"),
            ("agy", False, "/agile.plan"),
            ("claude", True, "/agile-plan"),
            ("claude", False, "/agile.plan"),
            ("copilot", True, "/agile-plan"),
            ("copilot", False, "/agile.plan"),
            ("cursor-agent", True, "/agile-plan"),
            ("cursor-agent", False, "/agile.plan"),
        ],
    )
    def test_hook_invocation_format(self, tmp_path, ai, ai_skills, expected):
        result = self._render_invocation(tmp_path, ai, ai_skills)
        assert result == expected, (
            f"{ai} (ai_skills={ai_skills}): expected {expected!r}, got {result!r}"
        )
