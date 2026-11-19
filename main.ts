// gta6-meme-x-01 entry program (Node 22, standard library only).
//
// The entry is the X post itself: this program only hands the grader the
// post's address. It copies POST.json from the repository root into the
// output directory, where the house reads it, fetches the post from X (its
// first picture and its text) and hands that to the judge. Nothing this
// program writes is judged; the meme is the post's picture.
//
// Run it the way the grader does. Outside the grader's container the two
// environment variables stand in for /bot and /output:
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts
// It prints nothing on success. The copy is verified by reading it back:
// a mismatch fails the run, so the two runs the grader does can only write
// the same bytes. The program touches no network, no clock and no file
// outside this repository, so its output is fully deterministic.
//
// NOTE: the POST.json in this repository still holds the placeholder
// address. A follow-up session replaces it with the real post address
// (https://x.com/<handle>/status/<id>) after the meme is posted on X;
// nothing else in this program changes when that happens.

import { copyFileSync, mkdirSync, readFileSync } from "node:fs";
import { join } from "node:path";

const botDir = process.env.MAKEFUN_BOT_DIR ?? "/bot";
const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";

const source = join(botDir, "POST.json");
const target = join(outputDir, "POST.json");

mkdirSync(outputDir, { recursive: true });
try {
  copyFileSync(source, target);
} catch (error) {
  console.error(`could not copy POST.json out of ${botDir}: ${(error as Error).message}`);
  process.exit(1);
}

if (!readFileSync(source).equals(readFileSync(target))) {
  console.error("POST.json copy does not match the repository's POST.json");
  process.exit(1);
}

if (readFileSync(target).length === 0) {
  console.error("POST.json is empty; refusing to hand in an empty post address");
  process.exit(1);
}
