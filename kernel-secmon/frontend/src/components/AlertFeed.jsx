import React, { useRef, useEffect } from 'react';
import { AlertCircle, Terminal, Info, ShieldAlert } from 'lucide-react';

const SeverityBadge = ({ severity }) => {
    const styles = {
        HIGH: "bg-cyber-alert/20 text-cyber-alert border-cyber-alert shadow-[0_0_10px_rgba(255,0,60,0.3)]",
        MEDIUM: "bg-cyber-warning/20 text-cyber-warning border-cyber-warning",
        INFO: "bg-cyber-secondary/20 text-cyber-secondary border-cyber-secondary"
    };

    return (
        <span className={`px-2 py-0.5 rounded text-xs font-mono font-bold border ${styles[severity] || styles.INFO}`}>
            {severity}
        </span>
    );
};

const AlertFeed = ({ events, onEventClick }) => {
    const scrollRef = useRef(null);
    const displayEvents = events && events.length > 0 ? events.slice().reverse() : [];

    return (
        <div className="bg-cyber-card rounded-xl border border-cyber-border overflow-hidden shadow-2xl relative h-[600px] flex flex-col">
            <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-cyber-primary to-cyber-secondary"></div>

            <div className="p-4 border-b border-cyber-border bg-cyber-dark/80 backdrop-blur-sm flex justify-between items-center shrink-0">
                <h2 className="text-lg font-bold text-white flex items-center gap-2 font-display tracking-wide">
                    <Terminal size={20} className="text-cyber-primary" />
                    <span className="glow-text">LIVE_KERNEL_FEED</span>
                </h2>
                <div className="flex gap-2">
                    <span className="h-2 w-2 rounded-full bg-cyber-alert animate-pulse"></span>
                    <span className="h-2 w-2 rounded-full bg-cyber-primary animate-pulse delay-75"></span>
                    <span className="h-2 w-2 rounded-full bg-cyber-secondary animate-pulse delay-150"></span>
                </div>
            </div>

            <div className="overflow-x-auto overflow-y-auto flex-1 custom-scrollbar">
                {displayEvents.length === 0 ? (
                    <div className="h-full flex flex-col items-center justify-center text-slate-500 font-mono">
                        <ShieldAlert className="mb-4 opacity-20" size={64} />
                        <p>{'>'} NO THREATS DETECTED</p>
                        <p>{'>'} SYSTEM: SECURE</p>
                    </div>
                ) : (
                    <table className="w-full text-left text-sm font-mono border-collapse">
                        <thead className="bg-cyber-dark text-slate-400 text-xs uppercase tracking-wider sticky top-0 z-10 shadow-lg">
                            <tr>
                                <th className="px-6 py-4 border-b border-cyber-border bg-cyber-dark">Time</th>
                                <th className="px-6 py-4 border-b border-cyber-border bg-cyber-dark">Level</th>
                                <th className="px-6 py-4 border-b border-cyber-border bg-cyber-dark">Type</th>
                                <th className="px-6 py-4 border-b border-cyber-border bg-cyber-dark">Source</th>
                                <th className="px-6 py-4 border-b border-cyber-border bg-cyber-dark">Message</th>
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-cyber-border/50">
                            {displayEvents.map((event, idx) => (
                                <tr
                                    key={idx}
                                    onClick={() => onEventClick && onEventClick(event)}
                                    className="hover:bg-cyber-primary/5 transition-colors group cursor-pointer"
                                >
                                    <td className="px-6 py-3 text-cyber-secondary opacity-80 whitespace-nowrap">
                                        [{new Date(event.timestamp).toLocaleTimeString()}]
                                    </td>
                                    <td className="px-6 py-3">
                                        <SeverityBadge severity={event.severity} />
                                    </td>
                                    <td className="px-6 py-3 text-white font-bold tracking-wide">
                                        {event.type}
                                    </td>
                                    <td className="px-6 py-3 text-slate-300">
                                        <span className="text-cyber-primary group-hover:underline decoration-cyber-primary/50 underline-offset-4">
                                            {event.process_name}
                                        </span>
                                        <span className="text-slate-600 ml-2 text-xs">({event.pid})</span>
                                    </td>
                                    <td className="px-6 py-3 text-slate-400 max-w-sm truncate group-hover:text-slate-200 transition-colors" title={event.details}>
                                        {'>'} {event.details}
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                )}
            </div>
        </div>
    );
};

export default AlertFeed;
