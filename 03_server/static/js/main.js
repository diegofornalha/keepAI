// Ativar tooltips do Bootstrap
document.addEventListener("DOMContentLoaded", function () {
  var tooltipTriggerList = [].slice.call(
    document.querySelectorAll('[data-bs-toggle="tooltip"]')
  );
  var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl);
  });
});

// Fechar alertas automaticamente
document.addEventListener("DOMContentLoaded", function () {
  var alerts = document.querySelectorAll(".alert:not(.alert-permanent)");
  alerts.forEach(function (alert) {
    setTimeout(function () {
      var bsAlert = new bootstrap.Alert(alert);
      bsAlert.close();
    }, 5000);
  });
});

// Adicionar classe active ao link atual
document.addEventListener("DOMContentLoaded", function () {
  var currentLocation = window.location.pathname;
  var navLinks = document.querySelectorAll(".nav-link");

  navLinks.forEach(function (link) {
    if (link.getAttribute("href") === currentLocation) {
      link.classList.add("active");
    }
  });
});

// Animação suave ao scroll
document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
  anchor.addEventListener("click", function (e) {
    e.preventDefault();
    const target = document.querySelector(this.getAttribute("href"));
    if (target) {
      target.scrollIntoView({
        behavior: "smooth",
        block: "start",
      });
    }
  });
});
