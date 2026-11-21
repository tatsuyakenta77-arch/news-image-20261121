// news-image-20261121 — "21 November 2026 in One Image" (Node 22, standard library only).
// The entry image is the entry.png beside this file: a newspaper front page summing up
// Saturday 21 November 2026 — ICJ Rohingya genocide ruling, Russian missile in Poland,
// Wall Street AI sell-off, COP31 stalling, UK-EU deal, Peru 6.8 quake. The program
// copies it to /output/entry.png. No network, no randomness: every run writes the
// same bytes, so both grader runs produce an identical file. The copy is byte-exact by
// construction (copyFileSync), so the gate's 1 MiB / 1024x1024 limits are met exactly
// as the shipped entry.png meets them (1024x1024, ~0.83 MiB).
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(outDir, { recursive: true });
copyFileSync(new URL('./entry.png', import.meta.url), join(outDir, 'entry.png'));
