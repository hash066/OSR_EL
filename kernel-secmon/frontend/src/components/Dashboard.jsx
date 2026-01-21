import React, { useState, useEffect, useRef } from 'react';
import StatsCards from './StatsCards';
import AlertFeed from './AlertFeed';
import ThreatTimeline from './ThreatTimeline';
import SystemStatus3D from './SystemStatus3D';
import ProcessGraph from './ProcessGraph';
import AnalysisModal from './AnalysisModal';
import { ShieldCheck, Activity, Cpu, Wifi, History, GitBranch } from 'lucide-react';

const Dashboard = () => {
    const [events, setEvents] = useState([]);
    const [stats, setStats] = useState({ total_events: 0, high_severity: 0 });
    const [isConnected, setIsConnected] = useState(false);
    const [selectedEvent, setSelectedEvent] = useState(null);
    const [isModalOpen, setIsModalOpen] = useState(false);
    const wsRef = useRef(null);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const evRes = await fetch('http://localhost:8001/api/events');
                const evData = await evRes.json();
                setEvents(evData);

                const stRes = await fetch('http://localhost:8001/api/stats');
                const stData = await stRes.json();
                setStats(stData);
            } catch (err) {
                console.error("Failed to fetch initial data", err);
            }
        };

        fetchData();

        const connectWs = () => {
            const ws = new WebSocket('ws://localhost:8001/ws/feed');
            ws.onopen = () => {
                console.log('Connected to WS');
                setIsConnected(true);
            };

            ws.onmessage = (event) => {
                const newEvent = JSON.parse(event.data);
                setEvents(prev => [...prev.slice(-99), newEvent]);

                setStats(prev => ({
                    ...prev,
                    total_events: (prev.total_events || 0) + 1,
                    high_severity: newEvent.severity === 'HIGH' ? (prev.high_severity || 0) + 1 : (prev.high_severity || 0),
                    medium_severity: newEvent.severity === 'MEDIUM' ? (prev.medium_severity || 0) + 1 : (prev.medium_severity || 0)
                }));
            };

            ws.onclose = () => {
                setIsConnected(false);
                setTimeout(connectWs, 3000);
            };

            wsRef.current = ws;
        };

        connectWs();

        return () => {
            if (wsRef.current) wsRef.current.close();
        };
    }, []);

    const handleEventClick = (event) => {
        setSelectedEvent(event);
        setIsModalOpen(true);
    };

    return (
        <div className="min-h-screen bg-cyber-black text-slate-200 font-sans selection:bg-cyber-primary selection:text-black">
            {/* Header */}
            <header className="bg-cyber-dark/90 backdrop-blur-md border-b border-cyber-border sticky top-0 z-50">
                <div className="max-w-[1600px] mx-auto px-6 h-20 flex items-center justify-between">
                    <div className="flex items-center gap-4">
                        <div className={`p-2 rounded-lg border ${isConnected ? 'border-cyber-primary bg-cyber-primary/10' : 'border-cyber-alert bg-cyber-alert/10'}`}>
                            <ShieldCheck className={isConnected ? "text-cyber-primary" : "text-cyber-alert"} size={28} />
                        </div>
                        <div>
                            <h1 className="text-2xl font-bold text-white font-display tracking-wider glow-text">KERNEL_SECMON</h1>
                            <div className="flex items-center gap-2">
                                <span className="text-[10px] text-cyber-secondary font-mono tracking-[0.2em] uppercase">Security Level: Maximum</span>
                            </div>
                        </div>
                    </div>

                    <div className="flex items-center gap-6">
                        <div className="hidden md:flex flex-col items-end text-right">
                            <span className="text-xs text-slate-500 font-mono">SYSTEM_UPTIME</span>
                            <span className="text-white font-mono">00:42:15</span>
                        </div>

                        <div className={`flex items-center gap-3 px-4 py-2 rounded border font-mono text-xs font-bold transition-all ${isConnected ? 'bg-cyber-primary/5 border-cyber-primary/30 text-cyber-primary shadow-[0_0_10px_rgba(0,255,157,0.2)]' : 'bg-cyber-alert/5 border-cyber-alert/30 text-cyber-alert'}`}>
                            <Wifi size={14} className={isConnected ? "animate-pulse" : ""} />
                            {isConnected ? 'LINK_ESTABLISHED' : 'LINK_OFFLINE'}
                        </div>
                    </div>
                </div>
            </header>

            {/* Main Content */}
            <main className="max-w-[1600px] mx-auto px-6 py-10">
                <StatsCards stats={stats} />

                <div className="grid grid-cols-1 xl:grid-cols-4 gap-8">
                    <div className="xl:col-span-2">
                        <AlertFeed events={events} onEventClick={handleEventClick} />
                    </div>

                    <div className="xl:col-span-1 border-x border-cyber-border/30 px-2">
                        <ThreatTimeline events={events} onEventClick={handleEventClick} />
                    </div>

                    <div className="space-y-6">
                        {/* 3D Status Visualization */}
                        <SystemStatus3D stats={stats} />

                        {/* Process Lineage Graph */}
                        <div className="bg-cyber-card rounded-xl p-6 border border-cyber-border shadow-lg">
                            <h3 className="text-md font-bold text-white mb-6 font-display flex items-center gap-2">
                                <GitBranch className="text-cyber-primary" size={18} />
                                PROCESS_LINEAGE_MAP
                            </h3>
                            <div className="h-[400px]">
                                <ProcessGraph onNodeClick={handleEventClick} />
                            </div>
                        </div>

                        {/* Status Panel */}
                        <div className="bg-cyber-card rounded-xl p-6 border border-cyber-border shadow-lg">
                            <h3 className="text-md font-bold text-white mb-6 font-display flex items-center gap-2">
                                <Activity className="text-cyber-secondary" size={18} />
                                SYSTEM_STATUS
                            </h3>
                            <div className="space-y-4 font-mono text-xs">
                                <div className="flex justify-between items-center p-3 bg-cyber-dark rounded border border-cyber-border">
                                    <span className="text-slate-400">KERNEL_MODULE</span>
                                    <span className="text-cyber-primary font-bold">LOADED</span>
                                </div>
                                <div className="flex justify-between items-center p-3 bg-cyber-dark rounded border border-cyber-border">
                                    <span className="text-slate-400">AGENT_STATUS</span>
                                    <span className="text-cyber-primary font-bold">LISTENING</span>
                                </div>
                                <div className="flex justify-between items-center p-3 bg-cyber-dark rounded border border-cyber-border">
                                    <span className="text-slate-400">BUFFER_USAGE</span>
                                    <div className="w-24 bg-cyber-black h-2 rounded-full overflow-hidden">
                                        <div className="bg-cyber-secondary h-full w-[45%]"></div>
                                    </div>
                                </div>
                            </div>
                        </div>

                        {/* Decorative / Info Panel */}
                        <div className="bg-cyber-card rounded-xl p-6 border border-cyber-border shadow-lg relative overflow-hidden">
                            <div className="absolute inset-0 bg-[url('https://media.giphy.com/media/U3qYN8S0j3bpK/giphy.gif')] opacity-[0.03] pointer-events-none"></div>
                            <h3 className="text-md font-bold text-white mb-4 font-display flex items-center gap-2">
                                <Cpu className="text-cyber-warning" size={18} />
                                THREAT_INTEL
                            </h3>
                            <div className="text-slate-400 text-xs leading-relaxed font-mono">
                                <p className="mb-2">{'>'} Monitoring syscall table hooks...</p>
                                <p className="mb-2">{'>'} Scanning task_struct for credential inconsistencies...</p>
                                <p className="mb-2">{'>'} VFS layer integrity check: <span className="text-cyber-primary">OK</span></p>
                                <p>{'>'} IDT vector analysis: <span className="text-cyber-primary">OK</span></p>
                            </div>
                        </div>
                    </div>
                </div>
            </main>

            <AnalysisModal
                isOpen={isModalOpen}
                onClose={() => setIsModalOpen(false)}
                event={selectedEvent}
            />
        </div>
    );
};

export default Dashboard;
