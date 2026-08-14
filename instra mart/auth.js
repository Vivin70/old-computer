// Registration
const registerForm = document.getElementById("registerForm");
if (registerForm) {
  registerForm.addEventListener("submit", function (e) {
    e.preventDefault();

    const user = {
      name: document.getElementById("name").value,
      email: document.getElementById("email").value,
      phone: document.getElementById("phone").value,
      password: document.getElementById("password").value,
      address: document.getElementById("address").value
    };

    localStorage.setItem("instamartUser", JSON.stringify(user));
    alert("Registration successful! Please login.");
    window.location.href = "login.html";
  });
}

// Login
const loginForm = document.getElementById("loginForm");
if (loginForm) {
  loginForm.addEventListener("submit", function (e) {
    e.preventDefault();

    const username = document.getElementById("login-username").value;
    const password = document.getElementById("login-password").value;
    const storedUser = JSON.parse(localStorage.getItem("instamartUser"));

    if (!storedUser) {
      alert("No user registered. Please register first.");
      return;
    }

    if ((username === storedUser.email || username === storedUser.name) && password === storedUser.password) {
      alert("Login successful!");
      window.location.href = "index.html"; // redirect to homepage
    } else {
      alert("Invalid credentials!");
    }
  });
}
