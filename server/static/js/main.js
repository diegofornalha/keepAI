// Utilitários
const formatDate = (date) => {
  return new Intl.DateTimeFormat("pt-BR", {
    year: "numeric",
    month: "long",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  }).format(new Date(date));
};

const formatDateShort = (date) => {
  return new Intl.DateTimeFormat("pt-BR", {
    day: "2-digit",
    month: "2-digit",
    year: "2-digit",
  }).format(new Date(date));
};

const formatCurrency = (value) => {
  return new Intl.NumberFormat("pt-BR", {
    style: "currency",
    currency: "BRL",
  }).format(value);
};

// API Helpers
const api = {
  async get(endpoint) {
    try {
      const response = await fetch(endpoint);
      if (!response.ok) throw new Error("Erro na requisição");
      return await response.json();
    } catch (error) {
      console.error("Erro na requisição GET:", error);
      throw error;
    }
  },

  async post(endpoint, data) {
    try {
      const response = await fetch(endpoint, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      });
      if (!response.ok) throw new Error("Erro na requisição");
      return await response.json();
    } catch (error) {
      console.error("Erro na requisição POST:", error);
      throw error;
    }
  },

  async put(endpoint, data) {
    try {
      const response = await fetch(endpoint, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      });
      if (!response.ok) throw new Error("Erro na requisição");
      return await response.json();
    } catch (error) {
      console.error("Erro na requisição PUT:", error);
      throw error;
    }
  },

  async delete(endpoint) {
    try {
      const response = await fetch(endpoint, {
        method: "DELETE",
      });
      if (!response.ok) throw new Error("Erro na requisição");
      return await response.json();
    } catch (error) {
      console.error("Erro na requisição DELETE:", error);
      throw error;
    }
  },
};

// Markdown Helper
const md = {
  parse(text) {
    return marked.parse(text, {
      breaks: true,
      gfm: true,
    });
  },

  sanitize(html) {
    const temp = document.createElement("div");
    temp.innerHTML = html;
    return temp.textContent || temp.innerText;
  },
};

// Storage Helper
const storage = {
  get(key) {
    try {
      const item = localStorage.getItem(key);
      return item ? JSON.parse(item) : null;
    } catch (error) {
      console.error("Erro ao ler do localStorage:", error);
      return null;
    }
  },

  set(key, value) {
    try {
      localStorage.setItem(key, JSON.stringify(value));
      return true;
    } catch (error) {
      console.error("Erro ao salvar no localStorage:", error);
      return false;
    }
  },

  remove(key) {
    try {
      localStorage.removeItem(key);
      return true;
    } catch (error) {
      console.error("Erro ao remover do localStorage:", error);
      return false;
    }
  },
};

// Theme Helper
const theme = {
  init() {
    const savedTheme = storage.get("theme") || "light";
    this.set(savedTheme);

    // Observar mudanças no sistema
    window.matchMedia("(prefers-color-scheme: dark)").addListener((e) => {
      if (!storage.get("theme")) {
        this.set(e.matches ? "dark" : "light");
      }
    });
  },

  set(mode) {
    if (mode === "dark") {
      document.documentElement.classList.add("dark");
    } else {
      document.documentElement.classList.remove("dark");
    }
    storage.set("theme", mode);
  },

  toggle() {
    const current = storage.get("theme") || "light";
    this.set(current === "light" ? "dark" : "light");
  },
};

// Notification Helper
const notify = {
  permission: false,

  async init() {
    if ("Notification" in window) {
      const permission = await Notification.requestPermission();
      this.permission = permission === "granted";
    }
  },

  async show(title, options = {}) {
    if (!this.permission) return;

    try {
      const notification = new Notification(title, {
        icon: "/static/img/favicon.png",
        ...options,
      });

      notification.onclick = function () {
        window.focus();
        this.close();
      };
    } catch (error) {
      console.error("Erro ao mostrar notificação:", error);
    }
  },
};

// Form Helper
const form = {
  serialize(formElement) {
    const formData = new FormData(formElement);
    const data = {};

    for (let [key, value] of formData.entries()) {
      if (data[key]) {
        if (!Array.isArray(data[key])) {
          data[key] = [data[key]];
        }
        data[key].push(value);
      } else {
        data[key] = value;
      }
    }

    return data;
  },

  validate(formElement) {
    const inputs = formElement.querySelectorAll("input, select, textarea");
    let isValid = true;

    inputs.forEach((input) => {
      if (input.hasAttribute("required") && !input.value.trim()) {
        input.classList.add("is-invalid");
        isValid = false;
      } else {
        input.classList.remove("is-invalid");
      }
    });

    return isValid;
  },

  clear(formElement) {
    formElement.reset();
    formElement.querySelectorAll(".is-invalid").forEach((input) => {
      input.classList.remove("is-invalid");
    });
  },
};

// Inicialização
document.addEventListener("DOMContentLoaded", () => {
  theme.init();
  notify.init();
});

// Exportar helpers
window.app = {
  api,
  md,
  storage,
  theme,
  notify,
  form,
  formatDate,
  formatDateShort,
  formatCurrency,
};
