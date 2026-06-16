from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()

@router.get("/", response_class=HTMLResponse, include_in_schema=False)
def gui():
    return """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Horse Training Planner</title>
  <style>
    :root {
      --ink: #1f2933;
      --muted: #52606d;
      --line: #d9e2ec;
      --panel: #ffffff;
      --page: #eef2f7;
      --accent: #2563eb;
      --accent-dark: #1d4ed8;
      --danger: #b91c1c;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      font-family: Arial, Helvetica, sans-serif;
      color: var(--ink);
      background: var(--page);
    }
    header {
      padding: 22px clamp(16px, 4vw, 42px);
      border-bottom: 1px solid var(--line);
      background: var(--panel);
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      flex-wrap: wrap;
    }
    h1, h2, h3 { margin: 0; line-height: 1.2; }
    h1 { font-size: clamp(1.35rem, 3vw, 2rem); }
    h2 { font-size: 1.05rem; }
    h3 { font-size: .95rem; color: var(--muted); }
    main {
      width: min(1220px, calc(100% - 28px));
      margin: 22px auto 42px;
      display: grid;
      grid-template-columns: minmax(280px, 360px) 1fr;
      align-items: start;
      gap: 18px;
    }
    section, form, .toolbar, .output {
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
    }
    section { padding: 16px; }
    .stack {
      display: grid;
      gap: 14px;
      align-content: start;
    }
    form {
      padding: 14px;
      display: grid;
      gap: 10px;
    }
    label {
      display: grid;
      gap: 5px;
      color: var(--muted);
      font-size: .86rem;
      font-weight: 700;
    }
    input, select, button {
      width: 100%;
      min-height: 40px;
      border-radius: 6px;
      font: inherit;
    }
    input, select {
      border: 1px solid #bcccdc;
      padding: 8px 10px;
      background: #fff;
    }
    .submitted input:invalid, .submitted select:invalid { border-color: var(--danger); }
    button {
      border: 0;
      padding: 9px 12px;
      color: #fff;
      background: var(--accent);
      cursor: pointer;
      font-weight: 700;
    }
    button:hover { background: var(--accent-dark); }
    button.secondary { background: #475569; }
    button.danger { background: var(--danger); }
    
    /* REFACTOR: Changed hard-coded columns to use fluid auto-fit wrapping */
    .grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
      gap: 14px;
    }
    .toolbar {
      padding: 12px;
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));
      gap: 10px;
    }
    .filter-bar {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
      gap: 10px;
      align-items: end;
    }
    
    .table-wrap { overflow-x: auto; }
    table {
      width: 100%;
      border-collapse: collapse;
      min-width: 680px;
      background: #fff;
    }
    th, td {
      border-bottom: 1px solid var(--line);
      padding: 10px;
      text-align: left;
      white-space: nowrap;
    }
    th {
      color: var(--muted);
      font-size: .82rem;
      text-transform: uppercase;
    }
    .pager {
      display: grid;
      grid-template-columns: 110px 1fr 110px;
      gap: 10px;
      align-items: center;
    }
    .page-info {
      text-align: center;
      color: var(--muted);
      font-weight: 700;
    }
    .status {
      padding: 10px 12px;
      border-radius: 6px;
      background: #fee2e2;
      color: #991b1b;
      font-weight: 700;
    }
    .status.signed-in {
      background: #dcfce7;
      color: #166534;
    }
    .output {
      min-height: 220px;
      padding: 14px;
      overflow: auto;
      background: #0f172a;
      color: #e2e8f0;
      white-space: pre-wrap;
    }
    .mini-output {
      min-height: 120px;
      max-height: 260px;
    }
    .hint { color: var(--muted); font-size: .84rem; }
    
    /* REFACTOR: Lifted the layout breakpoint slightly from 920px to 1100px to avoid squishing */
    @media (max-width: 1100px) {
      main { grid-template-columns: 1fr; }
    }
    @media (max-width: 600px) {
      .grid, .toolbar, .filter-bar, .pager { grid-template-columns: 1fr; }
      .page-info { text-align: center; order: -1; }
    }
  </style>
</head>
<body>
  <header>
    <div>
      <h1>Horse Training Planner</h1>
      <p class="hint">Register, log in, browse stable data, and manage trainings through the REST API.</p>
    </div>
    <div id="authStatus" class="status">Signed out</div>
  </header>

  <main>
    <aside class="stack">
      <section class="stack">
        <h2>Account</h2>
        <form id="registerForm">
          <h3>Register user</h3>
          <label>Name <input name="name" required minlength="2" maxlength="40" pattern="[A-Za-zÀ-ž .'-]{2,40}" autocomplete="given-name"></label>
          <label>Surname <input name="surname" required minlength="2" maxlength="40" pattern="[A-Za-zÀ-ž .'-]{2,40}" autocomplete="family-name"></label>
          <label>Email <input name="email" required type="email" maxlength="120" autocomplete="email"></label>
          <label>Password <input name="password" required type="password" minlength="6" maxlength="72" autocomplete="new-password"></label>
          <button type="submit">Create account</button>
        </form>
        <form id="loginForm">
          <h3>Login</h3>
          <label>Email <input name="email" required type="email" maxlength="120" autocomplete="email"></label>
          <label>Password <input name="password" required type="password" minlength="6" maxlength="72" autocomplete="current-password"></label>
          <button type="submit">Log in</button>
        </form>
      </section>

      <section class="stack">
        <h2>Quick lookups</h2>
        <div class="toolbar">
          <button type="button" data-get="/api/horses">Horses</button>
          <button type="button" data-get="/api/trainers">Trainers</button>
          <button type="button" data-get="/api/training-types">Types</button>
          <button type="button" data-get="/api/trainings">Trainings</button>
          <button type="button" class="secondary" id="logoutButton">Logout</button>
        </div>
        <h3>Lookup results</h3>
        <pre id="lookupOutput" class="output mini-output">Click Horses, Trainers, Types, or Trainings.</pre>
      </section>
    </aside>

    <div class="stack">
    <section class="stack">
      <h2>Browse trainings</h2>
      <form id="trainingFilterForm" class="filter-bar">
        <label>Status
          <select name="status">
            <option value="">All statuses</option>
            <option value="open">open</option>
            <option value="full">full</option>
            <option value="completed">completed</option>
            <option value="cancelled">cancelled</option>
          </select>
        </label>
        <label>Horse ID <input name="horse_id" type="number" min="1" step="1" inputmode="numeric" placeholder="Any"></label>
        <label>Page size <input name="size" type="number" min="1" max="20" step="1" value="5" inputmode="numeric"></label>
        <button type="submit">Apply filter</button>
      </form>
      <div class="table-wrap">
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Horse</th>
              <th>Trainer</th>
              <th>Type</th>
              <th>Date</th>
              <th>Capacity</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody id="trainingRows">
            <tr><td colspan="7">Log in and apply a filter to load trainings.</td></tr>
          </tbody>
        </table>
      </div>
      <div class="pager">
        <button type="button" id="prevPage" class="secondary">Previous</button>
        <div id="pageInfo" class="page-info">Page 1 of 1, 0 results</div>
        <button type="button" id="nextPage" class="secondary">Next</button>
      </div>
    </section>

    <section class="stack">
      <h2>Training management</h2>
      <div class="grid">
        <form id="createTrainingForm">
          <h3>Create training</h3>
          <label>Horse ID <input name="horse_id" required type="number" min="1" step="1" inputmode="numeric"></label>
          <label>Trainer ID <input name="trainer_id" required type="number" min="1" step="1" inputmode="numeric"></label>
          <label>Training type ID <input name="training_type_id" required type="number" min="1" step="1" inputmode="numeric"></label>
          <label>Date <input name="date" required type="datetime-local"></label>
          <button type="submit">Create training</button>
        </form>

        <form id="updateTrainingForm">
          <h3>Update training</h3>
          <label>Training ID <input name="id" required type="number" min="1" step="1" inputmode="numeric"></label>
          <label>Horse ID <input name="horse_id" type="number" min="1" step="1" inputmode="numeric"></label>
          <label>Trainer ID <input name="trainer_id" type="number" min="1" step="1" inputmode="numeric"></label>
          <label>Training type ID <input name="training_type_id" type="number" min="1" step="1" inputmode="numeric"></label>
          <label>Date <input name="date" type="datetime-local"></label>
          <label>Capacity <input name="capacity" type="number" min="1" max="30" step="1" inputmode="numeric"></label>
          <label>Status
            <select name="status">
              <option value="">No change</option>
              <option value="open">open</option>
              <option value="full">full</option>
              <option value="completed">completed</option>
              <option value="cancelled">cancelled</option>
            </select>
          </label>
          <button type="submit">Update training</button>
        </form>

        <form id="joinTrainingForm">
          <h3>Join training</h3>
          <label>Training ID <input name="id" required type="number" min="1" step="1" inputmode="numeric"></label>
          <button type="submit">Join</button>
        </form>

        <form id="participantsForm">
          <h3>Show participants</h3>
          <label>Training ID <input name="id" required type="number" min="1" step="1" inputmode="numeric"></label>
          <button type="submit">Load participants</button>
        </form>

        <form id="deleteTrainingForm">
          <h3>Delete training</h3>
          <label>Training ID <input name="id" required type="number" min="1" step="1" inputmode="numeric"></label>
          <button type="submit" class="danger">Delete training</button>
        </form>
      </div>

      <h2>API response</h2>
      <pre id="output" class="output">Ready.</pre>
    </section>
    </div>
  </main>

  <script>
    const output = document.querySelector("#output");
    const lookupOutput = document.querySelector("#lookupOutput");
    const authStatus = document.querySelector("#authStatus");
    const trainingRows = document.querySelector("#trainingRows");
    const pageInfo = document.querySelector("#pageInfo");
    const prevPage = document.querySelector("#prevPage");
    const nextPage = document.querySelector("#nextPage");
    const tokenKey = "horsePlannerToken";
    let token = localStorage.getItem(tokenKey) || "";
    let trainingPage = 1;
    let trainingPages = 1;
    let activeTrainingFilters = { status: "", horse_id: "", size: "5" };

    function setStatus() {
      authStatus.textContent = token ? "Signed in" : "Signed out";
      authStatus.classList.toggle("signed-in", Boolean(token));
    }

    function asIsoDate(value) {
      return value ? new Date(value).toISOString() : undefined;
    }

    function integer(value) {
      return value === "" ? undefined : Number.parseInt(value, 10);
    }

    function readForm(form) {
      const data = Object.fromEntries(new FormData(form).entries());
      for (const [key, value] of Object.entries(data)) {
        if (value === "") delete data[key];
      }
      return data;
    }

    function validateAtLeastOneTrainingUpdate(body) {
      if (Object.keys(body).length === 0) {
        throw new Error("Enter at least one field to update.");
      }
    }

    function formatDate(value) {
      return value ? new Date(value).toLocaleString() : "";
    }

    function renderTrainingPage(data) {
      trainingPage = data.page;
      trainingPages = data.pages;
      pageInfo.textContent = `Page ${data.page} of ${data.pages}, ${data.total} result${data.total === 1 ? "" : "s"}`;
      prevPage.disabled = data.page <= 1;
      nextPage.disabled = data.page >= data.pages;
      trainingRows.innerHTML = "";

      if (data.items.length === 0) {
        trainingRows.innerHTML = '<tr><td colspan="7">No trainings match the current filter.</td></tr>';
        return;
      }

      data.items.forEach((training) => {
        const row = document.createElement("tr");
        row.innerHTML = `
          <td>${training.id}</td>
          <td>${training.horse_id}</td>
          <td>${training.trainer_id}</td>
          <td>${training.training_type_id}</td>
          <td>${formatDate(training.date)}</td>
          <td>${training.capacity}</td>
          <td>${training.status}</td>
        `;
        trainingRows.appendChild(row);
      });
    }

    async function loadTrainingPage(page = 1) {
      const params = new URLSearchParams({
        page: String(page),
        size: activeTrainingFilters.size || "5"
      });
      if (activeTrainingFilters.status) params.set("status", activeTrainingFilters.status);
      if (activeTrainingFilters.horse_id) params.set("horse_id", activeTrainingFilters.horse_id);
      const data = await request(`/api/trainings/page?${params.toString()}`);
      renderTrainingPage(data);
    }

    async function request(path, options = {}, target = output) {
      const headers = { "Content-Type": "application/json", ...(options.headers || {}) };
      if (token) headers.Authorization = `Bearer ${token}`;
      const response = await fetch(path, { ...options, headers });
      const text = await response.text();
      let body = text;
      try { body = text ? JSON.parse(text) : null; } catch (_) {}
      target.textContent = JSON.stringify({ status: response.status, body }, null, 2);
      if (!response.ok) {
        throw new Error(typeof body === "string" ? body : (body && body.detail) || "Request failed");
      }
      return body;
    }

    function onSubmit(selector, handler) {
      document.querySelector(selector).addEventListener("submit", async (event) => {
        event.preventDefault();
        const form = event.currentTarget;
        form.classList.add("submitted");
        if (!form.reportValidity()) return;
        try {
          await handler(form);
        } catch (error) {
          output.textContent += `\\n\\n${error.message}`;
        }
      });
    }

    onSubmit("#registerForm", (form) => {
      return request("/api/users", { method: "POST", body: JSON.stringify(readForm(form)) });
    });

    onSubmit("#loginForm", async (form) => {
      const body = await request("/api/auth/login", { method: "POST", body: JSON.stringify(readForm(form)) });
      token = body.token;
      localStorage.setItem(tokenKey, token);
      setStatus();
    });

    onSubmit("#createTrainingForm", (form) => {
      const data = readForm(form);
      const body = {
        horse_id: integer(data.horse_id),
        trainer_id: integer(data.trainer_id),
        training_type_id: integer(data.training_type_id),
        date: asIsoDate(data.date)
      };
      return request("/api/trainings", { method: "POST", body: JSON.stringify(body) });
    });

    onSubmit("#updateTrainingForm", (form) => {
      const data = readForm(form);
      const id = integer(data.id);
      delete data.id;
      const body = {};
      ["horse_id", "trainer_id", "training_type_id", "capacity"].forEach((key) => {
        if (data[key] !== undefined) body[key] = integer(data[key]);
      });
      if (data.date) body.date = asIsoDate(data.date);
      if (data.status) body.status = data.status;
      validateAtLeastOneTrainingUpdate(body);
      return request(`/api/trainings/${id}`, { method: "PUT", body: JSON.stringify(body) });
    });

    onSubmit("#joinTrainingForm", (form) => {
      const id = integer(readForm(form).id);
      return request(`/api/trainings/${id}/join`, { method: "POST", body: "{}" });
    });

    onSubmit("#participantsForm", (form) => {
      const id = integer(readForm(form).id);
      return request(`/api/trainings/${id}/participants`);
    });

    onSubmit("#deleteTrainingForm", (form) => {
      const id = integer(readForm(form).id);
      return request(`/api/trainings/${id}`, { method: "DELETE" });
    });

    onSubmit("#trainingFilterForm", (form) => {
      activeTrainingFilters = readForm(form);
      activeTrainingFilters.size = activeTrainingFilters.size || "5";
      trainingPage = 1;
      return loadTrainingPage(trainingPage);
    });

    document.querySelectorAll("[data-get]").forEach((button) => {
      button.addEventListener("click", () => request(button.dataset.get, {}, lookupOutput).catch((error) => {
        lookupOutput.textContent += `\\n\\n${error.message}`;
      }));
    });

    document.querySelector("#logoutButton").addEventListener("click", () => {
      token = "";
      localStorage.removeItem(tokenKey);
      setStatus();
      output.textContent = "Signed out.";
    });

    prevPage.addEventListener("click", () => {
      if (trainingPage > 1) loadTrainingPage(trainingPage - 1).catch((error) => {
        output.textContent += `\\n\\n${error.message}`;
      });
    });

    nextPage.addEventListener("click", () => {
      if (trainingPage < trainingPages) loadTrainingPage(trainingPage + 1).catch((error) => {
        output.textContent += `\\n\\n${error.message}`;
      });
    });

    setStatus();
  </script>
</body>
</html>
"""
