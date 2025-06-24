// Particles.js configuration for fire theme
particlesJS('particles-js', {
    "particles": {
        "number": {
            "value": 100,
            "density": {
                "enable": true,
                "value_area": 800
            }
        },
        "color": {
            "value": ["#ff4444", "#ff6600", "#ffaa00", "#ff0000"]
        },
        "shape": {
            "type": "circle",
            "stroke": {
                "width": 0,
                "color": "#000000"
            },
            "polygon": {
                "nb_sides": 5
            }
        },
        "opacity": {
            "value": 0.6,
            "random": true,
            "anim": {
                "enable": true,
                "speed": 1,
                "opacity_min": 0.1,
                "sync": false
            }
        },
        "size": {
            "value": 3,
            "random": true,
            "anim": {
                "enable": true,
                "speed": 4,
                "size_min": 0.3,
                "sync": false
            }
        },
        "line_linked": {
            "enable": false
        },
        "move": {
            "enable": true,
            "speed": 2,
            "direction": "top",
            "random": true,
            "straight": false,
            "out_mode": "out",
            "bounce": false,
            "attract": {
                "enable": false,
                "rotateX": 600,
                "rotateY": 1200
            }
        }
    },
    "interactivity": {
        "detect_on": "canvas",
        "events": {
            "onhover": {
                "enable": true,
                "mode": "bubble"
            },
            "onclick": {
                "enable": true,
                "mode": "push"
            },
            "resize": true
        },
        "modes": {
            "grab": {
                "distance": 400,
                "line_linked": {
                    "opacity": 1
                }
            },
            "bubble": {
                "distance": 200,
                "size": 8,
                "duration": 2,
                "opacity": 0.8,
                "speed": 3
            },
            "repulse": {
                "distance": 200,
                "duration": 0.4
            },
            "push": {
                "particles_nb": 4
            },
            "remove": {
                "particles_nb": 2
            }
        }
    },
    "retina_detect": true
});

// Additional fire effect animations
function createFireParticle() {
    const particle = document.createElement('div');
    particle.className = 'fire-particle';
    particle.style.cssText = `
        position: fixed;
        width: 4px;
        height: 4px;
        background: radial-gradient(circle, #ff4444, #ff6600);
        border-radius: 50%;
        pointer-events: none;
        z-index: -1;
        animation: fireRise ${Math.random() * 3 + 2}s linear forwards;
        left: ${Math.random() * 100}vw;
        bottom: -10px;
    `;
    
    document.body.appendChild(particle);
    
    setTimeout(() => {
        particle.remove();
    }, 5000);
}

// Add fire particle animation keyframes
if (!document.getElementById('fire-particles-style')) {
    const style = document.createElement('style');
    style.id = 'fire-particles-style';
    style.textContent = `
        @keyframes fireRise {
            0% {
                transform: translateY(0) scale(1);
                opacity: 1;
            }
            50% {
                transform: translateY(-50vh) scale(1.2);
                opacity: 0.8;
            }
            100% {
                transform: translateY(-100vh) scale(0.5);
                opacity: 0;
            }
        }
        
        .fire-particle {
            box-shadow: 0 0 10px rgba(255, 68, 68, 0.8);
        }
    `;
    document.head.appendChild(style);
}

// Create fire particles periodically
setInterval(createFireParticle, 200);

// Add mouse trail effect
let mouseTrail = [];
document.addEventListener('mousemove', function(e) {
    mouseTrail.push({ x: e.clientX, y: e.clientY, time: Date.now() });
    
    // Limit trail length
    if (mouseTrail.length > 10) {
        mouseTrail.shift();
    }
    
    // Create trail particle
    if (Math.random() < 0.3) {
        const trailParticle = document.createElement('div');
        trailParticle.style.cssText = `
            position: fixed;
            width: 3px;
            height: 3px;
            background: radial-gradient(circle, #ff6600, transparent);
            border-radius: 50%;
            pointer-events: none;
            z-index: -1;
            left: ${e.clientX}px;
            top: ${e.clientY}px;
            animation: trailFade 1s ease-out forwards;
        `;
        document.body.appendChild(trailParticle);
        
        setTimeout(() => {
            trailParticle.remove();
        }, 1000);
    }
});

// Add trail fade animation
if (!document.getElementById('trail-style')) {
    const trailStyle = document.createElement('style');
    trailStyle.id = 'trail-style';
    trailStyle.textContent = `
        @keyframes trailFade {
            0% {
                opacity: 1;
                transform: scale(1);
            }
            100% {
                opacity: 0;
                transform: scale(0.5);
            }
        }
    `;
    document.head.appendChild(trailStyle);
}

// Add window resize handler for particles
window.addEventListener('resize', function() {
    if (window.pJSDom && window.pJSDom[0] && window.pJSDom[0].pJS) {
        window.pJSDom[0].pJS.fn.particlesRefresh();
    }
});
