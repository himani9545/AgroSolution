// Check if a language preference is saved
document.addEventListener("DOMContentLoaded", function() {
    const savedLanguage = localStorage.getItem('language') || 'en';
    setLanguage(savedLanguage);

    const languageSelect = document.getElementById('languageSelect');
    if (languageSelect) {
        languageSelect.value = savedLanguage;
    }
});



// Function to change the language
function changeLanguage() {
    const selectedLang = document.getElementById('languageSelect').value;
    localStorage.setItem('language', selectedLang);
    setLanguage(selectedLang);
}

// Function to safely set text content
function updateText(selector, text) {
    const element = document.querySelector(selector);
    if (element) {
        element.innerText = text;
    }
}

// Function to safely update placeholders
function updatePlaceholder(selector, text) {
    const element = document.querySelector(selector);
    if (element) {
        element.placeholder = text;
    }
}

// Function to apply the selected language to the page
function setLanguage(lang) {
    if (lang === 'hi') {
        // Homepage text
        updateText('#tryForFreeBtn', "मुफ्त में आज़माएँ");
        updateText('#loginBtn', "लॉगिन करें");
        updateText('#signupBtn', "साइन अप करें");
        updateText('#knowAboutYourCropsBtn', "अपने फसलों के बारे में जानें");
        updateText('#aboutUsBtn', "हमारे बारे में");

        // Recommendation Page Text
        updateText('#cropRecTitle', "फसल सिफारिश");
        updateText('#cropRecDesc', "मिट्टी के प्रकार और स्थान के आधार पर व्यक्तिगत फसल सुझाव प्राप्त करें।");
        updateText('#cropRecBtn', "देखें");

        updateText('#fertilizerRecTitle', "उर्वरक सिफारिश");
        updateText('#fertilizerRecDesc', "फसल वृद्धि को प्रभावी ढंग से बढ़ाने के लिए सही उर्वरक खोजें।");
        updateText('#fertilizerRecBtn', "देखें");

        updateText('#pesticideRecTitle', "कीटनाशक सिफारिश");
        updateText('#pesticideRecDesc', "सर्वश्रेष्ठ कीटनाशकों का चयन करें और उनके अनुप्रयोग विधियों को जानें।");
        updateText('#pesticideRecBtn', "देखें");

        // For Forms (signup, login, etc.)
        updateText('#signupModal h2', "साइन अप करें");
        updatePlaceholder('#signupUsername', "अपना उपयोगकर्ता नाम दर्ज करें");
        updatePlaceholder('#signupEmail', "अपना ईमेल दर्ज करें");
        updatePlaceholder('#signupPassword', "अपना पासवर्ड दर्ज करें");
        updatePlaceholder('#signupConfirmPassword', "अपना पासवर्ड फिर से दर्ज करें");

        updateText('#loginModal h2', "लॉगिन करें");
        updatePlaceholder('#loginEmail', "अपना ईमेल दर्ज करें");
        updatePlaceholder('#loginPassword', "अपना पासवर्ड दर्ज करें");
        updateText('#cropPageHeading', "भारतीय फसलों के बारे में अधिक जानें");

    } else {
        // English Text
        updateText('#tryForFreeBtn', "Try for Free");
        updateText('#loginBtn', "Login");
        updateText('#signupBtn', "Sign Up");
        updateText('#knowAboutYourCropsBtn', "Know About Your Crops");
        updateText('#aboutUsBtn', "About Us");

        // Recommendation Page Text
        updateText('#cropRecTitle', "Crop Recommendation");
        updateText('#cropRecDesc', "Get personalized crop suggestions based on soil type and location.");
        updateText('#cropRecBtn', "Explore");

        updateText('#fertilizerRecTitle', "Fertilizer Recommendation");
        updateText('#fertilizerRecDesc', "Find the right fertilizers to enhance crop growth effectively.");
        updateText('#fertilizerRecBtn', "Explore");

        updateText('#pesticideRecTitle', "Pesticide Recommendation");
        updateText('#pesticideRecDesc', "Choose the best pesticides and learn their application methods.");
        updateText('#pesticideRecBtn', "Explore");

        // For Forms (signup, login, etc.)
        updateText('#signupModal h2', "Sign Up");
        updatePlaceholder('#signupUsername', "Enter your username");
        updatePlaceholder('#signupEmail', "Enter your email");
        updatePlaceholder('#signupPassword', "Enter your password");
        updatePlaceholder('#signupConfirmPassword', "Confirm your password");

        updateText('#loginModal h2', "Log In");
        updatePlaceholder('#loginEmail', "Enter your email");
        updatePlaceholder('#loginPassword', "Enter your password");
        updateText('#cropPageHeading', "Know More About Indian Crops");
    }
}
