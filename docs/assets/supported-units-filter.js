(function () {
  function ready(callback) {
    if (document.readyState === "loading") {
      document.addEventListener("DOMContentLoaded", callback);
      return;
    }
    callback();
  }

  function updateUrl(value) {
    if (!window.history || !window.history.replaceState) {
      return;
    }
    if (value === "__all__") {
      window.history.replaceState(null, "", window.location.pathname);
      return;
    }
    window.history.replaceState(null, "", "#" + encodeURIComponent(value));
  }

  ready(function () {
    var select = document.getElementById("unit-category-filter");
    var count = document.getElementById("unit-filter-count");
    var sections = Array.prototype.slice.call(
      document.querySelectorAll(".unit-category")
    );

    if (!select || sections.length === 0) {
      return;
    }

    var initialCategory = decodeURIComponent(window.location.hash.slice(1));
    if (
      initialCategory &&
      sections.some(function (section) {
        return section.dataset.category === initialCategory;
      })
    ) {
      select.value = initialCategory;
    }

    function applyFilter() {
      var selected = select.value;
      var visibleSections = 0;
      var visibleUnits = 0;
      var selectedName = "";

      sections.forEach(function (section) {
        var show = selected === "__all__" || section.dataset.category === selected;
        section.hidden = !show;
        if (show) {
          visibleSections += 1;
          visibleUnits += Number(section.dataset.unitCount || 0);
          selectedName = section.dataset.categoryName || "";
        }
      });

      if (count) {
        if (selected === "__all__") {
          count.textContent = "Showing all " + visibleSections + " categories.";
        } else {
          count.textContent =
            "Showing " + visibleUnits + " units in " + selectedName + ".";
        }
      }

      updateUrl(selected);
    }

    select.addEventListener("change", applyFilter);
    applyFilter();
  });
})();
