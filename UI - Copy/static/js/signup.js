document.addEventListener('DOMContentLoaded', function () {
    // Adjust font size on scroll
    window.onscroll = function () {
        var appName = document.querySelector('.app-name-container');
        var scrollPosition = window.pageYOffset;

        if (scrollPosition > 0) {
            appName.style.marginTop = '0';
            appName.style.fontSize = '50px';
        } else {
            appName.style.marginTop = '30px';
            appName.style.fontSize = '80px';
        }
    };

    // Get modal and buttons
    var signupModal = document.getElementById("signupModal");
    var signupBtn = document.getElementById("signupBtn");
    var closeSignupModal = document.getElementById("closeSignupModal");
    var signupLinkToLoginModal = document.getElementById("signupLinkToLoginModal");

    signupLinkToLoginModal.onclick = function () {
        signupModal.style.display = "none"; // Close Sign Up modal
        loginModal.style.display = "block"; // Open Login modal
    }
    // Open modal on "Sign Up" button click
    signupBtn.onclick = function () {
        signupModal.style.display = "block";
    };

    // Close modal on "X" button click
    closeSignupModal.onclick = function () {
        signupModal.style.display = "none";
    };

    // Handle the form submission
    document.querySelector("form").addEventListener("submit", function (event) {
        event.preventDefault(); // Prevent default form submission behavior
    
        
        // Get the email, password, and confirmPassword values from the form
        var name = document.querySelector("#signupModal #signupUsername").value; // Username
        var email = document.querySelector("#signupModal #signupEmail").value; // Email
        var password = document.querySelector("#signupModal #signupPassword").value; // Password
        var confirmPassword = document.querySelector("#signupModal #signupConfirmPassword").value; // Confirm Password
    
        // Validate password and confirm password
        if (password !== confirmPassword) {
            alert("Passwords do not match. Please try again.");
            return; // Stop further execution
        }
    
        // Send data to Flask backend using fetch
        fetch("http://127.0.0.1:5000/signup", {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
            },
            body: `name=${encodeURIComponent(name)}&email=${encodeURIComponent(email)}&password=${encodeURIComponent(password)}&confirmPassword=${encodeURIComponent(confirmPassword)}`
        })
        .then((response) => {
            if (!response.ok) {
                throw new Error("Network response was not ok");
            }
            return response.json();
        })
        .then((data) => {
            alert(data.message); // Show success or error message from the server
    
            // Hide the sign-up modal
            var signupModal = document.getElementById("signupModal");
            signupModal.style.display = "none";
    
            // Display the success modal
            if (data.message === "Sign up successful!") {
                var successModal = document.getElementById("successModal");
                successModal.style.display = "block";

                localStorage.setItem("userEmail", email);
                localStorage.setItem("userPassword", password); // In real apps, consider encrypting passwords!
            }
        })
        .catch((error) => {
            alert("There was a problem with the signup process: " + error.message);
        });
    });
    
    // Close the success modal when "X" is clicked
    var closeSuccessModal = document.getElementById("closeSuccessModal");
    closeSuccessModal.onclick = function () {
        document.getElementById("successModal").style.display = "none";
    };
});