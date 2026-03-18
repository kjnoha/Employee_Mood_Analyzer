/**
 * Floating mood-particles canvas — reacts to overall team mood.
 * Particles are soft, translucent circles that drift and connect.
 */
(function () {
    const canvas = document.getElementById('particle-canvas');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');

    let W, H, particles = [];
    const PARTICLE_COUNT = 50;
    const MAX_DIST = 140;

    // Mood-driven palette (set via data attribute or default)
    const palettes = {
        positive: ['#10b981', '#34d399', '#6ee7b7'],
        negative: ['#f43f5e', '#fb7185', '#fda4af'],
        neutral: ['#06b6d4', '#22d3ee', '#67e8f9'],
        mixed: ['#818cf8', '#a78bfa', '#c4b5fd'],
    };

    function getPalette() {
        const mood = canvas.dataset.mood || 'mixed';
        return palettes[mood] || palettes.mixed;
    }

    function resize() {
        W = canvas.width = window.innerWidth;
        H = canvas.height = window.innerHeight;
    }

    class Particle {
        constructor() {
            this.reset();
        }
        reset() {
            const palette = getPalette();
            this.x = Math.random() * W;
            this.y = Math.random() * H;
            this.r = Math.random() * 3 + 1;
            this.vx = (Math.random() - 0.5) * 0.4;
            this.vy = (Math.random() - 0.5) * 0.4;
            this.color = palette[Math.floor(Math.random() * palette.length)];
            this.alpha = Math.random() * 0.4 + 0.15;
        }
        update() {
            this.x += this.vx;
            this.y += this.vy;
            if (this.x < 0 || this.x > W) this.vx *= -1;
            if (this.y < 0 || this.y > H) this.vy *= -1;
        }
        draw() {
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.r, 0, Math.PI * 2);
            ctx.fillStyle = this.color;
            ctx.globalAlpha = this.alpha;
            ctx.fill();
            ctx.globalAlpha = 1;
        }
    }

    function init() {
        resize();
        particles = [];
        for (let i = 0; i < PARTICLE_COUNT; i++) particles.push(new Particle());
    }

    function connectParticles() {
        for (let i = 0; i < particles.length; i++) {
            for (let j = i + 1; j < particles.length; j++) {
                const dx = particles[i].x - particles[j].x;
                const dy = particles[i].y - particles[j].y;
                const dist = Math.sqrt(dx * dx + dy * dy);
                if (dist < MAX_DIST) {
                    const alpha = (1 - dist / MAX_DIST) * 0.12;
                    ctx.beginPath();
                    ctx.moveTo(particles[i].x, particles[i].y);
                    ctx.lineTo(particles[j].x, particles[j].y);
                    ctx.strokeStyle = particles[i].color;
                    ctx.globalAlpha = alpha;
                    ctx.lineWidth = 0.6;
                    ctx.stroke();
                    ctx.globalAlpha = 1;
                }
            }
        }
    }

    function animate() {
        ctx.clearRect(0, 0, W, H);
        particles.forEach(p => { p.update(); p.draw(); });
        connectParticles();
        requestAnimationFrame(animate);
    }

    window.addEventListener('resize', () => { resize(); });
    init();
    animate();

    // Expose a way to update the mood palette live
    window.updateParticleMood = function (mood) {
        canvas.dataset.mood = mood;
        particles.forEach(p => {
            const palette = getPalette();
            p.color = palette[Math.floor(Math.random() * palette.length)];
        });
    };
})();
