// Utility Functions
const debounce = (func, wait) => {
  let timeout;
  return (...args) => {
    clearTimeout(timeout);
    timeout = setTimeout(() => func(...args), wait);
  };
};

// Toast Notifications
const Toast = {
  show(message, type = "info") {
    const toastContainer = document.querySelector(".toast-container");
    const toast = document.createElement("div");
    toast.className = `toast align-items-center text-white bg-${type}`;
    toast.innerHTML = `
            <div class="d-flex">
                <div class="toast-body">${message}</div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        `;
    toastContainer.appendChild(toast);
    const bsToast = new bootstrap.Toast(toast);
    bsToast.show();
    toast.addEventListener("hidden.bs.toast", () => toast.remove());
  },
};

// App Initialization
const App = {
  init() {
    this.setupEventListeners();
    this.setupTheme();
  },

  setupEventListeners() {
    // Sidebar Toggle
    document.querySelector(".sidebar-toggle")?.addEventListener("click", () => {
      document.body.classList.toggle("sidebar-open");
    });

    // Form Validation
    document.querySelectorAll("form").forEach((form) => {
      form.addEventListener("submit", this.handleFormSubmit);
    });
  },

  setupTheme() {
    const theme = localStorage.getItem("theme") || "light";
    document.body.setAttribute("data-theme", theme);
  },

  handleFormSubmit(e) {
    if (!this.checkValidity()) {
      e.preventDefault();
      e.stopPropagation();
    }
    this.classList.add("was-validated");
  },
};

// Initialize when DOM is ready
document.addEventListener("DOMContentLoaded", () => App.init());
