/**
 * Madiha's Cartoon Portfolio - Frontend JavaScript
 * Connects to Flask backend API
 */

const API_BASE = 'http://localhost:5001/api';

// ============ DOM Elements ============
const skillsGrid = document.getElementById('skillsGrid');
const projectsGrid = document.getElementById('projectsGrid');
const contactForm = document.getElementById('contactForm');
const formMessage = document.getElementById('formMessage');
const visitorCount = document.getElementById('visitorCount');
const heroName = document.getElementById('heroName');
const heroTitle = document.getElementById('heroTitle');
const aboutText = document.getElementById('aboutText');
const contactEmail = document.getElementById('contactEmail');
const contactPhone = document.getElementById('contactPhone');
const backToTop = document.getElementById('backToTop');
const hamburger = document.querySelector('.hamburger');
const navLinks = document.querySelector('.nav-links');

// ============ Initialize ============
document.addEventListener('DOMContentLoaded', () => {
    loadProfile();
    loadSkills();
    loadProjects();
    incrementVisitors();
    setupEventListeners();
});

// ============ API Functions ============

// Load Profile Data
async function loadProfile() {
    try {
        const response = await fetch(`${API_BASE}/profile`);
        if (response.ok) {
            const profile = await response.json();
            if (heroName) heroName.textContent = profile.name;
            if (heroTitle) heroTitle.textContent = profile.title;
            if (aboutText) aboutText.innerHTML = profile.about;
            if (contactEmail) {
                contactEmail.textContent = profile.email;
                contactEmail.href = `mailto:${profile.email}`;
            }
            if (contactPhone) {
                contactPhone.textContent = profile.phone;
                contactPhone.href = `tel:${profile.phone}`;
            }
        }
    } catch (error) {
        console.log('Using default profile data');
    }
}

// Load Skills
async function loadSkills() {
    if (!skillsGrid) return;
    
    skillsGrid.innerHTML = '<div class="loading"></div>';
    
    try {
        const response = await fetch(`${API_BASE}/skills`);
        if (response.ok) {
            const skills = await response.json();
            renderSkills(skills);
        } else {
            renderDefaultSkills();
        }
    } catch (error) {
        console.log('Using default skills');
        renderDefaultSkills();
    }
}

function renderSkills(skills) {
    skillsGrid.innerHTML = skills.map(skill => `
        <div class="skill-card" style="--skill-color: ${skill.color}">
            <span class="skill-emoji">${skill.emoji}</span>
            <h3>${skill.name}</h3>
            <div class="skill-bar">
                <div class="skill-progress" style="--progress: ${skill.proficiency}%"></div>
            </div>
            <span class="skill-percent">${skill.proficiency}%</span>
        </div>
    `).join('');
    
    // Trigger animation
    setTimeout(() => {
        document.querySelectorAll('.skill-progress').forEach(bar => {
            bar.style.animation = 'fillBar 1.5s ease-out forwards';
        });
    }, 100);
}

function renderDefaultSkills() {
    const defaultSkills = [
        { name: 'HTML5', emoji: '🌐', color: '#e34c26', proficiency: 85 },
        { name: 'CSS3', emoji: '🎨', color: '#264de4', proficiency: 80 },
        { name: 'Java', emoji: '☕', color: '#f89820', proficiency: 75 },
        { name: 'Python', emoji: '🐍', color: '#3776ab', proficiency: 70 }
    ];
    renderSkills(defaultSkills);
}

// Load Projects
async function loadProjects() {
    if (!projectsGrid) return;
    
    projectsGrid.innerHTML = '<div class="loading"></div>';
    
    try {
        const response = await fetch(`${API_BASE}/projects`);
        if (response.ok) {
            const projects = await response.json();
            renderProjects(projects);
        } else {
            renderDefaultProjects();
        }
    } catch (error) {
        console.log('Using default projects');
        renderDefaultProjects();
    }
}

function renderProjects(projects) {
    projectsGrid.innerHTML = projects.map(project => `
        <div class="project-card">
            <img src="${project.image_url}" alt="${project.title}" class="project-image" 
                 onerror="this.src='https://images.unsplash.com/photo-1517694712202-14dd9538aa97?w=400'">
            <div class="project-content">
                <h3 class="project-title">${project.title}</h3>
                <p class="project-desc">${project.description}</p>
                <div class="project-tech">
                    ${project.technologies.split(',').map(tech => 
                        `<span class="tech-tag">${tech.trim()}</span>`
                    ).join('')}
                </div>
            </div>
        </div>
    `).join('');
}

function renderDefaultProjects() {
    const defaultProjects = [
        {
            title: 'Portfolio Website 🎨',
            description: 'A fun cartoon-themed portfolio with playful animations!',
            technologies: 'HTML,CSS,JavaScript,Python',
            image_url: 'https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=400'
        },
        {
            title: 'Calculator App 🔢',
            description: 'A colorful calculator with basic and scientific operations.',
            technologies: 'HTML,CSS,JavaScript',
            image_url: 'https://images.unsplash.com/photo-1587145820266-a5951ee6f620?w=400'
        },
        {
            title: 'To-Do List 📝',
            description: 'A cute task manager to organize daily activities!',
            technologies: 'HTML,CSS,JavaScript',
            image_url: 'https://images.unsplash.com/photo-1484480974693-6ca0a78fb36b?w=400'
        }
    ];
    renderProjects(defaultProjects);
}

// Visitor Counter
async function incrementVisitors() {
    try {
        const response = await fetch(`${API_BASE}/visitors/increment`, {
            method: 'POST'
        });
        if (response.ok) {
            const data = await response.json();
            animateCounter(data.count);
        }
    } catch (error) {
        // Animate with a default value if API fails
        animateCounter(Math.floor(Math.random() * 100) + 50);
    }
}

function animateCounter(target) {
    if (!visitorCount) return;
    
    let current = 0;
    const increment = Math.ceil(target / 50);
    const timer = setInterval(() => {
        current += increment;
        if (current >= target) {
            current = target;
            clearInterval(timer);
        }
        visitorCount.textContent = current;
    }, 30);
}

// Contact Form
async function submitContact(formData) {
    try {
        const response = await fetch(`${API_BASE}/contact`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });
        
        const data = await response.json();
        
        if (response.ok) {
            showMessage('success', '🎉 Message sent successfully! Thank you! 💖');
            contactForm.reset();
        } else {
            showMessage('error', data.error || '😢 Something went wrong. Please try again!');
        }
    } catch (error) {
        showMessage('error', '😢 Could not connect to server. Please try again later!');
    }
}

function showMessage(type, message) {
    formMessage.className = `form-message ${type}`;
    formMessage.textContent = message;
    
    setTimeout(() => {
        formMessage.className = 'form-message';
        formMessage.textContent = '';
    }, 5000);
}

// ============ Event Listeners ============
function setupEventListeners() {
    // Contact Form Submit
    if (contactForm) {
        contactForm.addEventListener('submit', (e) => {
            e.preventDefault();
            
            const formData = {
                name: document.getElementById('name').value,
                email: document.getElementById('email').value,
                message: document.getElementById('message').value
            };
            
            submitContact(formData);
        });
    }
    
    // Back to Top Button
    window.addEventListener('scroll', () => {
        if (window.scrollY > 500) {
            backToTop.classList.add('visible');
        } else {
            backToTop.classList.remove('visible');
        }
    });
    
    if (backToTop) {
        backToTop.addEventListener('click', () => {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }
    
    // Mobile Navigation
    if (hamburger) {
        hamburger.addEventListener('click', () => {
            hamburger.classList.toggle('active');
            navLinks.classList.toggle('active');
        });
    }
    
    // Close mobile nav when clicking a link
    document.querySelectorAll('.nav-links a').forEach(link => {
        link.addEventListener('click', () => {
            hamburger.classList.remove('active');
            navLinks.classList.remove('active');
        });
    });
    
    // Smooth scroll for navigation
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                const offsetTop = target.offsetTop - 80;
                window.scrollTo({
                    top: offsetTop,
                    behavior: 'smooth'
                });
            }
        });
    });
    
    // Intersection Observer for animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);
    
    // Observe sections for scroll animations
    document.querySelectorAll('.section').forEach(section => {
        section.style.opacity = '0';
        section.style.transform = 'translateY(30px)';
        section.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(section);
    });
}

// ============ Fun Extras ============

// Add sparkle effect on click
document.addEventListener('click', (e) => {
    createSparkle(e.clientX, e.clientY);
});

function createSparkle(x, y) {
    const sparkles = ['✨', '⭐', '💖', '🌟', '💫'];
    const sparkle = document.createElement('div');
    sparkle.textContent = sparkles[Math.floor(Math.random() * sparkles.length)];
    sparkle.style.cssText = `
        position: fixed;
        left: ${x}px;
        top: ${y}px;
        font-size: 1.5rem;
        pointer-events: none;
        z-index: 9999;
        animation: sparkleAnim 1s ease-out forwards;
    `;
    
    document.body.appendChild(sparkle);
    
    setTimeout(() => sparkle.remove(), 1000);
}

// Add sparkle animation style
const style = document.createElement('style');
style.textContent = `
    @keyframes sparkleAnim {
        0% {
            opacity: 1;
            transform: scale(1) translateY(0);
        }
        100% {
            opacity: 0;
            transform: scale(0) translateY(-50px);
        }
    }
`;
document.head.appendChild(style);

// Konami Code Easter Egg
let konamiCode = [];
const konamiSequence = ['ArrowUp', 'ArrowUp', 'ArrowDown', 'ArrowDown', 'ArrowLeft', 'ArrowRight', 'ArrowLeft', 'ArrowRight', 'b', 'a'];

document.addEventListener('keydown', (e) => {
    konamiCode.push(e.key);
    konamiCode = konamiCode.slice(-10);
    
    if (konamiCode.join(',') === konamiSequence.join(',')) {
        activateRainbowMode();
    }
});

function activateRainbowMode() {
    document.body.style.animation = 'rainbow 2s linear infinite';
    const rainbowStyle = document.createElement('style');
    rainbowStyle.textContent = `
        @keyframes rainbow {
            0% { filter: hue-rotate(0deg); }
            100% { filter: hue-rotate(360deg); }
        }
    `;
    document.head.appendChild(rainbowStyle);
    
    alert('🌈 Rainbow Mode Activated! 🎉');
    
    setTimeout(() => {
        document.body.style.animation = '';
    }, 10000);
}

console.log('🎀 Madiha\'s Portfolio Loaded! ✨');
console.log('💡 Tip: Try the Konami Code for a surprise!');
