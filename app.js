// ViFast — menu di động, cuộn mượt, huy hiệu phiên bản (không thư viện).
(() => {
  'use strict';

  const header = document.querySelector('.site-header');
  const toggle = document.querySelector('.nav-toggle');
  const nav = document.getElementById('site-nav');

  /* ---------- Menu di động ---------- */
  if (header && toggle && nav) {
    const setOpen = (open) => {
      header.classList.toggle('is-open', open);
      nav.classList.toggle('is-open', open);
      toggle.setAttribute('aria-expanded', String(open));
    };

    toggle.addEventListener('click', () => {
      setOpen(toggle.getAttribute('aria-expanded') !== 'true');
    });

    nav.addEventListener('click', (event) => {
      if (event.target instanceof Element && event.target.closest('a')) setOpen(false);
    });

    document.addEventListener('keydown', (event) => {
      if (event.key === 'Escape' && toggle.getAttribute('aria-expanded') === 'true') {
        setOpen(false);
        toggle.focus();
      }
    });
  }

  /* ---------- Cuộn mượt cho liên kết neo ---------- */
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)');

  document.addEventListener('click', (event) => {
    if (!(event.target instanceof Element)) return;

    const link = event.target.closest('a[href^="#"]');
    if (!link || link.classList.contains('skip-link')) return;

    const hash = link.getAttribute('href');
    if (!hash || hash.length < 2) return;

    const section = document.getElementById(hash.slice(1));
    if (!section) return;

    event.preventDefault();
    section.scrollIntoView({
      behavior: reduceMotion.matches ? 'auto' : 'smooth',
      block: 'start',
    });
  });

  /* ---------- Huy hiệu phiên bản từ GitHub ---------- */
  // Nếu API lỗi, bị giới hạn hoặc offline: bỏ qua, huy hiệu vẫn ẩn.
  const repos = ['ViFastKey', 'ViFastTts', 'ViFastOs'];
  const badges = new Map(
    repos.map((repo) => [repo, document.querySelector(`[data-release="${repo}"]`)])
  );

  Promise.allSettled(
    repos.map(async (repo) => {
      const response = await fetch(
        `https://api.github.com/repos/vifast-oss/${repo}/releases/latest`,
        { headers: { Accept: 'application/vnd.github+json' } }
      );
      if (!response.ok) return;

      const data = await response.json();
      const badge = badges.get(repo);
      if (badge && typeof data.tag_name === 'string' && data.tag_name) {
        badge.textContent = data.tag_name;
        badge.hidden = false;
      }
    })
  );
})();
