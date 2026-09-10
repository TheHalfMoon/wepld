"""Tests for ClineIntegration."""

import os
import pytest

from agile_cli.integrations import get_integration
from agile_cli.integrations.cline import format_cline_command_name
from .test_integration_base_markdown import MarkdownIntegrationTests


class TestClineCommandNameFormatter:
    """Test the Cline command name formatter."""

    def test_simple_name_without_prefix(self):
        """Test formatting a simple name without 'agile.' prefix."""
        assert format_cline_command_name("plan") == "agile-plan"
        assert format_cline_command_name("tasks") == "agile-tasks"
        assert format_cline_command_name("agile") == "agile-specify"

    def test_name_with_agile_prefix(self):
        """Test formatting a name that already has 'agile.' prefix."""
        assert format_cline_command_name("agile.plan") == "agile-plan"
        assert format_cline_command_name("agile.tasks") == "agile-tasks"

    def test_extension_command_name(self):
        """Test formatting extension command names with dots."""
        assert (
            format_cline_command_name("agile.my-extension.example")
            == "agile-my-extension-example"
        )
        assert (
            format_cline_command_name("my-extension.example")
            == "agile-my-extension-example"
        )

    def test_idempotent_already_hyphenated(self):
        """Test that already-hyphenated names are returned unchanged (idempotent)."""
        assert format_cline_command_name("agile-plan") == "agile-plan"
        assert (
            format_cline_command_name("agile-my-extension-example")
            == "agile-my-extension-example"
        )


class TestClineIntegration(MarkdownIntegrationTests):
    KEY = "cline"
    FOLDER = ".clinerules/"
    COMMANDS_SUBDIR = "workflows"
    REGISTRAR_DIR = ".clinerules/workflows"

    @pytest.mark.parametrize(
        "cmd_name, expected_filename",
        [
            ("plan", "agile-plan.md"),
            ("agile.plan", "agile-plan.md"),
            ("agile.git.commit", "agile-git-commit.md"),
            ("agile", "agile-specify.md"),
            ("agilefoo", "agile-specifyfoo.md"),
        ],
    )
    def test_cline_command_filename(self, cmd_name, expected_filename):
        """Verify Cline uses hyphenated filenames."""
        cline = get_integration("cline")
        assert cline.command_filename(cmd_name) == expected_filename

    def test_cline_invoke_separator(self):
        """Verify Cline uses hyphen as invoke separator."""
        cline = get_integration("cline")
        assert cline.invoke_separator == "-"
        assert cline.registrar_config["invoke_separator"] == "-"

    def test_cline_name_injection_and_formatting(self):
        """Verify Cline has inject_name and format_name configured."""
        cline = get_integration("cline")
        assert cline.registrar_config["inject_name"] is True
        assert cline.registrar_config["format_name"] == format_cline_command_name

    def test_cline_handoff_rewrite(self):
        """Verify Cline rewrites agent: agile.foo to agent: agile-foo."""
        cline = get_integration("cline")
        content = "---\nagent: agile.plan\n---\n"
        rewritten = cline._rewrite_handoff_references(content)
        assert rewritten == "---\nagent: agile-plan\n---\n"

    def test_cline_hook_instruction_injection(self):
        """Verify Cline injects the dot-to-hyphen note for hooks."""
        cline = get_integration("cline")
        content = "- For each executable hook, output the following:\n"
        injected = cline._inject_hook_command_note(content)
        assert "replace dots (`.`) with hyphens (`-`)" in injected
        assert "- For each executable hook, output the following:" in injected

    def test_cline_hook_instruction_injection_no_trailing_newline(self):
        """Note must not collapse onto the instruction line when the
        instruction is the final line with no trailing newline.

        The injection regex matches the end-of-line via ``(\\r\\n|\\n|$)``, so
        the captured ``eol`` is empty on a file's last line that lacks a
        trailing newline. Without an ``or "\\n"`` fallback the note text and
        the instruction are emitted on the same line.
        """
        cline = get_integration("cline")
        content = "- For each executable hook, output the following:"  # no trailing \n
        injected = cline._inject_hook_command_note(content)
        assert "replace dots (`.`) with hyphens (`-`)" in injected
        # Instruction stays on its own line rather than being mashed onto the note.
        assert "\n- For each executable hook, output the following:" in injected

    # -- Overrides for MarkdownIntegrationTests ---------------------------

    def test_setup_creates_files(self, tmp_path):
        from agile_cli.integrations.manifest import IntegrationManifest

        i = get_integration(self.KEY)
        m = IntegrationManifest(self.KEY, tmp_path)
        created = i.setup(tmp_path, m)
        assert len(created) > 0
        cmd_files = [
            f
            for f in created
            if "scripts" not in f.parts
            and f.suffix == ".md"
        ]
        for f in cmd_files:
            assert f.exists()
            assert f.name.startswith("agile-")
            assert f.name.endswith(".md")

        specify_file = next(
            (f for f in cmd_files if f.name == "agile-specify.md"), None
        )
        assert specify_file is not None
        specify_contents = specify_file.read_text(encoding="utf-8")
        assert "/agile-plan" in specify_contents
        assert "/agile.plan" not in specify_contents

    def test_integration_flag_creates_files(self, tmp_path):
        from typer.testing import CliRunner
        from agile_cli import app

        project = tmp_path / f"int-{self.KEY}"
        project.mkdir()
        old_cwd = os.getcwd()
        try:
            os.chdir(project)
            runner = CliRunner()
            result = runner.invoke(
                app,
                [
                    "init",
                    "--here",
                    "--integration",
                    self.KEY,
                    "--script",
                    "sh",
                    "--ignore-agent-tools",
                ],
                catch_exceptions=False,
            )
        finally:
            os.chdir(old_cwd)
        assert result.exit_code == 0
        i = get_integration(self.KEY)
        cmd_dir = i.commands_dest(project)
        assert cmd_dir.is_dir()
        commands = sorted(cmd_dir.glob("agile-*"))
        assert len(commands) > 0

    def _expected_files(self, script_variant: str) -> list[str]:
        """Override to expect hyphenated agile- prefix."""
        i = get_integration(self.KEY)
        cmd_dir = i.registrar_config["dir"]
        files = []

        # Command files
        for stem in (
            self.COMMANDS_SUBDIR_STEMS
            if hasattr(self, "COMMANDS_SUBDIR_STEMS")
            else self.COMMAND_STEMS
        ):
            files.append(f"{cmd_dir}/agile-{stem.replace('.', '-')}.md")

        # Framework files
        files.append(".agile/integration.json")
        files.append(".agile/init-options.json")
        files.append(f".agile/integrations/{self.KEY}.manifest.json")
        files.append(".agile/integrations/agile.manifest.json")
        files.append(".agile/.gitignore")

        if script_variant == "sh":
            for name in [
                "check-prerequisites.sh",
                "common.sh",
                "create-new-feature.sh",
                "resolve-template.sh",
                "setup-plan.sh",
                "setup-tasks.sh",
            ]:
                files.append(f".agile/scripts/bash/{name}")
        else:
            for name in [
                "check-prerequisites.ps1",
                "common.ps1",
                "create-new-feature.ps1",
                "resolve-template.ps1",
                "setup-plan.ps1",
                "setup-tasks.ps1",
            ]:
                files.append(f".agile/scripts/powershell/{name}")

        for name in [
            "checklist-template.md",
            "constitution-template.md",
            "plan-template.md",
            "spec-template.md",
            "tasks-template.md",
        ]:
            files.append(f".agile/templates/{name}")

        files.append(".agile/memory/.constitution-template.json")
        files.append(".agile/memory/constitution.md")
        # Bundled workflow
        files.append(".agile/workflows/agile/workflow.yml")
        files.append(".agile/workflows/workflow-registry.json")

        return sorted(files)
