(function () {
  "use strict";

  var body = document.body;
  var menu = document.querySelector(".menu-toggle");
  var navigation = document.querySelector(".site-navigation");
  var themeButton = document.querySelector("[data-theme-toggle]");
  var logo = document.querySelector(".brand-logo");

  function setTheme(theme) {
    body.setAttribute("data-theme", theme);
    if (logo) {
      logo.src = theme === "dark" ? logo.dataset.darkLogo : logo.dataset.lightLogo;
    }
    try { localStorage.setItem("intel-ai-skills-theme", theme); } catch (error) { /* private mode */ }
  }

  var savedTheme = null;
  try { savedTheme = localStorage.getItem("intel-ai-skills-theme"); } catch (error) { /* private mode */ }
  setTheme(savedTheme || "light");

  if (themeButton) {
    themeButton.addEventListener("click", function () {
      setTheme(body.getAttribute("data-theme") === "dark" ? "light" : "dark");
    });
  }

  if (menu && navigation) {
    menu.addEventListener("click", function () {
      var open = navigation.classList.toggle("is-open");
      menu.setAttribute("aria-expanded", String(open));
    });
  }

  document.querySelectorAll("[data-copy]").forEach(function (button) {
    button.addEventListener("click", function () {
      var original = button.textContent;
      var value = button.getAttribute("data-copy");
      if (!navigator.clipboard) return;
      navigator.clipboard.writeText(value).then(function () {
        button.textContent = "Copied";
        window.setTimeout(function () { button.textContent = original; }, 1400);
      });
    });
  });
}());
