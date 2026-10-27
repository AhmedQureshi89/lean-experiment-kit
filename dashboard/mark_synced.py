#!/usr/bin/env python3
"""Records that the live dashboard now matches experiments/. Run only after the ArtifactData batch succeeded."""
import datetime, pathlib
stamp = pathlib.Path(__file__).resolve().parent / '.last-sync'
stamp.write_text(datetime.datetime.now().isoformat(timespec='seconds'), encoding='utf-8')
print('dashboard sync recorded at', stamp.read_text(encoding='utf-8'))
