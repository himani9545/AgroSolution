
document.addEventListener('DOMContentLoaded', function () {

    // Get modal and buttons for Log In
var loginModal = document.getElementById("loginModal");
var loginBtn = document.getElementById("loginBtn");
var closeLoginModal = document.getElementById("closeLoginModal");
var loginLinkToSignupModal = document.getElementById("loginLinkToSignupModal");
var loginForm = document.querySelector("#loginModal form"); // Get the login form


// Get modal for Sign Up (This will be used when transitioning to Sign Up)
var signupModal = document.getElementById("signupModal");

// Open modal on "Log In" button click
loginBtn.onclick = function () {
    loginModal.style.display = "block";
};

// Close modal on "X" button click for Log In
closeLoginModal.onclick = function () {
    loginModal.style.display = "none";
};

// Switch to Sign Up modal when "Log In" link is clicked
loginLinkToSignupModal.onclick = function () {
    loginModal.style.display = "none"; // Close Log In modal
    signupModal.style.display = "block"; // Open Sign Up modal
};
// Handle form submission inside the Login Modal
loginForm.addEventListener("submit", function (event) {
    event.preventDefault(); // Prevent default form submission

    var email = document.querySelector("#loginModal #email").value;
    var password = document.querySelector("#loginModal #password").value;

// Retrieve stored credentials from localStorage
var storedEmail = localStorage.getItem('userEmail');
var storedPassword = localStorage.getItem('userPassword');

   // Check if the entered credentials match the stored credentials
   if (email === storedEmail && password === storedPassword) {
    // Redirect to try.html if credentials match
    window.location.href = "try";
} else {
    // Show error message if credentials do not match
    alert("Incorrect email or password! Please try again.");
}
});
});
