---
name: threejs
description: >
  Three.js (r186) para 3D en web: escena, cámara y renderer, geometría,
  materiales/PBR, luces y sombras, texturas, loaders GLTF/DRACO, animación,
  interacción/raycasting, shaders GLSL y TSL/WebGPU, postprocesado, performance
  y React Three Fiber. Úsala para visores 3D, configuradores, landings 3D,
  juegos web y escenas interactivas.
---

# Three.js

Base: three.js **r186** (WebGLRenderer; WebGPU/TSL cuando se indique). Las referencias completas están troceadas en `references/` (≤7 KB por trozo, por el presupuesto de herramientas de DSH). Lee solo el trozo que necesites.

## Reglas de oro

- Un solo bucle: `renderer.setAnimationLoop(fn)`; no mezcles `requestAnimationFrame` con renders manuales.
- Color y tono: `renderer.outputColorSpace = THREE.SRGBColorSpace` y `renderer.toneMapping = THREE.ACESFilmicToneMapping` salvo que el diseño pida otra cosa.
- DPR: `renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2))`.
- `resize`: actualiza `camera.aspect`, `camera.updateProjectionMatrix()` y `renderer.setSize`.
- Limpia al desmontar: `geometry.dispose()`, `material.dispose()`, `texture.dispose()`, `renderer.dispose()`. En R3F el reconciler hace el cleanup.
- Nada de asignar objetos/texturas en el loop: reutiliza `Vector3`, materiales y geometrías.
- GLTF: `GLTFLoader` (+ `DRACOLoader`/meshopt si aplica), `scene.traverse` para sombras y `castShadow`/`receiveShadow` selectivos.
- Sombras: solo luces necesarias, `shadow.mapSize` 1024–2048 y `shadow.camera` ajustada.
- Instancing para >100 objetos repetidos; LOD y frustum culling; limita draw calls y tamaño de texturas.
- Shaders/postprocesado: mide el coste; evita passes a pantalla completa innecesarios. En WebGPU usa TSL.
- Verifica en navegador real (consola, WebGL errors, FPS, peso del bundle); que compile no significa que funcione.

## Quick start

```javascript
import * as THREE from "three";

const renderer = new THREE.WebGLRenderer({ antialias: true, powerPreference: "high-performance" });
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
document.body.appendChild(renderer.domElement);

const scene = new THREE.Scene();
scene.background = new THREE.Color(0x111318);

const camera = new THREE.PerspectiveCamera(50, window.innerWidth / window.innerHeight, 0.1, 200);
camera.position.set(3, 2, 5);
camera.lookAt(0, 1, 0);

scene.add(new THREE.AmbientLight(0xffffff, 0.4));
const key = new THREE.DirectionalLight(0xffffff, 2);
key.position.set(4, 6, 3);
key.castShadow = true;
scene.add(key);

const mesh = new THREE.Mesh(
  new THREE.BoxGeometry(1, 1, 1),
  new THREE.MeshStandardMaterial({ color: 0x3a86ff, roughness: 0.4, metalness: 0.1 }),
);
mesh.castShadow = true;
mesh.position.y = 1;
scene.add(mesh);
scene.add(new THREE.Mesh(new THREE.PlaneGeometry(20, 20), new THREE.MeshStandardMaterial({ color: 0x222222 })).rotateX(-Math.PI / 2));

const timer = new THREE.Timer();
timer.connect(document);
renderer.setAnimationLoop(() => {
  timer.update();
  mesh.rotation.y += timer.getDelta();
  renderer.render(scene, camera);
});

window.addEventListener("resize", () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});
```

## Referencias (lee solo lo necesario)

| Tarea | Referencia |
|---|---|
| Escena, cámara, renderer, transformadas, math, cleanup | `references/fundamentals-*.md` |
| Geometría, BufferGeometry, instancing | `references/geometry-*.md` |
| Materiales PBR/basic/phong, props | `references/materials-*.md` |
| Texturas, UVs, cubemaps, HDR, color space | `references/textures-*.md` |
| Luces, sombras, IBL | `references/lighting-*.md` |
| GLTF/texturas/assets, carga asíncrona | `references/loaders-*.md` |
| Pipeline de assets (compresión, DRACO/meshopt, optimización) | `references/asset-pipeline-*.md` |
| Animación: keyframes, skeletal, morph, mezcla, GLTF clips | `references/animation-*.md` |
| Interacción: raycasting, controls, puntero/touch | `references/interaction-*.md` |
| Shaders GLSL, ShaderMaterial, uniforms | `references/shaders-*.md` |
| Postprocesado: EffectComposer, bloom, DOF | `references/postprocessing-*.md` |
| Rendimiento: draw calls, memoria, profiling | `references/performance-*.md` |
| React Three Fiber | `references/react-three-fiber-*.md` |

Cada tema tiene `-1`, `-2`…; empieza por `-1` y sigue si hace falta. `references/SOURCE.md` guarda la versión upstream.

## Flujo de trabajo

1. Identifica la tarea y lee el `-1` del tema (y el siguiente solo si el `-1` no basta).
2. Copia el patrón del ejemplo, adapta y **mide** (FPS, draw calls, memoria, peso).
3. Verifica en navegador con `playwright`/`webapp-testing` o `browseros-neo`; revisa consola y errores WebGL.
4. Para dudas de timing/interacción, combina con `motion-design` y `ui-animation`.

## Errores típicos

- Contexto WebGL perdido por no liberar recursos al desmontar.
- Escena negra por falta de luz o color space mal configurado.
- Sombras que no aparecen: `castShadow` en malla, `receiveShadow` en suelo y luz con `castShadow`.
- Texturas lavadas: `texture.colorSpace = THREE.SRGBColorSpace` en mapas de color.
- Jank por crear geometrías/materiales dentro del frame.
- Modelos GLTF gigantes sin compresión ni LOD.
- Varios `WebGLRenderer` en la misma página compitiendo por el contexto.
