const products = [
  { id: 1, name: 'Tomatoes', price: 30, img: 'https://via.placeholder.com/150?text=Tomatoes' },
  { id: 2, name: 'Apples', price: 50, img: 'https://via.placeholder.com/150?text=Apples' },
  { id: 3, name: 'Milk', price: 25, img: 'https://via.placeholder.com/150?text=Milk' },
  { id: 4, name: 'Bread', price: 20, img: 'https://via.placeholder.com/150?text=Bread' },
];

let cartCount = 0;

function renderProducts() {
  const grid = document.getElementById('product-grid');
  products.forEach(product => {
    const div = document.createElement('div');
    div.classList.add('product');
    div.innerHTML = `
      <img src="${product.img}" alt="${product.name}" />
      <h3>${product.name}</h3>
      <p>₹${product.price}</p>
      <button onclick="addToCart()">Add to Cart</button>
    `;
    grid.appendChild(div);
  });
}

function addToCart() {
  cartCount++;
  document.getElementById('cart-count').innerText = cartCount;
}

window.onload = renderProducts;
