import React, { useEffect, useRef, useState } from 'react';
import ForceGraph2D from 'react-force-graph-2d';
import { Network } from 'lucide-react';

const ProcessGraph = ({ onNodeClick }) => {
    const [graphData, setGraphData] = useState({ nodes: [], links: [] });
    const [loading, setLoading] = useState(true);
    const graphRef = useRef();

    useEffect(() => {
        fetchProcessTree();

        // Refresh every 5 seconds
        const interval = setInterval(fetchProcessTree, 5000);
        return () => clearInterval(interval);
    }, []);

    const fetchProcessTree = async () => {
        try {
            const res = await fetch('http://localhost:8001/api/processes/tree');
            const data = await res.json();
            setGraphData(data);
            setLoading(false);
        } catch (err) {
            console.error('Failed to fetch process tree:', err);
            setLoading(false);
        }
    };

    const getNodeColor = (node) => {
        if (node.suspicious) return '#ff006a'; // Cyber alert red
        return '#00ff9d'; // Cyber primary green
    };

    const getNodeSize = (node) => {
        // Size based on event count, minimum 4, maximum 10
        return Math.min(Math.max(node.event_count * 0.5 + 4, 4), 10);
    };

    const handleNodeClick = (node) => {
        if (onNodeClick) {
            // Find a recent event for this process
            fetch(`http://localhost:8001/api/events?limit=200`)
                .then(res => res.json())
                .then(events => {
                    const event = events.find(e => e.pid === node.pid);
                    if (event) {
                        onNodeClick(event);
                    }
                })
                .catch(err => console.error('Failed to fetch event:', err));
        }
    };

    if (loading) {
        return (
            <div className="w-full h-full flex items-center justify-center bg-cyber-dark rounded-xl border border-cyber-border">
                <div className="text-cyber-primary font-mono text-xs animate-pulse">
                    LOADING_PROCESS_TREE...
                </div>
            </div>
        );
    }

    if (!graphData.nodes || graphData.nodes.length === 0) {
        return (
            <div className="w-full h-full flex flex-col items-center justify-center bg-cyber-dark rounded-xl border border-cyber-border p-6">
                <Network className="text-slate-600 mb-3" size={32} />
                <p className="text-slate-500 text-xs font-mono">No process data available</p>
                <p className="text-slate-600 text-[10px] font-mono mt-1">Generate events to populate graph</p>
            </div>
        );
    }

    return (
        <div className="w-full h-full bg-cyber-dark rounded-xl border border-cyber-border overflow-hidden relative">
            {/* Legend */}
            <div className="absolute top-3 left-3 z-10 bg-cyber-black/80 backdrop-blur-sm border border-cyber-border rounded-lg p-3 font-mono text-[10px]">
                <div className="flex items-center gap-2 mb-2">
                    <div className="w-3 h-3 rounded-full bg-cyber-primary"></div>
                    <span className="text-slate-300">Normal Process</span>
                </div>
                <div className="flex items-center gap-2">
                    <div className="w-3 h-3 rounded-full bg-cyber-alert"></div>
                    <span className="text-slate-300">Suspicious Process</span>
                </div>
            </div>

            {/* Node count badge */}
            <div className="absolute top-3 right-3 z-10 bg-cyber-black/80 backdrop-blur-sm border border-cyber-border rounded-lg px-3 py-2 font-mono text-[10px]">
                <span className="text-slate-400">NODES:</span>{' '}
                <span className="text-cyber-primary font-bold">{graphData.nodes.length}</span>
            </div>

            <ForceGraph2D
                ref={graphRef}
                graphData={graphData}
                nodeLabel={(node) => `${node.name} (PID: ${node.pid})\nEvents: ${node.event_count}\nStatus: ${node.suspicious ? 'SUSPICIOUS' : 'NORMAL'}`}
                nodeColor={getNodeColor}
                nodeRelSize={getNodeSize}
                nodeCanvasObject={(node, ctx, globalScale) => {
                    // Draw node circle
                    const size = getNodeSize(node);
                    ctx.beginPath();
                    ctx.arc(node.x, node.y, size, 0, 2 * Math.PI);
                    ctx.fillStyle = getNodeColor(node);
                    ctx.fill();

                    // Add glow effect for suspicious nodes
                    if (node.suspicious) {
                        ctx.shadowBlur = 15;
                        ctx.shadowColor = '#ff006a';
                        ctx.fill();
                        ctx.shadowBlur = 0;
                    }

                    // Draw label if zoomed in enough
                    if (globalScale > 1.2) {
                        ctx.font = `${Math.max(3, 10 / globalScale)}px monospace`;
                        ctx.textAlign = 'center';
                        ctx.textBaseline = 'middle';
                        ctx.fillStyle = '#ffffff';
                        ctx.fillText(node.name.substring(0, 12), node.x, node.y + size + 8);
                    }
                }}
                linkColor={() => 'rgba(100, 116, 139, 0.3)'}
                linkWidth={1}
                linkDirectionalArrowLength={3}
                linkDirectionalArrowRelPos={1}
                linkDirectionalParticles={2}
                linkDirectionalParticleWidth={1.5}
                backgroundColor="#0a0a0a"
                onNodeClick={handleNodeClick}
                cooldownTicks={100}
                d3VelocityDecay={0.3}
                enableNodeDrag={true}
                enableZoomInteraction={true}
                enablePanInteraction={true}
            />
        </div>
    );
};

export default ProcessGraph;
