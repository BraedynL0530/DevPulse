// CSRF Token Helper
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

const csrfToken = getCookie('csrftoken');

// State
let currentDeleteProjectId = null;

// DOM Elements
const userMenuBtn = document.getElementById('userMenuBtn');
const userMenu = document.getElementById('userMenu');
const createProjectBtn = document.getElementById('createProjectBtn');
const createProjectModal = document.getElementById('createProjectModal');
const apiKeyModal = document.getElementById('apiKeyModal');
const inviteModal = document.getElementById('inviteModal');
const deleteModal = document.getElementById('deleteModal');

// User Menu Dropdown
userMenuBtn?.addEventListener('click', (e) => {
    e.stopPropagation();
    userMenu.classList.toggle('show');
});

document.addEventListener('click', () => {
    userMenu?.classList.remove('show');
    // Close all project dropdowns
    document.querySelectorAll('.project-dropdown').forEach(d => {
        d.classList.remove('show');
    });
});

// Generate API Key
document.getElementById('generateKeyBtn')?.addEventListener('click', async (e) => {
    e.preventDefault();
    try {
        const response = await fetch('/api.devpulse/proxy-path', {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken
            }
        });

        const data = await response.json();

        if (response.ok) {
            document.getElementById('generatedKey').value = data.key;
            apiKeyModal.classList.add('show');
        } else {
            alert('Error generating API key: ' + (data.error || 'Unknown error'));
        }
    } catch (error) {
        alert('Network error: ' + error.message);
    }
});

// Copy API Key
document.getElementById('copyKeyBtn')?.addEventListener('click', () => {
    const keyInput = document.getElementById('generatedKey');
    keyInput.select();
    navigator.clipboard.writeText(keyInput.value);

    const btn = document.getElementById('copyKeyBtn');
    btn.textContent = 'Copied!';
    setTimeout(() => btn.textContent = 'Copy', 1500);
});

// Close API Key Modal
document.getElementById('closeKeyModal')?.addEventListener('click', () => {
    apiKeyModal.classList.remove('show');
});

document.getElementById('closeKeyModalBtn')?.addEventListener('click', () => {
    apiKeyModal.classList.remove('show');
});

// View Invite Code
document.getElementById('viewInviteBtn')?.addEventListener('click', (e) => {
    e.preventDefault();
    inviteModal.classList.add('show');
});

// Copy Invite Code
document.getElementById('copyInviteBtn')?.addEventListener('click', () => {
    const inviteInput = document.getElementById('inviteCode');
    inviteInput.select();
    navigator.clipboard.writeText(inviteInput.value);

    const btn = document.getElementById('copyInviteBtn');
    btn.textContent = 'Copied!';
    setTimeout(() => btn.textContent = 'Copy', 1500);
});

// Close Invite Modal
document.getElementById('closeInviteModal')?.addEventListener('click', () => {
    inviteModal.classList.remove('show');
});

document.getElementById('closeInviteModalBtn')?.addEventListener('click', () => {
    inviteModal.classList.remove('show');
});

// Create Project Modal
createProjectBtn?.addEventListener('click', () => {
    createProjectModal.classList.add('show');
});

document.getElementById('closeCreateModal')?.addEventListener('click', () => {
    createProjectModal.classList.remove('show');
});

document.getElementById('cancelCreate')?.addEventListener('click', () => {
    createProjectModal.classList.remove('show');
});

// Create Project Form
document.getElementById('createProjectForm')?.addEventListener('submit', async (e) => {
    e.preventDefault();

    const projectName = document.getElementById('projectName').value;

    try {
        const response = await fetch('/api.devpulse/create-project', { // not added yet
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({ name: projectName })
        });

        const data = await response.json();

        if (response.ok) {
            createProjectModal.classList.remove('show');
            document.getElementById('projectName').value = '';
            // Reload page to show new project
            window.location.reload();
        } else {
            alert('Error creating project: ' + (data.error || 'Unknown error'));
        }
    } catch (error) {
        alert('Network error: ' + error.message);
    }
});

// Delete Project Modal
document.getElementById('closeDeleteModal')?.addEventListener('click', () => {
    deleteModal.classList.remove('show');
});

document.getElementById('cancelDelete')?.addEventListener('click', () => {
    deleteModal.classList.remove('show');
});

document.getElementById('confirmDelete')?.addEventListener('click', async () => {
    if (!currentDeleteProjectId) return;

    try {
        const response = await fetch(`/api.devpulse/delete-project/${currentDeleteProjectId}`, { // not added yet
            method: 'DELETE',
            headers: {
                'X-CSRFToken': csrfToken
            }
        });

        if (response.ok) {
            deleteModal.classList.remove('show');
            // Reload page to remove deleted project
            window.location.reload();
        } else {
            const data = await response.json();
            alert('Error deleting project: ' + (data.error || 'Unknown error'));
        }
    } catch (error) {
        alert('Network error: ' + error.message);
    }
});

// Toggle Project Actions Dropdown
function toggleProjectActions(projectId) {
    event.stopPropagation();
    const dropdown = document.getElementById(`dropdown-${projectId}`);

    // Close all other dropdowns
    document.querySelectorAll('.project-dropdown').forEach(d => {
        if (d.id !== `dropdown-${projectId}`) {
            d.classList.remove('show');
        }
    });

    dropdown.classList.toggle('show');
}

// Delete Project
function deleteProject(projectId, projectName) {
    currentDeleteProjectId = projectId;
    document.getElementById('deleteProjectName').textContent = projectName;
    deleteModal.classList.add('show');
}

// Utility Functions
function formatNumber(num) {
    if (num >= 1000000) return (num / 1000000).toFixed(1) + 'M';
    if (num >= 1000) return (num / 1000).toFixed(1) + 'K';
    return num.toString();
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}