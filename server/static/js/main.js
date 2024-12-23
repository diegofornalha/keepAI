// Funções de utilidade
function showLoading() {
  const loading = document.createElement("div");
  loading.className = "loading-overlay";
  loading.innerHTML = '<div class="loading"></div>';
  document.body.appendChild(loading);
  setTimeout(() => loading.classList.add("show"), 0);
}

function hideLoading() {
  const loading = document.querySelector(".loading-overlay");
  if (loading) {
    loading.classList.remove("show");
    setTimeout(() => loading.remove(), 300);
  }
}

function showToast(message, type = "success") {
  const toast = document.createElement("div");
  toast.className = `toast align-items-center text-white bg-${type} border-0 fade show`;
  toast.setAttribute("role", "alert");
  toast.setAttribute("aria-live", "assertive");
  toast.setAttribute("aria-atomic", "true");

  toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">${message}</div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
        </div>
    `;

  const container =
    document.querySelector(".toast-container") ||
    (() => {
      const div = document.createElement("div");
      div.className = "toast-container position-fixed top-0 end-0 p-3";
      document.body.appendChild(div);
      return div;
    })();

  container.appendChild(toast);
  new bootstrap.Toast(toast).show();
}

// Funções de tema
function initTheme() {
  const savedTheme = localStorage.getItem("theme") || "light";
  document.documentElement.setAttribute("data-bs-theme", savedTheme);

  const icon = document.querySelector("#theme-toggle i");
  if (icon) {
    icon.className = `fas fa-${savedTheme === "dark" ? "sun" : "moon"}`;
  }
}

// Funções de formulário
function validateForm(form) {
  const inputs = form.querySelectorAll(
    "input[required], select[required], textarea[required]"
  );
  let isValid = true;

  inputs.forEach((input) => {
    if (!input.value.trim()) {
      input.classList.add("is-invalid");
      isValid = false;
    } else {
      input.classList.remove("is-invalid");
    }
  });

  return isValid;
}

// Funções de API
async function apiRequest(endpoint, options = {}) {
  try {
    showLoading();

    const response = await fetch(endpoint, {
      ...options,
      headers: {
        "Content-Type": "application/json",
        ...options.headers,
      },
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error("API Error:", error);
    showToast(error.message || "Ocorreu um erro na requisição", "danger");
    throw error;
  } finally {
    hideLoading();
  }
}

// Inicialização
document.addEventListener("DOMContentLoaded", () => {
  initTheme();

  // Inicializar todos os tooltips
  const tooltips = document.querySelectorAll('[data-bs-toggle="tooltip"]');
  tooltips.forEach((tooltip) => new bootstrap.Tooltip(tooltip));

  // Inicializar todos os popovers
  const popovers = document.querySelectorAll('[data-bs-toggle="popover"]');
  popovers.forEach((popover) => new bootstrap.Popover(popover));

  // Adicionar validação a todos os formulários
  const forms = document.querySelectorAll("form[data-validate]");
  forms.forEach((form) => {
    form.addEventListener("submit", (e) => {
      if (!validateForm(form)) {
        e.preventDefault();
        e.stopPropagation();
      }
    });
  });
});
