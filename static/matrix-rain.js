// Matrix Rain Effect for Hacker Terminal
function createMatrixRain() {
    const canvas = document.createElement('canvas');
    canvas.id = 'matrix-rain';
    canvas.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: -2;
        background: #000000;
    `;
    
    // Remove existing canvas if any
    const existingCanvas = document.getElementById('matrix-rain');
    if (existingCanvas) {
        existingCanvas.remove();
    }
    
    document.body.insertBefore(canvas, document.body.firstChild);
    
    const ctx = canvas.getContext('2d');
    
    // Resize canvas
    function resizeCanvas() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    }
    
    resizeCanvas();
    window.addEventListener('resize', resizeCanvas);
    
    // Matrix characters
    const matrix = "ABCDEFGHIJKLMNOPQRSTUVWXYZ123456789@#$%^&*()*&^%+-/~{[|`]}";
    const matrixArray = matrix.split("");
    
    const fontSize = 14;
    const columns = canvas.width / fontSize;
    
    const drops = [];
    for (let x = 0; x < columns; x++) {
        drops[x] = 1;
    }
    
    function draw() {
        // Black background with slight transparency for trail effect
        ctx.fillStyle = 'rgba(0, 0, 0, 0.04)';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        
        ctx.fillStyle = '#00ff41';
        ctx.font = fontSize + 'px Fira Code, monospace';
        
        for (let i = 0; i < drops.length; i++) {
            const text = matrixArray[Math.floor(Math.random() * matrixArray.length)];
            ctx.fillText(text, i * fontSize, drops[i] * fontSize);
            
            if (drops[i] * fontSize > canvas.height && Math.random() > 0.975) {
                drops[i] = 0;
            }
            drops[i]++;
        }
    }
    
    setInterval(draw, 50);
}

// Terminal Boot Sequence
function showBootSequence() {
    const bootMessages = [
        "INITIALIZING HACKER TERMINAL...",
        "LOADING YOUTUBE DOWNLOADER MODULE...",
        "ESTABLISHING SECURE CONNECTION...",
        "BYPASSING FIREWALLS...",
        "ACCESSING DARK WEB PROTOCOLS...",
        "SYSTEM READY FOR OPERATION",
        "",
        "WARNING: UNAUTHORIZED ACCESS DETECTED",
        "COUNTER-SURVEILLANCE ACTIVATED",
        "",
        "[SYSTEM] YouTube Download Engine Online",
        "[SYSTEM] Ready for commands..."
    ];
    
    const bootContainer = document.createElement('div');
    bootContainer.id = 'boot-sequence';
    bootContainer.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: #000000;
        color: #00ff41;
        font-family: 'Fira Code', monospace;
        font-size: 14px;
        padding: 2rem;
        z-index: 9999;
        overflow: hidden;
    `;
    
    document.body.appendChild(bootContainer);
    
    let messageIndex = 0;
    
    function typeMessage() {
        if (messageIndex < bootMessages.length) {
            const message = bootMessages[messageIndex];
            const messageLine = document.createElement('div');
            messageLine.style.cssText = `
                margin: 0.2rem 0;
                animation: typewriter 0.5s steps(${message.length}) forwards;
                overflow: hidden;
                white-space: nowrap;
                width: 0;
            `;
            messageLine.textContent = message;
            bootContainer.appendChild(messageLine);
            
            // Add CSS animation
            if (!document.getElementById('typewriter-style')) {
                const style = document.createElement('style');
                style.id = 'typewriter-style';
                style.textContent = `
                    @keyframes typewriter {
                        from { width: 0; }
                        to { width: 100%; }
                    }
                `;
                document.head.appendChild(style);
            }
            
            messageIndex++;
            setTimeout(typeMessage, 600);
        } else {
            setTimeout(() => {
                bootContainer.style.animation = 'fadeOut 1s forwards';
                setTimeout(() => {
                    bootContainer.remove();
                }, 1000);
            }, 2000);
        }
    }
    
    // Add fade out animation
    if (!document.getElementById('fadeout-style')) {
        const style = document.createElement('style');
        style.id = 'fadeout-style';
        style.textContent = `
            @keyframes fadeOut {
                to { opacity: 0; }
            }
        `;
        document.head.appendChild(style);
    }
    
    typeMessage();
}

// Command Line Simulation
function simulateCommand(command, output) {
    const commandLine = document.createElement('div');
    commandLine.className = 'command-simulation';
    commandLine.style.cssText = `
        font-family: 'Fira Code', monospace;
        color: #00ff41;
        margin: 0.5rem 0;
        font-size: 0.9rem;
    `;
    
    commandLine.innerHTML = `
        <span style="color: #00aa33;">root@hacker:~$</span> ${command}<br>
        <span style="color: #00ff41;">${output}</span>
    `;
    
    return commandLine;
}

// Glitch Effect
function addGlitchEffect() {
    const glitchStyle = document.createElement('style');
    glitchStyle.id = 'glitch-effects';
    glitchStyle.textContent = `
        .glitch {
            position: relative;
            animation: glitch-skew 1s infinite linear alternate-reverse;
        }
        
        .glitch::before,
        .glitch::after {
            content: attr(data-text);
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
        }
        
        .glitch::before {
            animation: glitch-anim-1 0.5s infinite linear alternate-reverse;
            color: #ff0040;
            z-index: -1;
        }
        
        .glitch::after {
            animation: glitch-anim-2 1s infinite linear alternate-reverse;
            color: #00ffff;
            z-index: -2;
        }
        
        @keyframes glitch-anim-1 {
            0% { transform: translate(0); }
            20% { transform: translate(-2px, 2px); }
            40% { transform: translate(-2px, -2px); }
            60% { transform: translate(2px, 2px); }
            80% { transform: translate(2px, -2px); }
            100% { transform: translate(0); }
        }
        
        @keyframes glitch-anim-2 {
            0% { transform: translate(0); }
            20% { transform: translate(2px, -2px); }
            40% { transform: translate(2px, 2px); }
            60% { transform: translate(-2px, -2px); }
            80% { transform: translate(-2px, 2px); }
            100% { transform: translate(0); }
        }
        
        @keyframes glitch-skew {
            0% { transform: skew(0deg); }
            10% { transform: skew(-1deg); }
            20% { transform: skew(1deg); }
            30% { transform: skew(0deg); }
            40% { transform: skew(1deg); }
            50% { transform: skew(-1deg); }
            60% { transform: skew(0deg); }
            70% { transform: skew(-1deg); }
            80% { transform: skew(1deg); }
            90% { transform: skew(0deg); }
            100% { transform: skew(0deg); }
        }
    `;
    
    if (!document.getElementById('glitch-effects')) {
        document.head.appendChild(glitchStyle);
    }
}

// Initialize everything
function initializeHackerTerminal() {
    // Show boot sequence first
    showBootSequence();
    
    // Start matrix rain after boot
    setTimeout(() => {
        createMatrixRain();
        addGlitchEffect();
    }, 8000);
    
    // Add random glitch effects to elements
    setInterval(() => {
        const elements = document.querySelectorAll('h1, h2, h3');
        elements.forEach(el => {
            if (Math.random() < 0.1) {
                el.classList.add('glitch');
                el.setAttribute('data-text', el.textContent);
                setTimeout(() => {
                    el.classList.remove('glitch');
                }, 2000);
            }
        });
    }, 5000);
}

// Auto-start when page loads
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeHackerTerminal);
} else {
    initializeHackerTerminal();
}

// Add typing sound effect simulation
function addTypingEffect() {
    document.addEventListener('keypress', function() {
        // Visual feedback for typing
        if (Math.random() < 0.3) {
            const flash = document.createElement('div');
            flash.style.cssText = `
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0, 255, 65, 0.02);
                pointer-events: none;
                z-index: 999;
                animation: flashFade 0.1s ease-out forwards;
            `;
            
            document.body.appendChild(flash);
            
            setTimeout(() => flash.remove(), 100);
        }
    });
    
    // Add flash animation
    if (!document.getElementById('flash-style')) {
        const flashStyle = document.createElement('style');
        flashStyle.id = 'flash-style';
        flashStyle.textContent = `
            @keyframes flashFade {
                0% { opacity: 1; }
                100% { opacity: 0; }
            }
        `;
        document.head.appendChild(flashStyle);
    }
}

addTypingEffect();