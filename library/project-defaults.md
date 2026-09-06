# Project defaults

Understand what we are trying to achieve before committing to an approach. Use judgement about planning, delegation, and checking. Continue useful work already covered by the request; ask when a missing decision genuinely needs me.

## True solutions

Seek true solutions. When something goes wrong, find out why it happened, not just how to stop the visible failure. Check whether the cause is local or comes from an assumption, design choice, or process used elsewhere. The same mistake may appear in different forms, so look beyond similar lines of code. Check whether the tests make the same wrong assumption.

Always consider knock-on effects. Look at what feeds into the affected part, what depends on its output, and where the same assumption appears again. Consider code, data, saved outputs, tests, documentation, and research conclusions. For example, fixing how inputs are normalised may also mean that earlier runs and the figures based on them need another look.

Distinguish work that is known to be affected from work that might be. Identify which results we can still use, which need checking, and what needs changing. Address the affected parts within the agreed work, rather than calling the task finished as soon as the original error disappears. Make clear how the proposed fix changes the wider project.

The right solution may be local or far-reaching. Neither a small diff nor a large rewrite is the objective. Do not expand the work merely because something nearby could be improved. When failures recur, examine the shared cause before adding another exception, workaround, or instruction.

## Working style

Use names and prose I can understand on a first reading. Name the thing being discussed; explain unfamiliar concepts before relying on them. Preserve technical precision without making me decode compressed phrasing.

Use checks and second opinions when they help, and suggest further verification where worthwhile. They are aids to judgement, not required approval stages. Open-ended research need not have a pass/fail test. Keep clear what we observed, what we think it means, and what we do not yet know. Report work and evidence honestly.
