// src/utils/file/file.util.ts

export function getFileExtension(
  filename: string
) {
  return filename.split(".").pop() ?? "";
}

export function bytesToMB(bytes: number) {
  return (
    bytes / (1024 * 1024)
  ).toFixed(2);
}