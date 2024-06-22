import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

const renderer = new THREE.WebGLRenderer({

  alpha: true,

})

renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

const scene = new THREE.Scene();

const camera = new THREE.PerspectiveCamera(30, window.innerWidth / window.innerHeight, 5, 2000);
camera.position.set(-10, 210, 110);

const controls = new OrbitControls(camera, renderer.domElement);
controls.minDistance = 0;
controls.maxDistance = 30;
controls.minPolarAngle = 1;
controls.maxPolarAngle =1;
controls.target = new THREE.Vector3(0, 0, 0);
controls.update();

const ambientLight = new THREE.AmbientLight(0xffffff);
scene.add(ambientLight);
const loader = new GLTFLoader().setPath('../static/three-d-models/alpaca/');
loader.load('scene.gltf', (gltf) => {
  console.log('loading model');
  const mesh = gltf.scene;
  mesh.traverse((child) => {
    if (child.isMesh) {
      child.castShadow = true;
      child.receiveShadow = true;
    }
  });
  mesh.scale.set(6, 6, 6);
  mesh.rotation.y = THREE.MathUtils.degToRad(-25);
  scene.add(mesh);

});

function animate() {
  requestAnimationFrame(animate);
  controls.update();
  renderer.render(scene, camera);
}
animate();
