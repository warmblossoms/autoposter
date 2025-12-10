const fs = require("fs");
const path = require("path");
const ffmpeg = require("fluent-ffmpeg");

const OUTPUT_DIR = path.join(__dirname, "../output");

async function createReel(productId, imagePaths) {
  const productOutputDir = path.join(OUTPUT_DIR, productId);
  if (!fs.existsSync(productOutputDir)) {
    fs.mkdirSync(productOutputDir, { recursive: true });
  }

  const reelPath = path.join(productOutputDir, "reel.mp4");

  return new Promise((resolve, reject) => {
    let cmd = ffmpeg();

    imagePaths.forEach(img => {
      cmd = cmd.input(img);
    });

    cmd
      .outputOptions([
        "-vf scale=1080:1920,format=yuv420p",
        "-r 30"
      ])
      .on("end", () => {
        console.log("Reel created:", reelPath);
        resolve(reelPath);
      })
      .on("error", (err) => {
        reject(err);
      })
      .save(reelPath);
  });
}

// Run standalone
if (require.main === module) {
  const { productId, images } = JSON.parse(process.argv[2]);
  createReel(productId, images).then(() => {
    console.log("Reel generation done");
  });
}

module.exports = createReel;
