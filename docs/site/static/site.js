(function () {
  "use strict";

  var body = document.body;
  var menu = document.querySelector(".menu-toggle");
  var navigation = document.querySelector(".site-navigation");
  var themeButton = document.querySelector("[data-theme-toggle]");
  var logo = document.querySelector(".brand-logo");
  var backToTop = document.querySelector("[data-back-to-top]");

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
    navigation.querySelectorAll("a").forEach(function (link) {
      link.addEventListener("click", function () {
        navigation.classList.remove("is-open");
        menu.setAttribute("aria-expanded", "false");
      });
    });
  }

  var languageSelect = document.querySelector("[data-language-select]");
  if (languageSelect) {
    languageSelect.addEventListener("change", function () {
      if (languageSelect.value) window.location.href = languageSelect.value;
    });
  }

  function updateSearch(value) {
    var query = value.trim().toLocaleLowerCase();
    var searchable = Array.prototype.slice.call(document.querySelectorAll("[data-searchable]"));
    searchable.forEach(function (item) {
      var match = !query || item.getAttribute("data-searchable").toLocaleLowerCase().indexOf(query) !== -1;
      item.hidden = !match;
    });
    var countItems = document.querySelectorAll(".catalog-card");
    if (!countItems.length) countItems = document.querySelectorAll(".docs-nav-link[data-searchable]");
    var visible = Array.prototype.filter.call(countItems, function (item) { return !item.hidden; }).length;
    document.querySelectorAll("[data-search-group]").forEach(function (group) {
      var children = group.querySelectorAll("[data-searchable]");
      var hasMatch = !query || Array.prototype.some.call(children, function (child) { return !child.hidden; });
      group.hidden = !hasMatch;
      if (group.tagName.toLowerCase() === "details") group.open = !query || hasMatch;
    });
    document.querySelectorAll("[data-search-status]").forEach(function (status) {
      status.textContent = query && visible === 0 ? status.getAttribute("data-empty-label") : (query ? String(visible) + " " + status.getAttribute("data-result-label") : status.getAttribute("data-default-label"));
    });
    document.querySelectorAll("[data-skill-search], #global-search").forEach(function (input) {
      if (input.value !== value) input.value = value;
    });
  }

  var searchInputs = document.querySelectorAll("[data-skill-search], #global-search");
  var searchQuery = new URLSearchParams(window.location.search).get("q") || "";
  searchInputs.forEach(function (input) {
    input.addEventListener("input", function () { updateSearch(input.value); });
  });
  if (searchInputs.length && searchQuery) updateSearch(searchQuery);

  document.querySelectorAll('a[href^="#"]').forEach(function (link) {
    link.addEventListener("click", function (event) {
      var target = document.getElementById(link.getAttribute("href").slice(1));
      if (!target) return;
      event.preventDefault();
      target.scrollIntoView({ behavior: "smooth", block: "start" });
      history.replaceState(null, "", link.getAttribute("href"));
    });
  });

  function toggleBackToTop() {
    if (backToTop) backToTop.classList.toggle("is-visible", window.scrollY > 520);
  }
  if (backToTop) {
    window.addEventListener("scroll", toggleBackToTop, { passive: true });
    backToTop.addEventListener("click", function () { window.scrollTo({ top: 0, behavior: "smooth" }); });
    toggleBackToTop();
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
