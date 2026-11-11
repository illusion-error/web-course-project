(() => {
  // Desktop pointer only; touch devices keep the native cursor.
  if (!window.matchMedia('(pointer: fine)').matches) return;

  const script = document.currentScript;
  const base = script.src.replace(/\/js\/[^/]+$/, '/');

  const img = new Image();
  img.id = 'cat-cursor';
  img.alt = '';
  img.src = base + 'icons/cat-cursor.png';

  let tx = -100, ty = -100, x = -100, y = -100;
  let visible = false, raf = null;

  function loop() {
    x += (tx - x) * 0.2;
    y += (ty - y) * 0.2;
    img.style.transform = `translate3d(${x - 36}px, ${y - 22}px, 0)`;
    raf = requestAnimationFrame(loop);
  }

  function mount() {
    document.body.appendChild(img);
    document.body.classList.add('has-cat-cursor');
  }

  if (document.body) mount();
  else document.addEventListener('DOMContentLoaded', mount);

  window.addEventListener('mousemove', (e) => {
    tx = e.clientX;
    ty = e.clientY;
    if (!visible) {
      visible = true;
      x = tx; y = ty;
      img.style.opacity = '1';
    }
    if (!raf) loop();
  });

  document.addEventListener('mouseleave', () => {
    visible = false;
    img.style.opacity = '0';
  });
  document.addEventListener('mouseenter', () => {
    visible = true;
    img.style.opacity = '1';
  });

  const hoverSel = 'a, button, [role="button"]';
  document.addEventListener('mouseover', (e) => {
    if (e.target.closest && e.target.closest(hoverSel)) img.classList.add('is-hover');
  });
  document.addEventListener('mouseout', (e) => {
    if (e.target.closest && e.target.closest(hoverSel)) img.classList.remove('is-hover');
  });
})();
