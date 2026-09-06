# Research prompt library

Eight short snippets for research with Claude Code and Codex. Copy what is useful, change it for the task, and leave the rest. There is no installation, plugin, or required sequence.

**Recommended use:** keep project defaults and writing preferences in your research project's instruction file. Paste the other snippets into the conversation when you need them. Use skills later only if they save you repeated copying.

## Set up a research project once

Add [project-defaults.md](library/project-defaults.md) and [writing.md](library/writing.md) to the project's **`AGENTS.md`**. Merge them with any useful instructions already there, rather than replacing project-specific knowledge. Add this line to the adjacent **`CLAUDE.md`**:

```text
@AGENTS.md
```

Codex reads `AGENTS.md`; Claude Code reads `CLAUDE.md` and imports `AGENTS.md` through that line. You maintain one copy of the shared preferences. This is a supported pattern, not a plugin. See the official [Claude instructions](https://code.claude.com/docs/en/memory#agentsmd) and [Codex instructions](https://developers.openai.com/codex/guides/agents-md).

Pasting the same preferences into both files also works. Keep the copies in step, and do not add an import on top of an identical copy. Start a fresh session after changing persistent instructions, or ask the current agent to read the changes.

These files belong in **the project you are working on**, not just in this toolkit repository. This repository stores the snippets; it does not automatically apply them elsewhere. Project defaults are useful on every task. The fuller writing passage is worth keeping because readable explanations are a standing preference, not just a report requirement.

## Paste a snippet for the current task

Open a file below, copy its contents, and add the actual request. The snippets do not need one another or a local checkout of this repository. There is no need to tell the agent to read a library path.

| Snippet | When to use it |
| --- | --- |
| [Project defaults](library/project-defaults.md) | Persistent guidance: true solutions, knock-on effects, clear explanations, and judgement about checks. |
| [Writing](library/writing.md) | Persistent writing preferences, or a one-off pass on a difficult explanation. |
| [Research](library/research.md) | Investigating a question, comparing explanations, and choosing useful experiments. |
| [Second opinion](library/second-opinion.md) | Asking the other model family to inspect the work or take a fresh approach. |
| [Overnight work](library/overnight.md) | Continuing agreed work while you are away, handling runs, and keeping track of unfinished work. |
| [Morning report](library/morning-report.md) | A self-contained HTML account with explanations, figures, light/dark themes, and no appendix. |
| [Notebook](library/notebook.md) | An analysis notebook that explains the question, calculations, and results together. |
| [Sonnet writing](library/sonnet-writing.md) | A temporary request for Sonnet to write or edit this piece. Keep it out of permanent defaults. |

For example, paste **morning-report.md**, then add:

> Explain what we learned from the runs since yesterday. I particularly want to understand why the two methods behaved differently. Use the results we already have; identify anything that is still running.

Before leaving work overnight, you might paste **overnight.md** and **morning-report.md**, then describe the work to continue and ask for the report at the end. The report snippet already includes basic writing and figure guidance. There is no need to paste the writing file again when the project instructions contain it.

For a second opinion, paste **second-opinion.md** and name the question to examine. Give the lead agent room to decide what to do with the response. The snippet asks for a real call using tools already available, or a brief you can paste into the other tool. It does not install or authenticate either CLI. Likewise, the overnight snippet guides an agent that is already working; it does not schedule a future session or keep a closed application running.

Pasted text applies to the conversation where you supply it. On a fresh start or handover, include whichever task instructions still matter. Do not assume a new reviewer has seen the lead agent's conversation.

## When skills would help

A skill packages a reusable set of instructions so you can invoke it by name. Both hosts can load skill instructions on demand instead of keeping the full text in every session. Claude Code uses `/skill-name`; Codex CLI supports `$skill-name` or selection through `/skills`. See [Claude skills](https://code.claude.com/docs/en/skills) and [Codex skills](https://developers.openai.com/codex/skills).

For this library, start with copy/paste. It is easy to adjust and needs no setup. A manually selected **morning report** or **second opinion** skill would be a reasonable convenience once you find yourself using the same passage repeatedly. Packaging does not establish that a review is correct or supply access to another model. No skill files or exporters are included here.

Keep only the guidance that continues to help. A recurring failure is a reason to investigate its cause, not automatically another paragraph to add to the instructions.

Usage documentation checked on 6 September 2026.
