const fs = require("fs");
const path = require("path");
const axios = require("axios");
const sharp = require("sharp");

const OUTPUT_DIR = path.join(__dirname, "../output");

async function downloadImage(url, filename) {
  const response = await axios({
    url,
    responseType: "arraybuffer",
    method: "GET"
  });
  fs.writeFileSync(filename, response.data);
}

async function processImages(input) {
  const { productId, productName, imageUrls } = input;

  const productOutputDir = path.join(OUTPUT_DIR, productId);
  if (!fs.existsSync(productOutputDir)) {
    fs.mkdirSync(productOutputDir, { recursive: true });
  }

  const processedImages = [];

  for (let i = 0; i < imageUrls.length; i++) {
    if (!imageUrls[i]) continue;

    const imgPath = path.join(productOutputDir, `img${i + 1}.jpg`);
    await downloadImage(imageUrls[i], imgPath);

    const resizedPath = path.join(productOutputDir, `img${i + 1}_1080.jpg`);
    await sharp(imgPath)
      .resize(1080, 1080, { fit: "cover" })
      .jpeg({ quality: 90 })
      .toFile(resizedPath);

    processedImages.push(resizedPath);
  }

  console.log("Processed images saved at:", productOutputDir);
  return processedImages;
}

// ------- Run if triggered directly -------
if (require.main === module) {
  const input = JSON.parse(process.argv[2]);
  processImages(input).then(() => {
    console.log("Done image processing");
  });
}

module.exports = processImages;
