import { getUserData, register, getHistory } from "./api.js";

// TODO: change base_url depending on the env it is running
const BASE_URL = ""
let $main = document.getElementById("main");

export async function loadHomeView() {
  let response = await fetch(`${BASE_URL}/get_content`);
  let content = await response.text();
  let isAuthenticated = response.headers.get("X-Is-Authenticated") === "True";

  $main.innerHTML = content;

  if (isAuthenticated) {
    loadLoggedView();
  } else {
    loadNotLoggedView();
  }
}

export async function loadNotLoggedView() {
}

export async function loadLoggedView() {
  let userData = await getUserData();
  document.getElementById("userName").textContent = userData["username"];
  document.getElementById("userImage").src = userData["profile_pic"];

  let historyData = await getHistory();
  loadHistory(historyData);

  let $gainAmount = document.getElementById("gainAmount");
  let $expenseAmount = document.getElementById("expenseAmount");
  $gainAmount.addEventListener("input", function(event) {
    $gainAmount.classList.remove("is-danger");
    formatMoneyInput(event);
  });
  $expenseAmount.addEventListener("input", function(event) {
    $expenseAmount.classList.remove("is-danger");
    formatMoneyInput(event);
  });

  let $gainDescription = document.getElementById("gainDescription");
  let $expenseDescription = document.getElementById("expenseDescription");

  document.getElementById("gainButton").addEventListener("click", async function() {
    let amountStr = $gainAmount.value;
    let description = $gainDescription.value;
    let amount = brlStringToFloat(amountStr);

    if (amount === 0) {
      $gainAmount.classList.add("is-danger")
      return
    }
    $gainAmount.classList.remove("is-danger");
    $gainAmount.value = "R$ 0,00";
    $gainDescription.value = "";

    let res = await register("gain", amount, description);
    let record = res.record;
    appendToHistory(record);
  });

  document.getElementById("expenseButton").addEventListener("click", async function() {
    let amountStr = $expenseAmount.value;
    let description = $expenseDescription.value;
    let amount = brlStringToFloat(amountStr);

    if (amount === 0) {
      $expenseAmount.classList.add("is-danger")
      return
    }
    $expenseAmount.classList.remove("is-danger");
    $expenseAmount.value = "R$ 0,00";
    $expenseDescription.value = "";

    let res = await register("expense", amount, description);
    let record = res["record"];
    appendToHistory(record);
  });
}

function brlStringToFloat(brlString) {
    // Remove the "R$" prefix
    brlString = brlString.replace("R$", "").trim();
    // Remove thousand separators
    brlString = brlString.replace(/\./g, "");
    // Replace the decimal comma with a dot
    brlString = brlString.replace(",", ".");
    // Convert to float
    return parseFloat(brlString);
}

function formatMoneyInput(event) {
  function formatMoney(value) {
    let integerPart = value.replace(/^0+/, '');
    let decimalPart = integerPart.length <= 2 ? integerPart.padStart(2, '0') : integerPart.slice(-2);
    let formattedInteger = integerPart.length <= 2 ? '0' : integerPart.slice(0, -2).replace(/\B(?=(\d{3})+(?!\d))/g, '.');
    return `${formattedInteger},${decimalPart}`;
  }
  let inputValue = event.target.value;
  let numericValue = inputValue.replace(/\D/g, '');
  let formattedMoney = formatMoney(numericValue);
  let amount = `R$ ${formattedMoney}`
  event.target.value = amount;
}

function appendToHistory(record) {
  const date = new Date(record.created_at);
  const formattedDate = `${String(date.getDate()).padStart(2, '0')}/${String(date.getMonth() + 1).padStart(2, '0')}/${date.getFullYear()}`;

  const newRow = document.createElement('tr');

  newRow.innerHTML = `
    <td>R$ ${record.amount.toFixed(2).replace('.', ',')}</td>
    <td>${record.description}</td>
    <td>${formattedDate}</td>
    <td>
      <div class="button-container">
        <button class="button is-small is-info">Editar</button>
        <button class="button is-small is-danger">Apagar</button>
      </div>
    </td>
  `;

  newRow.dataset.recordId = record.id;
  newRow.dataset.userId = record.user_id;

  const tbody = document.querySelector('#history tbody');
  tbody.insertBefore(newRow, tbody.firstChild);
}

function loadHistory(historyData) {
  let history = historyData.history;

  history.forEach((record) => appendToHistory(record));
}
