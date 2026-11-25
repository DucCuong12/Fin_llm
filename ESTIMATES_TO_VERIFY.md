# November 25 verification status

The previous provisional cells and prose were replaced with results computed from cached price panels, event labels, and agent positions. The latest manuscript reports point estimates and omits confidence intervals. The replay retains its full numerical output for audit.

From the repository root, run:

    python multi_agent_desk/reproduce_voltilt_paper.py > voltilt_results.json
    python multi_agent_desk/write_voltilt_paper_tables.py voltilt_results.json

The published table source is reproduced by the two scripts. The replay used for this revision is archived in multi_agent_desk/reports4/voltilt_paper_nov25.json. Earlier draft markup and assumptions are backed up in the revision workspace.

The primary results use the observed-leg return and multiplier-cost proxy described in the paper. The drift-aware execution check uses the complete W1 panel only. A new post-cutoff news sample with reliable publication timestamps, a standalone sentiment classifier, and drift-aware accounting for missing or exiting holdings are outside the replay.
