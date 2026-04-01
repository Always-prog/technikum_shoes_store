(function () {
  const CART_KEY = "shoes_store_cart";

  function loadCart() {
    try {
      const raw = localStorage.getItem(CART_KEY);
      if (!raw) return [];
      const parsed = JSON.parse(raw);
      return Array.isArray(parsed) ? parsed : [];
    } catch (_err) {
      return [];
    }
  }

  function saveCart(items) {
    localStorage.setItem(CART_KEY, JSON.stringify(items));
  }

  function getTotals(items) {
    const totalItems = items.reduce((sum, item) => sum + Number(item.quantity || 0), 0);
    const totalPrice = items.reduce(
      (sum, item) => sum + Number(item.quantity || 0) * Number(item.price || 0),
      0
    );
    return { totalItems, totalPrice };
  }

  function updateBadge() {
    const cart = loadCart();
    const { totalItems } = getTotals(cart);
    document.querySelectorAll("[data-cart-count]").forEach((el) => {
      el.textContent = String(totalItems);
    });
  }

  function upsertItem(nextItem) {
    const cart = loadCart();
    const existing = cart.find((item) => Number(item.product_id) === Number(nextItem.product_id));
    if (existing) {
      existing.quantity += 1;
    } else {
      cart.push({ ...nextItem, quantity: 1 });
    }
    saveCart(cart);
    updateBadge();
  }

  function attachAddToCartButtons() {
    document.querySelectorAll("[data-add-to-cart]").forEach((button) => {
      button.addEventListener("click", () => {
        upsertItem({
          product_id: Number(button.dataset.productId),
          slug: button.dataset.productSlug,
          name: button.dataset.productName,
          price: Number(button.dataset.productPrice),
          image_url: button.dataset.productImage || "",
        });
        button.textContent = "Добавлено";
      });
    });
  }

  function renderCartPage() {
    const page = document.querySelector("[data-cart-page]");
    if (!page) return;

    const itemsContainer = page.querySelector("[data-cart-items]");
    const totalItemsEl = page.querySelector("[data-cart-total-items]");
    const totalPriceEl = page.querySelector("[data-cart-total-price]");
    const cart = loadCart();

    if (cart.length === 0) {
      itemsContainer.innerHTML = '<p class="empty-result">Корзина пуста.</p>';
      totalItemsEl.textContent = "0";
      totalPriceEl.textContent = "0.00";
      return;
    }

    itemsContainer.innerHTML = "";
    cart.forEach((item) => {
      const row = document.createElement("article");
      row.className = "cart-row";
      row.innerHTML = `
        <div class="cart-row-image-wrap">
          ${
            item.image_url
              ? `<img src="${item.image_url}" alt="${item.name}" class="cart-row-image">`
              : `<div class="image-placeholder">Нет изображения</div>`
          }
        </div>
        <div class="cart-row-main">
          <h3>${item.name}</h3>
          <p>${Number(item.price).toFixed(2)} ₽</p>
          <div class="cart-row-actions">
            <button type="button" data-cart-dec="${item.product_id}">-</button>
            <span>${item.quantity}</span>
            <button type="button" data-cart-inc="${item.product_id}">+</button>
            <button type="button" data-cart-remove="${item.product_id}">Удалить</button>
          </div>
        </div>
      `;
      itemsContainer.appendChild(row);
    });

    itemsContainer.querySelectorAll("[data-cart-inc]").forEach((button) => {
      button.addEventListener("click", () => changeQuantity(Number(button.dataset.cartInc), 1));
    });
    itemsContainer.querySelectorAll("[data-cart-dec]").forEach((button) => {
      button.addEventListener("click", () => changeQuantity(Number(button.dataset.cartDec), -1));
    });
    itemsContainer.querySelectorAll("[data-cart-remove]").forEach((button) => {
      button.addEventListener("click", () => removeItem(Number(button.dataset.cartRemove)));
    });

    const totals = getTotals(loadCart());
    totalItemsEl.textContent = String(totals.totalItems);
    totalPriceEl.textContent = totals.totalPrice.toFixed(2);
  }

  function changeQuantity(productId, delta) {
    const cart = loadCart()
      .map((item) =>
        Number(item.product_id) === productId
          ? { ...item, quantity: Math.max(0, Number(item.quantity) + delta) }
          : item
      )
      .filter((item) => Number(item.quantity) > 0);
    saveCart(cart);
    updateBadge();
    renderCartPage();
  }

  function removeItem(productId) {
    const cart = loadCart().filter((item) => Number(item.product_id) !== productId);
    saveCart(cart);
    updateBadge();
    renderCartPage();
  }

  window.CartStore = {
    loadCart,
    saveCart,
    clear() {
      saveCart([]);
      updateBadge();
    },
  };

  if (document.querySelector("[data-order-success]")) {
    window.CartStore.clear();
  }

  updateBadge();
  attachAddToCartButtons();
  renderCartPage();
})();
