/* default dom id (particles-js) */
//particlesJS();

/* config dom id */
//particlesJS('dom-id');

/* config dom id (optional) + config particles params */
particlesJS('particles-js', {
    particles: {
        color: '#fff',
        shape: 'circle',
        opacity: 1,
        size: 2,
        size_random: true,
        nb: 100,
        line_linked: {
            enable_auto: true,
            distance:250,
            color: '#fff',
            opacity: 0.4,
            width: 0.5,
            condensed_mode: {
                enable: false,
                rotateX: 600,
                rotateY: 600
            }
        },
        anim: {
            enable: true,
            speed: 2
        }
    },
    interactivity: {
        enable: true,
        mouse: {
            distance: 400
        },
        mode: 'grab'
    },
    retina_detect: true
});
