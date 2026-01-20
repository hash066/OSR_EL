import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { ShieldAlert, Info, AlertTriangle, Clock } from 'lucide-react';

const ThreatTimeline = ({ events, onEventClick }) => {
    // Take last 15 events for timeline
    const recentEvents = [...events].reverse().slice(0, 15);

    const getIcon = (severity) => {
        switch (severity) {
            case 'HIGH': return <ShieldAlert className="text-cyber-alert" size={16} />;
            case 'MEDIUM': return <AlertTriangle className="text-cyber-warning" size={16} />;
            default: return <Info className="text-cyber-primary" size={16} />;
        }
    };

    const getSeverityClass = (severity) => {
        switch (severity) {
            case 'HIGH': return 'border-cyber-alert/50 bg-cyber-alert/5 shadow-[0_0_10px_rgba(255,82,82,0.1)]';
            case 'MEDIUM': return 'border-cyber-warning/50 bg-cyber-warning/5';
            default: return 'border-cyber-primary/50 bg-cyber-primary/5';
        }
    };

    return (
        <div className="bg-cyber-card rounded-xl p-6 border border-cyber-border shadow-lg flex flex-col h-full">
            <h3 className="text-md font-bold text-white mb-6 font-display flex items-center gap-2">
                <Clock className="text-cyber-primary" size={18} />
                THREAT_TIMELINE
            </h3>

            <div className="flex-1 overflow-y-auto pr-2 space-y-4 relative">
                {/* Vertical Line */}
                <div className="absolute left-[15px] top-2 bottom-2 w-[1px] bg-cyber-border/50"></div>

                <AnimatePresence initial={false}>
                    {recentEvents.map((event, idx) => (
                        <motion.div
                            key={event.timestamp + idx}
                            initial={{ opacity: 0, x: -20 }}
                            animate={{ opacity: 1, x: 0 }}
                            exit={{ opacity: 0, scale: 0.9 }}
                            transition={{ duration: 0.3 }}
                            onClick={() => onEventClick && onEventClick(event)}
                            className={`relative pl-10 pr-4 py-3 rounded border text-xs font-mono group cursor-pointer hover:scale-[1.02] transition-transform ${getSeverityClass(event.severity)}`}
                        >
                            {/* Dot on line */}
                            <div className={`absolute left-[11px] top-1/2 -translate-y-1/2 w-[9px] h-[9px] rounded-full border-2 border-cyber-black z-10 
                                ${event.severity === 'HIGH' ? 'bg-cyber-alert' : event.severity === 'MEDIUM' ? 'bg-cyber-warning' : 'bg-cyber-primary'}`}
                            />

                            <div className="flex justify-between items-start mb-1">
                                <span className={`font-bold ${event.severity === 'HIGH' ? 'text-cyber-alert' : event.severity === 'MEDIUM' ? 'text-cyber-warning' : 'text-cyber-primary'}`}>
                                    {event.type}
                                </span>
                                <span className="text-[10px] text-slate-500">
                                    {new Date(event.timestamp).toLocaleTimeString([], { hour12: false })}
                                </span>
                            </div>

                            <p className="text-slate-400 line-clamp-2 leading-relaxed italic">
                                "{event.details}"
                            </p>

                            <div className="mt-2 flex items-center gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                                <span className="text-[9px] px-1.5 py-0.5 rounded bg-cyber-dark border border-cyber-border text-slate-500">
                                    PID: {event.pid}
                                </span>
                                <span className="text-[9px] px-1.5 py-0.5 rounded bg-cyber-dark border border-cyber-border text-slate-500 uppercase">
                                    {event.process_name}
                                </span>
                            </div>
                        </motion.div>
                    ))}
                </AnimatePresence>

                {recentEvents.length === 0 && (
                    <div className="text-center py-10 text-slate-500 font-mono text-xs">
                        WAITING_FOR_UPLINK...
                    </div>
                )}
            </div>
        </div>
    );
};

export default ThreatTimeline;
