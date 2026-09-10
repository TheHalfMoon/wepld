// Modified by WePLD on 2026-08-23: deterministic Pictorial rebrand/path integration from the pinned upstream source.
import { afterEach, beforeEach, describe, it } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';

import { stageOpenAIPlugin } from '../scripts/lib/openai-plugin.js';
import { buildCodexPluginHooksManifest } from '../scripts/lib/transformers/hooks.js';

function write(root, rel, contents) {
  const abs = path.join(root, rel);
  fs.mkdirSync(path.dirname(abs), { recursive: true });
  fs.writeFileSync(abs, contents);
}

describe('OpenAI plugin staging', () => {
  let root;
  let dist;

  beforeEach(() => {
    root = fs.mkdtempSync(path.join(os.tmpdir(), 'pictorial-openai-plugin-'));
    dist = path.join(root, 'dist');

    write(root, '.claude-plugin/plugin.json', JSON.stringify({
      name: 'pictorial',
      version: '3.9.1',
      author: {
        name: 'Paul Bakaus',
        email: 'paul@example.com',
      },
      homepage: 'https://github.com/TheHalfMoon/wepld',
      repository: 'https://github.com/TheHalfMoon/wepld',
    }));
    write(root, 'scripts/lib/assets/plugin-icon.png', 'icon');

    write(
      root,
      'dist/codex/.codex/skills/pictorial/SKILL.md',
      '---\nname: pictorial\n---\n\nUse $pictorial. Run .codex/skills/pictorial/scripts/context.mjs.\n',
    );
    write(
      root,
      'dist/codex/.codex/skills/pictorial/agents/openai.yaml',
      'interface:\n  display_name: Pictorial\n',
    );
    write(
      root,
      'dist/codex/.codex/skills/pictorial/agents/pictorial_asset_producer.toml',
      'name = "pictorial_asset_producer"\n',
    );

    // A Claude payload exists too. The OpenAI stage must never read it.
    write(
      root,
      'dist/claude-code/.claude/skills/pictorial/SKILL.md',
      '---\nname: pictorial\n---\n\nUse /pictorial. Run .claude/skills/pictorial/scripts/context.mjs.\n',
    );
  });

  afterEach(() => {
    fs.rmSync(root, { recursive: true, force: true });
  });

  it('packages the Codex skill, agents, manifest, icon, and compatible hook', () => {
    const pluginRoot = stageOpenAIPlugin(root, dist);
    const skill = fs.readFileSync(path.join(pluginRoot, 'skills/pictorial/SKILL.md'), 'utf8');
    const manifest = JSON.parse(fs.readFileSync(path.join(pluginRoot, '.codex-plugin/plugin.json'), 'utf8'));
    const hooks = JSON.parse(fs.readFileSync(path.join(pluginRoot, 'hooks/hooks.json'), 'utf8'));

    assert.match(skill, /\$pictorial/);
    assert.match(skill, /\.codex\/skills\/pictorial/);
    assert.doesNotMatch(skill, /(?:^|[\s`(])\/pictorial\b/m);
    assert.doesNotMatch(skill, /\.claude\/skills\/pictorial/);

    assert.ok(fs.existsSync(path.join(pluginRoot, 'skills/pictorial/agents/openai.yaml')));
    assert.ok(fs.existsSync(path.join(
      pluginRoot,
      'skills/pictorial/agents/pictorial_asset_producer.toml',
    )));
    assert.ok(fs.existsSync(path.join(pluginRoot, 'assets/icon.png')));

    assert.equal(manifest.skills, './skills/');
    assert.deepEqual(manifest.author, {
      name: 'Renaissance Geek Inc',
      url: 'https://github.com/TheHalfMoon/wepld',
    });
    assert.equal('email' in manifest.author, false);
    assert.equal(manifest.interface.shortDescription, 'Design and refine interfaces');
    assert.equal(manifest.interface.category, 'Creativity');
    assert.deepEqual(hooks, buildCodexPluginHooksManifest());
    assert.match(hooks.hooks.PostToolUse[0].hooks[0].command, /\$\{PLUGIN_ROOT\}/);
    assert.doesNotMatch(hooks.hooks.PostToolUse[0].hooks[0].command, /CLAUDE_PLUGIN_ROOT/);
  });
});
