// Get CSRF token from cookie
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Toggle API key field visibility
// changed to invite code lazily
const hasApiKeyCheckbox = document.getElementById('hasInviteCode');
const apiKeyGroup = document.getElementById('inviteCodeGroup');

hasApiKeyCheckbox.addEventListener('change', function() {
    if (this.checked) {
        apiKeyGroup.style.display = 'block';
    } else {
        apiKeyGroup.style.display = 'none';
    }
});

// Handle form submission
const loginForm = document.getElementById('loginForm');
const errorMessage = document.getElementById('errorMessage');

loginForm.addEventListener('submit', async function(e) {
    e.preventDefault();

    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const hasApiKey = document.getElementById('hasInviteCode').checked;
    const inviteCode = hasApiKey ? document.getElementById('inviteCode').value : null;

    // Clear previous errors
    errorMessage.classList.remove('show');
    errorMessage.textContent = '';

    try {
        const csrfToken = getCookie('csrftoken');

        const response = await fetch('/api.devpulse/signup-login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({
                email: email,
                password: password,
                invite_code: inviteCode
            })
        });

        const data = await response.json();

        if (response.ok) {
            // Redirect to dashboard on success
            window.location.href = '/devpulse/dashboard';
        } else {
            // Show error message
            errorMessage.textContent = data.error || 'An error occurred. Please try again.';
            errorMessage.classList.add('show');
        }
    } catch (error) {
        errorMessage.textContent = 'Network error. Please try again.';
        errorMessage.classList.add('show');
        console.error('Error:', error);
    }
});

// OAuth buttons (placeholder - you'll need to implement with django-allauth)
const googleBtn = document.querySelector('.btn-oauth.google');
const githubBtn = document.querySelector('.btn-oauth.github');

googleBtn.addEventListener('click', function() {
    window.location.href = '/accounts/google/login/';
});

githubBtn.addEventListener('click', function() {
    window.location.href = '/accounts/github/login/';
});