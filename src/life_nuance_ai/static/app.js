const state = { cases: [], assistants: [], activeCase: null };

const $ = (selector) => document.querySelector(selector);
const el = (tag, className, text) => {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text) node.textContent = text;
  return node;
};

async function loadDemo() {
  const [casesResponse, assistantsResponse] = await Promise.all([
    fetch("/v1/demo/cases"),
    fetch("/v1/assistants"),
  ]);
  state.cases = await casesResponse.json();
  state.assistants = await assistantsResponse.json();
  renderExamples();
  renderCatalog();
  renderSourceLibrary();
}

function renderExamples() {
  const list = $("#example-list");
  state.cases.forEach((item) => {
    const button = el("button", "example-chip", item.label);
    button.type = "button";
    button.addEventListener("click", () => selectCase(item, true));
    list.append(button);
  });
}

function selectCase(item, submit = false) {
  state.activeCase = item;
  $("#message").value = item.message;
  $("#location").value = item.location;
  if (submit) routeRequest();
}

function findCase(message) {
  const normalized = message.toLowerCase();
  return state.cases.find((item) => item.message.toLowerCase() === normalized)
    || state.cases.find((item) => item.message.toLowerCase().split(" ").filter((word) => normalized.includes(word)).length >= 5)
    || null;
}

async function routeRequest() {
  const message = $("#message").value.trim();
  if (!message) {
    $("#message").focus();
    return;
  }

  const button = $("#route-button");
  button.disabled = true;
  button.firstElementChild.textContent = "Routing";
  try {
    const response = await fetch("/v1/route", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        user_id: "demo-user",
        message,
        location: $("#location").value.trim(),
        constraints: state.activeCase?.constraints || {},
      }),
    });
    if (!response.ok) throw new Error("Could not route request");
    const route = await response.json();
    const demoCase = findCase(message) || state.cases.find((item) => item.assistant_id === route.assistant.id);
    renderResult(route, demoCase);
  } catch (error) {
    button.firstElementChild.textContent = "Try again";
    return;
  } finally {
    button.disabled = false;
    if (button.firstElementChild.textContent === "Routing") button.firstElementChild.textContent = "Route";
  }
}

function renderResult(route, item) {
  $("#empty-state").classList.add("hidden");
  $("#result").classList.remove("hidden");
  $("#assistant-icon").textContent = route.assistant.name.charAt(0);
  $("#assistant-name").textContent = route.assistant.name;
  $("#assistant-description").textContent = route.assistant.description;
  $("#confidence").textContent = `${Math.round(route.confidence * 100)}%`;
  $("#risk").textContent = route.risk_level;
  $("#routing-method").textContent = route.routing_method === "trained" ? "AI model" : "Rules";
  $("#disclaimer").textContent = route.disclaimer;
  $("#case-summary").textContent = item?.summary || "A structured starting point for this decision.";
  $("#handoff").classList.toggle("hidden", !route.handoff_required && route.risk_level !== "high");
  fillList("#facts", item?.facts || ["The assistant matched the request to its registered domain and boundaries."]);
  fillList("#actions", item?.actions || route.suggested_next_steps);
  fillList("#questions", route.intake_questions);
  renderSources(item?.sources || []);
  $("#result").scrollIntoView({ behavior: "smooth", block: "start" });
}

function fillList(selector, items) {
  const list = $(selector);
  list.replaceChildren(...items.map((item) => el("li", "", item)));
}

function renderSources(sources) {
  const container = $("#sources");
  container.replaceChildren(...sources.map((source) => {
    const card = el("div", "source-card");
    const link = el("a", "", source.title);
    link.href = source.url;
    link.target = "_blank";
    link.rel = "noreferrer";
    card.append(link, el("p", "", source.publisher), el("small", "", `Source checked ${source.checked}`));
    return card;
  }));
}

function renderCatalog() {
  $("#assistant-count").textContent = `${state.assistants.length} assistants registered`;
  const grid = $("#assistant-grid");
  grid.replaceChildren(...state.assistants.map((assistant) => {
    const card = el("article", "assistant-card");
    const top = el("div", "assistant-card-top");
    top.append(el("span", "assistant-icon", assistant.name.charAt(0)));
    const use = el("button", "", "Open workspace");
    use.type = "button";
    use.addEventListener("click", () => {
      showView("workspace");
      const item = state.cases.find((candidate) => candidate.assistant_id === assistant.id);
      if (item) selectCase(item);
      $("#message").focus();
    });
    top.append(use);
    card.append(top, el("h3", "", assistant.name), el("p", "", assistant.description));
    const tags = el("div", "tags");
    assistant.domains.forEach((domain) => tags.append(el("span", "tag", domain)));
    card.append(tags);
    return card;
  }));
}

function renderSourceLibrary() {
  const seen = new Set();
  const sources = state.cases.flatMap((item) => item.sources).filter((source) => {
    if (seen.has(source.url)) return false;
    seen.add(source.url);
    return true;
  });
  $("#source-library").replaceChildren(...sources.map((source) => {
    const row = el("div", "library-row");
    const link = el("a", "", source.title);
    link.href = source.url;
    link.target = "_blank";
    link.rel = "noreferrer";
    row.append(link, el("span", "", source.publisher), el("small", "", `Checked ${source.checked}`));
    return row;
  }));
}

function showView(view) {
  $("#workspace").classList.toggle("hidden", view !== "workspace");
  $("#assistants").classList.toggle("hidden", view !== "assistants");
  $("#sources-view").classList.toggle("hidden", view !== "sources");
  document.querySelectorAll(".nav-item").forEach((item) => item.classList.toggle("active", item.dataset.view === view));
  $(".sidebar").classList.remove("open");
}

$("#route-button").addEventListener("click", routeRequest);
$("#message").addEventListener("keydown", (event) => {
  if ((event.metaKey || event.ctrlKey) && event.key === "Enter") routeRequest();
});
document.querySelectorAll(".nav-item").forEach((item) => item.addEventListener("click", () => showView(item.dataset.view)));
$(".mobile-menu").addEventListener("click", () => $(".sidebar").classList.toggle("open"));

loadDemo().catch(() => {
  $("#example-list").append(el("span", "", "Demo data unavailable"));
});
