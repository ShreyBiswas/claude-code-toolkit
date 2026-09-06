# Research notebook

Build a notebook that explains the question and lets me inspect the analysis, rather than showing an unedited sequence of commands. Put the question and brief outcome first, then introduce the ideas needed to understand the method and results.

Before a substantial computation, explain what it will tell us and why we are doing it. After it, explain what the output means. Name the comparison and describe what changed; do not rely on abbreviated technical labels to carry the explanation. Keep results, caveats, and the relevant code together rather than sending important details to an appendix.

Use clear names and figures that show useful variation without crowding. Distinguish measured outputs from illustrative examples. Make it possible to trace a displayed result to its inputs and calculations.

Reuse project functions where helpful rather than copying large chunks of code. Keep execution order and dependencies clear, avoid hidden state, and separate loading existing results from launching expensive work. Do not silently rerun experiments for presentation.

Check or execute the notebook where useful and feasible. Identify saved outputs that have not been recomputed, cells that have not run, and partial or failed results. An exploratory notebook does not need to become a production pipeline or pass an invented acceptance test.
