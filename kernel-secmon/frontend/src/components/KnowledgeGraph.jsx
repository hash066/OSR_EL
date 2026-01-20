import React, { useCallback } from 'react';
import ForceGraph2D from 'react-force-graph-2d';

const KnowledgeGraph = ({ data }) => {
    const getColor = (type) => {
        switch (type) {
            case 'TARGET': return '#ff003c'; // Cyber Red
            case 'PARENT': return '#00f0ff'; // Neon Cyan
            case 'SYSTEM': return '#94a3b8'; // Slate
            default: return '#00ff9d';      // Neon Green
        }
    };

    const handleNodePaint = useCallback((node, ctx, globalScale) => {
        const label = node.name;
        const fontSize = 12 / globalScale;
        ctx.font = `${fontSize}px Orbitron`;
        const textWidth = ctx.measureText(label).width;
        const bckgDimensions = [textWidth, fontSize].map(n => n + fontSize * 0.2);

        // Node circle
        ctx.beginPath();
        ctx.arc(node.x, node.y, 5, 0, 2 * Math.PI, false);
        ctx.fillStyle = getColor(node.type);
        ctx.fill();

        // Glow effect
        ctx.shadowBlur = 10;
        ctx.shadowColor = getColor(node.type);

        // Label shadow for readability
        ctx.fillStyle = 'rgba(0, 0, 0, 0.8)';
        ctx.fillRect(node.x - bckgDimensions[0] / 2, node.y - bckgDimensions[1] / 2 + 10, bckgDimensions[0], bckgDimensions[1]);

        // Label text
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillStyle = '#fff';
        ctx.fillText(label, node.x, node.y + 12);
    }, []);

    return (
        <div className="w-full h-[400px] bg-cyber-black/50 border border-cyber-border rounded-lg overflow-hidden relative">
            <div className="absolute top-2 left-2 z-10">
                <span className="text-[10px] font-mono text-slate-500 uppercase">Process_Lineage_Graph</span>
            </div>

            <ForceGraph2D
                graphData={data}
                nodeLabel="name"
                nodeAutoColorBy="type"
                linkDirectionalArrowLength={3.5}
                linkDirectionalArrowRelPos={1}
                linkCurvature={0.25}
                backgroundColor="rgba(0,0,0,0)"
                linkColor={() => 'rgba(31, 41, 55, 0.5)'}
                nodeCanvasObject={handleNodePaint}
                cooldownTicks={100}
                width={700}
                height={400}
            />
        </div>
    );
};

export default KnowledgeGraph;
