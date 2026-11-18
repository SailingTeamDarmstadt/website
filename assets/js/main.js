// Mobile navigation
document.addEventListener("DOMContentLoaded", () => {
  const toggle = document.querySelector(".nav-toggle");
  const nav = document.getElementById("main-nav");
  if (toggle && nav) {
    toggle.addEventListener("click", () => {
      const open = toggle.getAttribute("aria-expanded") === "true";
      toggle.setAttribute("aria-expanded", String(!open));
      document.body.classList.toggle("nav-open", !open);
    });
  }

  // Header gets a solid background once the page is scrolled
  const header = document.querySelector(".site-header");
  const onScroll = () => header.classList.toggle("scrolled", window.scrollY > 10);
  onScroll();
  window.addEventListener("scroll", onScroll, { passive: true });

  // Portrait images in posts are centered instead of stretched to full width
  const markPortrait = (img) => img.classList.toggle("is-portrait", img.naturalHeight > img.naturalWidth);
  document.querySelectorAll(".post .prose img").forEach((img) => {
    if (img.complete && img.naturalWidth) markPortrait(img);
    else img.addEventListener("load", () => markPortrait(img), { once: true });
  });

  // Privacy-friendly YouTube embeds: nothing is loaded from YouTube until clicked
  document.querySelectorAll(".video[data-youtube]").forEach((el) => {
    const id = el.dataset.youtube;
    if (el.dataset.thumb) el.style.backgroundImage = "url('" + el.dataset.thumb + "')";
    el.innerHTML =
      '<button type="button" class="video-consent">' +
      '<span class="video-play" aria-hidden="true"></span>' +
      "<span>Video abspielen</span>" +
      "<small>Beim Abspielen werden Daten an YouTube übertragen.</small>" +
      "</button>";
    el.querySelector("button").addEventListener("click", () => {
      el.innerHTML =
        '<iframe src="https://www.youtube-nocookie.com/embed/' + encodeURIComponent(id) +
        '?autoplay=1" title="YouTube-Video" allow="autoplay; encrypted-media; picture-in-picture" allowfullscreen></iframe>';
    });
  });

  // Simple lightbox for gallery links
  const box = document.createElement("dialog");
  box.className = "lightbox";
  box.innerHTML = '<button type="button" aria-label="Schließen">×</button><img alt="">';
  document.body.appendChild(box);
  box.addEventListener("click", () => box.close());
  document.querySelectorAll(".gallery a[href], .boat-main-image").forEach((a) => {
    a.addEventListener("click", (e) => {
      e.preventDefault();
      box.querySelector("img").src = a.href;
      box.showModal();
    });
  });

  // Boat page: thumbnails switch the main image
  const main = document.querySelector(".boat-main-image");
  document.querySelectorAll(".boat-thumb").forEach((btn) => {
    btn.addEventListener("click", () => {
      main.href = btn.dataset.src;
      main.querySelector("img").src = btn.dataset.src;
      document.querySelectorAll(".boat-thumb").forEach((b) => b.classList.toggle("is-active", b === btn));
    });
  });
});
