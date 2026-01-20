import React, { useRef, useMemo } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { Sphere, MeshDistortMaterial, OrbitControls } from '@react-three/drei';

const PulseSphere = ({ status }) => {
    const meshRef = useRef();
    const isCritical = status.high_severity > 0;

    // Pulse speed based on severity
    const speed = isCritical ? 6 : status.medium_severity > 0 ? 3 : 1.5;
    const color = isCritical ? "#ff003c" : status.medium_severity > 0 ? "#fcee0a" : "#00ff9d";

    useFrame((state) => {
        if (!meshRef.current) return;
        const time = state.clock.getElapsedTime();

        // Rotation
        meshRef.current.rotation.y = time * 0.2;
        meshRef.current.rotation.z = time * 0.1;

        // Scale pulse
        const s = 1 + Math.sin(time * speed) * 0.05;
        meshRef.current.scale.set(s, s, s);
    });

    return (
        <Sphere ref={meshRef} args={[1, 32, 32]}>
            <MeshDistortMaterial
                color={color}
                wireframe
                distort={isCritical ? 0.4 : 0.2}
                speed={speed}
                opacity={0.6}
                transparent
            />
        </Sphere>
    );
};

const SystemStatus3D = ({ stats }) => {
    return (
        <div className="w-full h-48 bg-cyber-dark rounded-xl border border-cyber-border overflow-hidden relative cursor-grab active:cursor-grabbing">
            <div className="absolute top-4 left-4 z-10">
                <h4 className="text-[10px] font-mono text-slate-500 uppercase tracking-widest">
                    Kernel_Integrity_Mesh
                </h4>
            </div>

            <Canvas camera={{ position: [0, 0, 3], fov: 45 }}>
                <ambientLight intensity={0.5} />
                <pointLight position={[10, 10, 10]} intensity={1} color="#00f0ff" />
                <PulseSphere status={stats} />
                <OrbitControls enableZoom={false} />
            </Canvas>

            <div className="absolute bottom-4 right-4 z-10 text-right">
                <span className={`text-[10px] font-mono font-bold ${stats.high_severity > 0 ? 'text-cyber-alert' : 'text-cyber-primary'}`}>
                    {stats.high_severity > 0 ? 'STATUS: CRITICAL' : 'STATUS: STABLE'}
                </span>
            </div>
        </div>
    );
};

export default SystemStatus3D;
