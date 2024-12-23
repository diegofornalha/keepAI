// Utility Functions
const debounce = (func, wait) => {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
};

// Toast Notifications
class Toast {
  static show(message, type = "info", duration = 3000) {
    const toastContainer = document.querySelector(".toast-container");
    const toast = document.createElement("div");
    toast.className = `toast align-items-center text-white bg-${type}`;
    toast.setAttribute("role", "alert");
    toast.innerHTML = `
            <div class="d-flex">
                <div class="toast-body">
                    <i class="bi ${this.getIcon(type)} me-2"></i>
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        `;
    toastContainer.appendChild(toast);
    const bsToast = new bootstrap.Toast(toast, { delay: duration });
    bsToast.show();
    toast.addEventListener("hidden.bs.toast", () => toast.remove());
  }

  static getIcon(type) {
    const icons = {
      success: "bi-check-circle",
      error: "bi-exclamation-circle",
      warning: "bi-exclamation-triangle",
      info: "bi-info-circle",
    };
    return icons[type] || icons.info;
  }
}

// Loading State
class LoadingState {
  static show() {
    document.querySelector(".loading-overlay").classList.add("show");
  }

  static hide() {
    document.querySelector(".loading-overlay").classList.remove("show");
  }
}

// Form Validation
class FormValidation {
  static init(form) {
    form.addEventListener("submit", (e) => {
      if (!form.checkValidity()) {
        e.preventDefault();
        e.stopPropagation();
      }
      form.classList.add("was-validated");
    });
  }

  static validateField(input, validationFn) {
    const value = input.value;
    const isValid = validationFn(value);

    if (isValid) {
      input.classList.remove("is-invalid");
      input.classList.add("is-valid");
    } else {
      input.classList.remove("is-valid");
      input.classList.add("is-invalid");
    }

    return isValid;
  }
}

// API Requests
class API {
  static async request(url, options = {}) {
    try {
      LoadingState.show();
      const response = await fetch(url, {
        ...options,
        headers: {
          "Content-Type": "application/json",
          ...options.headers,
        },
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.message || "Erro na requisição");
      }

      return data;
    } catch (error) {
      Toast.show(error.message, "error");
      throw error;
    } finally {
      LoadingState.hide();
    }
  }
}

// Markdown Support
class MarkdownRenderer {
  static render(content) {
    if (typeof marked === "undefined") return content;
    return marked.parse(content);
  }
}

// Mobile Navigation
class MobileNav {
  static init() {
    const toggle = document.querySelector(".sidebar-toggle");
    if (!toggle) return;

    toggle.addEventListener("click", () => {
      document.body.classList.toggle("sidebar-open");
    });

    document.addEventListener("click", (e) => {
      if (
        document.body.classList.contains("sidebar-open") &&
        !e.target.closest(".sidebar") &&
        !e.target.closest(".sidebar-toggle")
      ) {
        document.body.classList.remove("sidebar-open");
      }
    });
  }
}

// Theme Support
class ThemeManager {
  static init() {
    const theme = localStorage.getItem("theme") || "light";
    this.setTheme(theme);

    const themeToggle = document.querySelector(".theme-toggle");
    if (themeToggle) {
      themeToggle.addEventListener("click", () => {
        const newTheme = document.body.classList.contains("dark-theme")
          ? "light"
          : "dark";
        this.setTheme(newTheme);
      });
    }
  }

  static setTheme(theme) {
    if (theme === "dark") {
      document.body.classList.add("dark-theme");
    } else {
      document.body.classList.remove("dark-theme");
    }
    localStorage.setItem("theme", theme);
  }
}

// Initialize
document.addEventListener("DOMContentLoaded", () => {
  MobileNav.init();
  ThemeManager.init();

  // Initialize all forms with validation
  document.querySelectorAll("form").forEach((form) => {
    FormValidation.init(form);
  });

  // Initialize all tooltips
  const tooltipTriggerList = [].slice.call(
    document.querySelectorAll('[data-bs-toggle="tooltip"]')
  );
  tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl);
  });
});
