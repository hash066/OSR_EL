import React, { useEffect, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { X, ShieldAlert, Cpu, Network, Zap, AlertTriangle, ExternalLink } from 'lucide-react';
import KnowledgeGraph from './KnowledgeGraph';

const AnalysisModal = ({ isOpen, onClose, event }) => {
    const [analysis, setAnalysis] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        if (isOpen && event && event.id) {
            setLoading(true);
            fetch(`http://localhost:8001/api/analysis/${event.id}`)
                .then(res => res.json())
                .then(data => {
                    setAnalysis(data);
                    setLoading(false);
                })
                .catch(err => {
                    console.error("Analysis fetch failed:", err);
                    setLoading(false);
                });
        }
    }, [isOpen, event]);

    if (!isOpen) return null;

    return (
        <AnimatePresence>
            <div className="fixed inset-0 z-[1000] flex items-center justify-center p-4">
                <motion.div
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    exit={{ opacity: 0 }}
                    onClick={onClose}
                    className="absolute inset-0 bg-cyber-black/80 backdrop-blur-sm"
                />

                <motion.div
                    initial={{ opacity: 0, scale: 0.9, y: 20 }}
                    animate={{ opacity: 1, scale: 1, y: 0 }}
                    exit={{ opacity: 0, scale: 0.9, y: 20 }}
                    className="relative w-full max-w-5xl bg-cyber-card border border-cyber-border rounded-2xl shadow-2xl overflow-hidden flex flex-col max-h-[90vh]"
                >
                    {/* Header */}
                    <div className="p-6 border-b border-cyber-border flex justify-between items-center bg-cyber-dark/50">
                        <div className="flex items-center gap-3">
                            <div className="p-2 rounded-lg bg-cyber-alert/10 border border-cyber-alert/30">
                                <ShieldAlert size={24} className="text-cyber-alert" />
                            </div>
                            <div>
                                <h2 className="text-xl font-bold text-white font-display tracking-wide uppercase">Threat_Detail: {event.type}</h2>
                                <p className="text-[10px] font-mono text-cyber-secondary tracking-widest">ID: {event.id || 'N/A'} | POSIX_PID: {event.pid}</p>
                            </div>
                        </div>
                        <button onClick={onClose} className="p-2 hover:bg-cyber-border rounded-full transition-colors">
                            <X size={20} className="text-slate-400" />
                        </button>
                    </div>

                    {/* Content */}
                    <div className="flex-1 overflow-y-auto p-8 grid grid-cols-1 lg:grid-cols-2 gap-8">
                        {/* Left Side: XAI & Details */}
                        <div className="space-y-8">
                            <div>
                                <h3 className="text-xs font-mono font-bold text-cyber-primary p-1 border-l-2 border-cyber-primary mb-4 flex items-center gap-2">
                                    <Zap size={14} /> EXPLAINABLE_AI_INSIGHTS
                                </h3>
                                <div className="p-5 bg-cyber-dark rounded-xl border border-cyber-border/50 relative overflow-hidden group">
                                    <div className="absolute top-0 right-0 p-2 opacity-10">
                                        <Cpu size={40} className="text-cyber-primary" />
                                    </div>
                                    {loading ? (
                                        <div className="animate-pulse space-y-3">
                                            <div className="h-4 bg-slate-800 rounded w-3/4"></div>
                                            <div className="h-4 bg-slate-800 rounded w-full"></div>
                                            <div className="h-4 bg-slate-800 rounded w-5/6"></div>
                                        </div>
                                    ) : (
                                        <p className="text-sm italic leading-relaxed text-slate-300 font-mono">
                                            "{analysis?.xai_explanation || 'No AI context available for this event type.'}"
                                        </p>
                                    )}
                                </div>
                            </div>

                            <div>
                                <h3 className="text-xs font-mono font-bold text-cyber-secondary p-1 border-l-2 border-cyber-secondary mb-4 flex items-center gap-2">
                                    <Network size={14} /> FORENSIC_PROPERTIES
                                </h3>
                                <div className="grid grid-cols-2 gap-4">
                                    <div className="p-4 bg-cyber-black rounded border border-cyber-border">
                                        <span className="text-[10px] text-slate-500 uppercase block mb-1">Process_Name</span>
                                        <span className="text-sm font-mono text-white">{event.process_name}</span>
                                    </div>
                                    <div className="p-4 bg-cyber-black rounded border border-cyber-border">
                                        <span className="text-[10px] text-slate-500 uppercase block mb-1">Severity_Score</span>
                                        <span className={`text-sm font-mono font-bold ${event.severity === 'HIGH' ? 'text-cyber-alert' : 'text-cyber-warning'}`}>{event.severity}</span>
                                    </div>
                                    <div className="p-4 bg-cyber-black rounded border border-cyber-border col-span-2">
                                        <span className="text-[10px] text-slate-500 uppercase block mb-1">Raw_Kernel_Data</span>
                                        <span className="text-[11px] font-mono text-slate-400 break-all">{event.details}</span>
                                    </div>
                                </div>
                            </div>

                            {/* Threat Intelligence Section */}
                            <div>
                                <h3 className="text-xs font-mono font-bold text-cyber-warning p-1 border-l-2 border-cyber-warning mb-4 flex items-center gap-2">
                                    <AlertTriangle size={14} /> THREAT_INTELLIGENCE
                                </h3>
                                <div className="space-y-3">
                                    {loading ? (
                                        <div className="p-4 bg-cyber-dark rounded-xl border border-cyber-border/50 animate-pulse">
                                            <div className="h-4 bg-slate-800 rounded w-2/3"></div>
                                        </div>
                                    ) : analysis?.threat_intel?.has_network_activity ? (
                                        <>
                                            {/* Threat Score Summary */}
                                            <div className="p-4 bg-cyber-dark rounded-xl border border-cyber-border/50">
                                                <div className="flex items-center justify-between mb-3">
                                                    <span className="text-[10px] text-slate-500 uppercase">Max Threat Score</span>
                                                    <span className={`text-2xl font-bold font-mono ${analysis.threat_intel.max_threat_score > 70 ? 'text-cyber-alert' :
                                                            analysis.threat_intel.max_threat_score > 30 ? 'text-cyber-warning' :
                                                                'text-cyber-primary'
                                                        }`}>
                                                        {analysis.threat_intel.max_threat_score}
                                                    </span>
                                                </div>
                                                <div className="w-full bg-cyber-black h-2 rounded-full overflow-hidden">
                                                    <div
                                                        className={`h-full transition-all ${analysis.threat_intel.max_threat_score > 70 ? 'bg-cyber-alert' :
                                                                analysis.threat_intel.max_threat_score > 30 ? 'bg-cyber-warning' :
                                                                    'bg-cyber-primary'
                                                            }`}
                                                        style={{ width: `${analysis.threat_intel.max_threat_score}%` }}
                                                    ></div>
                                                </div>
                                            </div>

                                            {/* Malicious IPs */}
                                            {analysis.threat_intel.malicious_ips.length > 0 && (
                                                <div className="p-4 bg-cyber-alert/10 rounded-xl border border-cyber-alert/30">
                                                    <div className="flex items-center gap-2 mb-2">
                                                        <ShieldAlert size={14} className="text-cyber-alert" />
                                                        <span className="text-xs font-bold text-cyber-alert uppercase">Known Malicious IPs Detected</span>
                                                    </div>
                                                    <div className="space-y-2">
                                                        {analysis.threat_intel.malicious_ips.map((intel, idx) => (
                                                            <div key={idx} className="text-[11px] font-mono text-slate-300 flex items-center justify-between">
                                                                <span>{intel.ip} ({intel.country_code})</span>
                                                                <a
                                                                    href={intel.report_url}
                                                                    target="_blank"
                                                                    rel="noopener noreferrer"
                                                                    className="text-cyber-primary hover:text-cyber-secondary flex items-center gap-1"
                                                                >
                                                                    Report <ExternalLink size={10} />
                                                                </a>
                                                            </div>
                                                        ))}
                                                    </div>
                                                </div>
                                            )}

                                            {/* All Checked IPs */}
                                            <div className="p-4 bg-cyber-dark rounded-xl border border-cyber-border/50">
                                                <span className="text-[10px] text-slate-500 uppercase block mb-2">Analyzed IPs ({analysis.threat_intel.checked_ips.length})</span>
                                                <div className="space-y-2 max-h-32 overflow-y-auto">
                                                    {analysis.threat_intel.checked_ips.map((intel, idx) => (
                                                        <div key={idx} className="text-[10px] font-mono flex items-center justify-between p-2 bg-cyber-black rounded border border-cyber-border/30">
                                                            <div className="flex items-center gap-2">
                                                                <div className={`w-2 h-2 rounded-full ${intel.is_malicious ? 'bg-cyber-alert' : 'bg-cyber-primary'}`}></div>
                                                                <span className="text-slate-300">{intel.ip}</span>
                                                                <span className="text-slate-600">({intel.country_code})</span>
                                                            </div>
                                                            <span className={`font-bold ${intel.threat_score > 70 ? 'text-cyber-alert' :
                                                                    intel.threat_score > 30 ? 'text-cyber-warning' :
                                                                        'text-cyber-primary'
                                                                }`}>
                                                                {intel.threat_score}
                                                            </span>
                                                        </div>
                                                    ))}
                                                </div>
                                            </div>
                                        </>
                                    ) : (
                                        <div className="p-4 bg-cyber-dark rounded-xl border border-cyber-border/50 text-center">
                                            <Network size={24} className="text-slate-600 mx-auto mb-2" />
                                            <p className="text-[10px] text-slate-500 font-mono">No network activity detected</p>
                                        </div>
                                    )}
                                </div>
                            </div>
                        </div>

                        {/* Right Side: Graph */}
                        <div className="flex flex-col">
                            <h3 className="text-xs font-mono font-bold text-cyber-warning p-1 border-l-2 border-cyber-warning mb-4 flex items-center gap-2">
                                <Network size={14} /> LINEAGE_KNOWLEDGE_GRAPH
                            </h3>
                            {loading ? (
                                <div className="flex-1 bg-cyber-dark rounded-xl border border-cyber-border flex items-center justify-center">
                                    <div className="text-cyber-primary font-mono text-xs animate-pulse">GENERATING_TOPOLOGY...</div>
                                </div>
                            ) : analysis?.graph ? (
                                <KnowledgeGraph data={analysis.graph} />
                            ) : (
                                <div className="flex-1 bg-cyber-dark rounded-xl border border-cyber-border flex items-center justify-center text-slate-500 text-xs">
                                    Graph data unavailable.
                                </div>
                            )}
                        </div>
                    </div>
                </motion.div>
            </div>
        </AnimatePresence>
    );
};

export default AnalysisModal;
