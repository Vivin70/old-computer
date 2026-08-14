const products = [
    { id: 1, name: "Tomatoes", price: 30, img: "https://via.placeholder.com/100?text=Tomatoes" },
    { id: 2, name: "Apples", price: 50, img: "https://via.placeholder.com/100?text=Apples" },
    { id: 3, name: "Milk", price: 25, img: "https://via.placeholder.com/100?text=Milk" },
    { id: 4, name: "Bread", price: 20, img: "https://via.placeholder.com/100?text=Bread" }
  ];
  
  let cart = [];
  
  function renderProducts() {
    const grid = document.getElementById("product-grid");
    products.forEach(product => {
      const div = document.createElement("div");
      div.classList.add("product");
      div.innerHTML = `
        <img src="${product.img}" alt="${product.name}" />
        <h3>${product.name}</h3>
        <p>₹${product.price}</p>
        <button onclick="addToCart(${product.id})">Add to Cart</button>
      `;
      grid.appendChild(div);
    });
  }
  
  function addToCart(id) {
    const product = products.find(p => p.id === id);
    cart.push(product);
    updateCart();
  }
  
  function updateCart() {
    const cartItemsDiv = document.getElementById("cart-items");
    cartItemsDiv.innerHTML = "";
    let total = 0;
  
    cart.forEach((item, index) => {
      total += item.price;
      const div = document.createElement("div");
      div.classList.add("cart-item");
      div.innerHTML = `
        <span>${item.name} - ₹${item.price}</span>
        <button onclick="removeFromCart(${index})">❌</button>
      `;
      cartItemsDiv.appendChild(div);
    });
  
    document.getElementById("cart-count").innerText = cart.length;
    document.getElementById("cart-total").innerText = total;
  }
  
  function removeFromCart(index) {
    cart.splice(index, 1);
    updateCart();
  }
  
  document.getElementById("buy-now").addEventListener("click", () => {
    if (cart.length === 0) {
      alert("Your cart is empty!");
    } else {
      alert("Thank you for your purchase! 🛍️");
      cart = [];
      updateCart();
    }
  });
  
  window.onload = renderProducts;
  