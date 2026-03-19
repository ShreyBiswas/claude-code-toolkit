---
name: presenter
description: Format proposals as themed groups, present for review, apply accepted changes
---

# Presenter

Format and present the proposals from Phase 3 for user review.

## Grouping

1. Group proposals by theme
2. Order themes by impact (most significant configuration gap first)
3. Within each theme, show **removals before additions** (clean up before adding)

## Presentation format

For each theme group, present:

```
## Theme: [descriptive name]
[1-2 sentence summary of what changed and why it matters for config]

### Proposed changes:

1. **[target file]** — [add/update/remove]
   [diff or description of the change]
   _Reason: [evidence from the delta]_

2. **[target file]** — [add/update/remove]
   ...

Accept this group? [y/n/edit]
```

Wait for the user's response before moving to the next group.

## Handling responses

- **y (accept)**: Mark all proposals in the group as accepted
- **n (reject)**: Discard all proposals in the group. The baseline still advances (the user saw them and chose not to act)
- **edit**: Present each proposal individually and let the user modify the proposed text before accepting. Show the proposal, ask for edits, then confirm

## Applying changes

After all groups have been reviewed:

1. Apply all accepted changes to their target files
2. For additions: append to the appropriate section of the target file, or create the file if it doesn't exist
3. For updates: replace the old content with the new content
4. For removals: delete the specified content (or the entire file if removing the whole thing)
5. Show each file write before executing it — use the Edit tool so the user can see the diff

## Output

Return to the orchestrator:
- Count of changes applied
- Count of files modified
- Count of stale entries removed
