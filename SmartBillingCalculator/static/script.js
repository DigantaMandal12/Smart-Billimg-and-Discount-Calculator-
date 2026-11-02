/**
 * Smart Billing & Discount Calculator — Frontend Interaction Script
 * Uses safe DOM node creation (document.createElement) instead of unsafe string interpolation.
 */
(function () {
  "use strict";

  const itemsContainer = document.getElementById("items");
  const addItemBtn = document.getElementById("add-item-btn");
  const printBillBtn = document.getElementById("print-bill-btn");
  const rowCounterPill = document.getElementById("row-counter-pill");

  if (!itemsContainer) {
    return;
  }

  const maxItems = parseInt(itemsContainer.getAttribute("data-max-items") || "50", 10);
  let rowIdSequence = itemsContainer.querySelectorAll(".item-row").length;

  function updateRowCounter() {
    const count = itemsContainer.querySelectorAll(".item-row").length;
    if (rowCounterPill) {
      rowCounterPill.textContent = count + " / " + maxItems + (count === 1 ? " item" : " items");
    }
  }

  function createFieldGroup(labelText, inputConfig) {
    const group = document.createElement("div");
    group.className = "field-group";

    const label = document.createElement("label");
    label.className = "mobile-label";
    label.setAttribute("for", inputConfig.id);
    label.textContent = labelText;

    const input = document.createElement("input");
    input.id = inputConfig.id;
    input.name = inputConfig.name;
    input.type = inputConfig.type;
    if (inputConfig.maxLength) {
      input.maxLength = inputConfig.maxLength;
    }
    if (inputConfig.min !== undefined) {
      input.min = inputConfig.min;
    }
    if (inputConfig.max !== undefined) {
      input.max = inputConfig.max;
    }
    if (inputConfig.step !== undefined) {
      input.step = inputConfig.step;
    }
    if (inputConfig.placeholder) {
      input.placeholder = inputConfig.placeholder;
    }
    if (inputConfig.value !== undefined) {
      input.value = inputConfig.value;
    }
    input.setAttribute("aria-label", inputConfig.ariaLabel);
    input.required = true;

    group.appendChild(label);
    group.appendChild(input);
    return { group: group, input: input };
  }

  function addItem() {
    const currentCount = itemsContainer.querySelectorAll(".item-row").length;
    if (currentCount >= maxItems) {
      window.alert("You can add up to " + maxItems + " products per bill.");
      return;
    }

    rowIdSequence += 1;
    const row = document.createElement("div");
    row.className = "item-row";

    const nameField = createFieldGroup("Product Name", {
      id: "item-name-" + rowIdSequence,
      name: "item_name[]",
      type: "text",
      maxLength: 80,
      placeholder: "e.g. Lab Notebook",
      ariaLabel: "Product name",
    });

    const priceField = createFieldGroup("Unit Price (₹)", {
      id: "item-price-" + rowIdSequence,
      name: "price[]",
      type: "number",
      min: "0",
      max: "100000000",
      step: "0.01",
      placeholder: "0.00",
      ariaLabel: "Price in rupees",
    });

    const qtyField = createFieldGroup("Quantity", {
      id: "item-qty-" + rowIdSequence,
      name: "quantity[]",
      type: "number",
      min: "1",
      max: "100000",
      step: "1",
      value: "1",
      ariaLabel: "Quantity",
    });

    const removeBtn = document.createElement("button");
    removeBtn.type = "button";
    removeBtn.className = "remove-button";
    removeBtn.setAttribute("aria-label", "Remove product row");
    removeBtn.title = "Remove row";
    removeBtn.textContent = "×";

    row.appendChild(nameField.group);
    row.appendChild(priceField.group);
    row.appendChild(qtyField.group);
    row.appendChild(removeBtn);

    itemsContainer.appendChild(row);
    updateRowCounter();
    nameField.input.focus();
  }

  function removeItem(button) {
    const rows = itemsContainer.querySelectorAll(".item-row");
    if (rows.length <= 1) {
      window.alert("At least one product row is required.");
      return;
    }
    const targetRow = button.closest(".item-row");
    if (targetRow) {
      targetRow.remove();
      updateRowCounter();
    }
  }

  if (addItemBtn) {
    addItemBtn.addEventListener("click", addItem);
  }

  itemsContainer.addEventListener("click", function (event) {
    const btn = event.target.closest(".remove-button");
    if (btn) {
      removeItem(btn);
    }
  });

  if (printBillBtn) {
    printBillBtn.addEventListener("click", function () {
      window.print();
    });
  }

  updateRowCounter();
})();
