function matrixRainInit() {
  const canvas = document.getElementById("matrix-rain");
  if (!canvas) return; // Prevent errors if canvas is missing
  const ctx = canvas.getContext("2d");
  let width = window.innerWidth;
  let height = window.innerHeight;
  canvas.width = width;
  canvas.height = height;

  const fontSize = 18;
  const columns = Math.floor(width / fontSize);
  const letters = Array.from({ length: columns }, () => 1);
  const chars =
    "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";

  function rainbowColor(y) {
    return `hsl(${(y / height) * 360}, 100%, 50%)`;
  }

  let frame = 0;
  const slowFactor = 3; // Increase this number to slow down more

  function draw() {
    ctx.fillStyle = "rgba(0,0,0,0.15)";
    ctx.fillRect(0, 0, width, height);

    ctx.font = `${fontSize}px monospace`;
    for (let i = 0; i < columns; i += 1) {
      const text = chars[Math.floor(Math.random() * chars.length)];
      const x = i * fontSize;
      const y = letters[i] * fontSize;

      ctx.fillStyle = rainbowColor(y);
      ctx.fillText(text, x, y);

      // Only update the letter position every 'slowFactor' frames
      if (frame % slowFactor === 0) {
        if (y > height && Math.random() > 0.975) {
          letters[i] = 0;
        } else {
          letters[i] += 1;
        }
      }
    }
  }

  function animate() {
    frame++;
    draw();
    requestAnimationFrame(animate);
  }

  animate();

  window.addEventListener("resize", () => {
    width = window.innerWidth;
    height = window.innerHeight;
    canvas.width = width;
    canvas.height = height;
  });
}

document.addEventListener("DOMContentLoaded", matrixRainInit);