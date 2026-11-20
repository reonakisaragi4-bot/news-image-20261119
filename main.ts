// news-image-20261119 — entry program (Node 22, standard library only).
// The poster lives in this repository as entry.png; this program places an
// exact copy of it at <output>/entry.png. Paths come from this file's own
// directory, not the process working directory, because the grader starts
// the program from an arbitrary cwd (it runs `node /bot/main.ts`).
// Local run:  mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { existsSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const folder = dirname(fileURLToPath(import.meta.url));
const targetDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const poster = resolve(folder, 'entry.png');
const target = resolve(targetDir, 'entry.png');

if (!existsSync(poster)) {
  throw new Error(`poster missing: ${poster}`);
}
mkdirSync(targetDir, { recursive: true });
const bytes = readFileSync(poster);
// Fail fast when the poster breaks the gate (at most 1 MiB): a too-big
// file is refused outright, so catching it here beats a rejected entry.
if (bytes.length > 1048576) {
  throw new Error(`entry.png is ${bytes.length} bytes, over the 1 MiB gate`);
}
writeFileSync(target, bytes);
const written = readFileSync(target);
if (!written.equals(bytes)) {
  throw new Error(`entry.png mismatch after write: ${written.length} != ${bytes.length}`);
}
console.log(`entry.png -> ${target} (${bytes.length} bytes)`);
