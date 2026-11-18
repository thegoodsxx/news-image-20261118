import { existsSync, readFileSync, writeFileSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

function deliverPoster(): void {
  const currentDir = dirname(fileURLToPath(import.meta.url));
  const sourcePath = resolve(currentDir, 'entry.png');
  const targetDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
  const targetPath = resolve(targetDir, 'entry.png');

  if (!existsSync(sourcePath)) {
    throw new Error(`Source poster not found at ${sourcePath}`);
  }

  const posterBytes = readFileSync(sourcePath);
  writeFileSync(targetPath, posterBytes);

  console.log(`Wrote ${posterBytes.byteLength} bytes to ${targetPath}`);
}

deliverPoster();
