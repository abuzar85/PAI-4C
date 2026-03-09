class WaterJug3D {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        this.width = this.container.clientWidth;
        this.height = this.container.clientHeight;

        this.scene = new THREE.Scene();
        this.camera = new THREE.PerspectiveCamera(45, this.width / this.height, 0.1, 1000);
        this.renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });

        this.renderer.setSize(this.width, this.height);
        this.renderer.setPixelRatio(window.devicePixelRatio);
        this.container.appendChild(this.renderer.domElement);

        this.setupLights();
        this.setupJugs();

        this.camera.position.z = 12;
        this.camera.position.y = 2;

        this.animate();

        window.addEventListener('resize', () => this.onWindowResize());
    }

    setupLights() {
        const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
        this.scene.add(ambientLight);

        const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
        directionalLight.position.set(5, 10, 7.5);
        this.scene.add(directionalLight);

        const pointLight = new THREE.PointLight(0x3b82f6, 1, 100);
        pointLight.position.set(-5, 5, 5);
        this.scene.add(pointLight);
    }

    setupJugs() {
        this.jugs = [];
        this.waterLevels = [];

        // Material for the glass jug
        const glassMaterial = new THREE.MeshPhongMaterial({
            color: 0xffffff,
            transparent: true,
            opacity: 0.2,
            shininess: 100,
            side: THREE.DoubleSide
        });

        // Material for the water
        const waterMaterial = new THREE.MeshPhongMaterial({
            color: 0x3b82f6,
            transparent: true,
            opacity: 0.7,
            shininess: 100
        });

        const jugSpacing = 4;

        for (let i = 0; i < 2; i++) {
            const group = new THREE.Group();
            group.position.x = (i === 0 ? -1 : 1) * (jugSpacing / 2);

            // Jug Body (Glass)
            const geometry = new THREE.CylinderGeometry(1, 1, 3, 32, 1, true);
            const jug = new THREE.Mesh(geometry, glassMaterial);
            group.add(jug);

            // Jug Bottom
            const bottomGeo = new THREE.CircleGeometry(1, 32);
            bottomGeo.rotateX(Math.PI / 2);
            const bottom = new THREE.Mesh(bottomGeo, glassMaterial);
            bottom.position.y = -1.5;
            group.add(bottom);

            // Water
            const waterGeo = new THREE.CylinderGeometry(0.98, 0.98, 3, 32);
            const water = new THREE.Mesh(waterGeo, waterMaterial);
            water.position.y = -1.5; // Start from bottom
            water.scale.set(1, 0.001, 1); // Initially empty
            group.add(water);

            this.scene.add(group);
            this.jugs.push(group);
            this.waterLevels.push(water);
        }
    }

    updateWaterLevels(j1, j1Cap, j2, j2Cap) {
        // Levels should be between 0 and 1
        const level1 = j1 / j1Cap;
        const level2 = j2 / j2Cap;

        this.animateWater(0, level1);
        this.animateWater(1, level2);
    }

    animateWater(index, targetLevel) {
        const water = this.waterLevels[index];
        const currentScale = water.scale.y;

        gsap.to(water.scale, {
            y: Math.max(0.001, targetLevel),
            duration: 1,
            ease: "power2.inOut",
            onUpdate: () => {
                // Adjust position so it grows from bottom
                // scale.y * 3 is the actual height.
                // At scale 1, pos.y is 0.
                // At scale 0, pos.y is -1.5.
                // Position Y = -1.5 + (height/2)
                water.position.y = -1.5 + (water.scale.y * 1.5);
            }
        });
    }

    animate() {
        requestAnimationFrame(() => this.animate());
        this.renderer.render(this.scene, this.camera);

        // Gentle rotation
        this.jugs.forEach((jug, i) => {
            jug.rotation.y += 0.005;
        });
    }

    onWindowResize() {
        this.width = this.container.clientWidth;
        this.height = this.container.clientHeight;
        this.camera.aspect = this.width / this.height;
        this.camera.updateProjectionMatrix();
        this.renderer.setSize(this.width, this.height);
    }
}
