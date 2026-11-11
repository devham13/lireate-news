(function () {
  "use strict";
  function hideBroken(img) {
    if (!img || img.dataset.lxImgHidden === "1") return;
    img.dataset.lxImgHidden = "1";
    img.style.display = "none";
    img.removeAttribute("srcset");
    img.setAttribute("aria-hidden", "true");
  }
  function watch(img) {
    if (img.complete && img.naturalWidth === 0) hideBroken(img);
    img.addEventListener("error", function () {
      hideBroken(img);
    });
  }
  document.querySelectorAll("img").forEach(watch);
  if (window.MutationObserver) {
    var obs = new MutationObserver(function (mutations) {
      mutations.forEach(function (m) {
        m.addedNodes.forEach(function (node) {
          if (node.tagName === "IMG") watch(node);
          if (node.querySelectorAll) node.querySelectorAll("img").forEach(watch);
        });
      });
    });
    obs.observe(document.documentElement, { childList: true, subtree: true });
  }
})();
