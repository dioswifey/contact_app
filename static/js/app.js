// app.js — 화면 동작: fetch 호출 · DOM 갱신
// 워크플로우: ① me 확인 → ② 로그인/관리 섹션 전환 → ③ categories → ④ contacts → ⑤ 이벤트 연결

const authModal = document.getElementById("auth-modal");
const authSection = document.getElementById("auth-section");
const manageSection = document.getElementById("manage-section");
const userBox = document.getElementById("user-box");
const usernameLabel = document.getElementById("username-label");
const page = document.querySelector(".page");
const topbar = document.querySelector(".topbar");

const loginForm = document.getElementById("login-form");
const loginBtn = document.getElementById("login-btn");
const signupBtn = document.getElementById("signup-btn");
const authMessage = document.getElementById("auth-message");
const logoutBtn = document.getElementById("logout-btn");

const categoryList = document.getElementById("category-list");
const categoryForm = document.getElementById("category-form");
const categorySelect = document.getElementById("category-select");

const contactForm = document.getElementById("contact-form");
const contactFormTitle = document.getElementById("contact-form-title");
const contactSubmitBtn = document.getElementById("contact-submit-btn");
const contactCancelBtn = document.getElementById("contact-cancel-btn");

const searchInput = document.getElementById("search-input");
const searchBtn = document.getElementById("search-btn");
const contactCount = document.getElementById("contact-count");
const contactListEl = document.getElementById("contact-list");
const emptyState = document.getElementById("empty-state");

const messageBar = document.getElementById("toast");
const messageBarText = document.getElementById("message-bar-text");

let editingContactId = null; // null = 추가 모드

// ── SCR-900 Common message bar ─────────────────────────────
function showMessage(text, kind = "info") {
  messageBar.hidden = false;
  messageBarText.textContent = text;
  messageBar.classList.remove("is-success", "is-error", "is-info");
  messageBar.classList.add(kind === "error" ? "is-error" : kind === "success" ? "is-success" : "is-info");
  clearTimeout(showMessage._t);
  showMessage._t = setTimeout(() => {
    messageBar.hidden = true;
    messageBarText.textContent = "Common notification area — Success/Error messages will appear here";
    messageBar.classList.remove("is-success", "is-error", "is-info");
  }, 3200);
}

// ── 공통 API 호출 ──────────────────────────────────────
async function api(path, options = {}) {
  const res = await fetch(path, {
    headers: { "Content-Type": "application/json" },
    credentials: "same-origin",
    ...options,
  });

  if (res.status === 204) return null;

  let body = null;
  try { body = await res.json(); } catch (_) { /* 본문 없음 */ }

  if (!res.ok) {
    if (res.status === 401) {
      showAuthSection();
      showMessage("Session expired. Please log in again.", "error");
    } else {
      showMessage(extractDetail(body), "error");
    }
    throw new Error(body ? extractDetail(body) : `HTTP ${res.status}`);
  }
  return body;
}

function extractDetail(body) {
  if (!body) return "Failed to process request.";
  if (Array.isArray(body.detail)) return body.detail[0]?.msg || "Please check your input.";
  return body.detail || "Failed to process request.";
}

function escapeHtml(str) {
  const div = document.createElement("div");
  div.textContent = str ?? "";
  return div.innerHTML;
}

// ── 화면 전환 ──────────────────────────────────────────
function showAuthSection() {
  authModal.classList.remove("auth-modal--hidden");
  authModal.classList.add("auth-modal--active");
  userBox.hidden = true;
  page.setAttribute("data-auth", "false");
  topbar.setAttribute("data-auth", "false");
}

function showManageSection(user) {
  usernameLabel.textContent = user.username;
  userBox.hidden = false;
  page.setAttribute("data-auth", "true");
  topbar.setAttribute("data-auth", "true");
  setTimeout(() => {
    authModal.classList.add("auth-modal--hidden");
    authModal.classList.remove("auth-modal--active");
  }, 100);
}

// ── 부트스트랩 ────────────────────────────────────────
async function bootstrap() {
  try {
    const user = await api("/auth/me");
    showManageSection(user);
    await loadCategories();
    await loadContacts();
  } catch (_) {
    showAuthSection();
  }
}

// ── 로그인 / 회원가입 / 로그아웃 ───────────────────────
loginForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  const data = Object.fromEntries(new FormData(loginForm));
  loginBtn.disabled = true;
  try {
    const user = await api("/auth/login", { method: "POST", body: JSON.stringify(data) });
    authMessage.textContent = "";
    showManageSection(user);
    await loadCategories();
    await loadContacts();
  } catch (err) {
    authMessage.textContent = err.message;
    authMessage.classList.remove("is-success");
  } finally {
    loginBtn.disabled = false;
  }
});

signupBtn.addEventListener("click", async () => {
  const data = Object.fromEntries(new FormData(loginForm));
  signupBtn.disabled = true;
  try {
    await api("/auth/signup", { method: "POST", body: JSON.stringify(data) });
    authMessage.textContent = "Sign up complete! Please log in.";
    authMessage.classList.add("is-success");
  } catch (err) {
    authMessage.textContent = err.message;
    authMessage.classList.remove("is-success");
  } finally {
    signupBtn.disabled = false;
  }
});

logoutBtn.addEventListener("click", async () => {
  try { await api("/auth/logout", { method: "POST" }); } catch (_) { /* 무시 */ }
  showAuthSection();
  loginForm.reset();
});

// ── 카테고리 관리 (SCR-003) ────────────────────────────
async function loadCategories() {
  const categories = await api("/categories");
  renderCategoryRows(categories);
  renderCategorySelect(categories);
}

function renderCategoryRows(categories) {
  categoryList.innerHTML = "";
  categories.forEach((cat) => {
    const li = document.createElement("li");
    li.innerHTML = `
      <span class="row-item__info"><span class="row-item__name">${escapeHtml(cat.name)}</span></span>
      <span class="row-item__ops">
        <button type="button" class="row-btn row-btn--edit" data-op="rename">Edit</button>
        <button type="button" class="row-btn row-btn--delete" data-op="delete">Delete</button>
      </span>
    `;
    li.querySelector('[data-op="rename"]').addEventListener("click", () => renameCategory(cat));
    li.querySelector('[data-op="delete"]').addEventListener("click", () => deleteCategory(cat));
    categoryList.appendChild(li);
  });
}

function renderCategorySelect(categories) {
  const prev = categorySelect.value;
  categorySelect.innerHTML = '<option value="">Category ▼ (Dropdown)</option>';
  categories.forEach((cat) => {
    const opt = document.createElement("option");
    opt.value = cat.id;
    opt.textContent = cat.name;
    categorySelect.appendChild(opt);
  });
  if ([...categorySelect.options].some((o) => o.value === prev && o.value !== "")) {
    categorySelect.value = prev;
  }
}

categoryForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  const data = Object.fromEntries(new FormData(categoryForm));
  try {
    await api("/categories", { method: "POST", body: JSON.stringify(data) });
    categoryForm.reset();
    await loadCategories();
    showMessage("새 카테고리가 추가되었습니다.", "success");
  } catch (_) { /* 메시지는 api()에서 처리 */ }
});

async function renameCategory(cat) {
  const name = prompt("새 카테고리 이름을 입력하세요 (1~10자)", cat.name);
  if (!name || name === cat.name) return;
  try {
    await api(`/categories/${cat.id}`, { method: "PATCH", body: JSON.stringify({ name }) });
    await loadCategories();
    await loadContacts(searchInput.value.trim() || undefined);
    showMessage("카테고리 이름이 바뀌었습니다.", "success");
  } catch (_) { /* 무시 */ }
}

async function deleteCategory(cat) {
  if (!confirm(`Delete "${cat.name}" category?`)) return;
  try {
    await api(`/categories/${cat.id}`, { method: "DELETE" });
    await loadCategories();
    showMessage("Category deleted.", "success");
  } catch (_) { /* 409 등은 api()가 메시지로 안내 */ }
}

// ── 연락처 목록 (SCR-002) ──────────────────────────────
async function loadContacts(name) {
  const params = new URLSearchParams();
  if (name) params.set("name", name);
  const res = await api(`/contacts${params.toString() ? "?" + params : ""}`);
  renderContacts(res);
}

function renderContacts({ total, items }) {
  contactCount.textContent = `${total} people saved`;
  contactListEl.innerHTML = "";
  emptyState.hidden = total > 0;

  items.forEach((contact) => {
    const li = document.createElement("li");
    li.innerHTML = `
      <span class="row-item__info">
        <span class="row-item__name">${escapeHtml(contact.name)}</span>
        <span class="row-item__sep">·</span>
        <span class="row-item__phone">${escapeHtml(contact.phone)}</span>
        <span class="row-item__sep">·</span>
        <span class="row-item__addr">${escapeHtml(contact.addr || "-")}</span>
        <span class="row-item__sep">·</span>
        <span class="row-item__type">${escapeHtml(contact.category_name)}</span>
      </span>
      <span class="row-item__ops">
        <button type="button" class="row-btn row-btn--edit" data-op="edit">Edit</button>
        <button type="button" class="row-btn row-btn--delete" data-op="delete">Delete</button>
      </span>
    `;
    li.querySelector('[data-op="edit"]').addEventListener("click", () => startEdit(contact));
    li.querySelector('[data-op="delete"]').addEventListener("click", () => removeContact(contact));
    contactListEl.appendChild(li);
  });
}

// ── 추가 / 수정 폼 ─────────────────────────────────────
contactForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  const data = Object.fromEntries(new FormData(contactForm));
  data.category_id = Number(data.category_id);
  if (!data.addr) delete data.addr;

  contactSubmitBtn.disabled = true;
  try {
    if (editingContactId) {
      await api(`/contacts/${editingContactId}`, { method: "PATCH", body: JSON.stringify(data) });
      showMessage("Contact updated.", "success");
    } else {
      await api("/contacts", { method: "POST", body: JSON.stringify(data) });
      showMessage("Contact added.", "success");
    }
    endEdit();
    await loadContacts(searchInput.value.trim() || undefined);
  } catch (_) {
    /* 실패 시 입력값 유지 — 안내는 api()에서 처리 */
  } finally {
    contactSubmitBtn.disabled = false;
  }
});

function startEdit(contact) {
  editingContactId = contact.id;
  contactForm.name.value = contact.name;
  contactForm.phone.value = contact.phone;
  contactForm.addr.value = contact.addr || "";
  categorySelect.value = contact.category_id;

  contactFormTitle.textContent = `Editing "${contact.name}"`;
  contactSubmitBtn.textContent = "Save";
  contactCancelBtn.hidden = false;
  contactForm.scrollIntoView({ behavior: "smooth", block: "center" });
}

function endEdit() {
  editingContactId = null;
  contactForm.reset();
  contactFormTitle.textContent = "Entering new contact";
  contactSubmitBtn.textContent = "Add";
  contactCancelBtn.hidden = true;
}

contactCancelBtn.addEventListener("click", endEdit);

async function removeContact(contact) {
  if (!confirm(`Delete contact "${contact.name}"?`)) return;
  try {
    await api(`/contacts/${contact.id}`, { method: "DELETE" });
    showMessage("Contact deleted.", "success");
    await loadContacts(searchInput.value.trim() || undefined);
  } catch (_) { /* 무시 */ }
}

// ── 검색 / 전체 (버튼 하나) ─────────────────────────────
searchBtn.addEventListener("click", () => loadContacts(searchInput.value.trim() || undefined));
searchInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter") { e.preventDefault(); loadContacts(searchInput.value.trim() || undefined); }
});

// ── 시작 ──────────────────────────────────────────────
bootstrap();
