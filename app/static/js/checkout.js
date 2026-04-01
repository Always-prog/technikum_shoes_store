(function () {
  const page = document.querySelector("[data-checkout-page]");
  if (!page || !window.CartStore) return;

  const itemsContainer = page.querySelector("[data-checkout-items]");
  const form = page.querySelector("[data-checkout-form]");
  const payloadInput = page.querySelector("[data-cart-payload]");
  const cart = window.CartStore.loadCart();

  if (cart.length === 0) {
    itemsContainer.innerHTML =
      '<p class="empty-result">Корзина пуста. Добавь товары перед оформлением.</p>';
  } else {
    let total = 0;
    const rows = cart
      .map((item) => {
        const line = Number(item.price) * Number(item.quantity);
        total += line;
        return `<li>${item.name} x ${item.quantity} — ${line.toFixed(2)} ₽</li>`;
      })
      .join("");

    itemsContainer.innerHTML = `
      <h2>Состав заказа</h2>
      <ul class="checkout-list">${rows}</ul>
      <p class="checkout-total">Итого: <strong>${total.toFixed(2)} ₽</strong></p>
    `;
  }

  payloadInput.value = JSON.stringify(
    cart.map((item) => ({
      product_id: Number(item.product_id),
      quantity: Number(item.quantity),
    }))
  );

  form.addEventListener("submit", (event) => {
    if (cart.length === 0) {
      event.preventDefault();
      alert("Корзина пуста.");
    }
  });
})();
