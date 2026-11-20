// gta6-meme-x-01 v2 — entrypoint.
// Copies POST.json from the repository to /output. That is all it does:
// the house reads the post itself from X.
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";

const botDir = process.env.MAKEFUN_BOT_DIR ?? ".";
const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? "out";

mkdirSync(outputDir, { recursive: true });
const post = readFileSync(join(botDir, "POST.json"), "utf8");

// Validate before copying: POST.json must be a JSON object whose url is
// an X post address, https://x.com/<handle>/status/<digits> (twitter.com
// and /i/web/status/<id> forms are read the same way by the house).
const parsed: unknown = JSON.parse(post);
if (typeof parsed !== "object" || parsed === null || Array.isArray(parsed)) {
  throw new Error("POST.json must be a JSON object");
}
const url = (parsed as Record<string, unknown>).url;
// PLACEHOLDER is the pre-post marker: it is replaced with the real post id
// after the meme is posted to X, and then the digits-only rule applies.
if (
  typeof url !== "string" ||
  !/^https:\/\/(www\.|mobile\.)?(x|twitter)\.com\/[^/]+\/status\/(\d+|PLACEHOLDER)$/.test(url)
) {
  throw new Error("POST.json url is not an X post address: " + String(url));
}

writeFileSync(join(outputDir, "POST.json"), post);
console.log("copied POST.json to " + join(outputDir, "POST.json"));
