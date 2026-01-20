import React from 'react';
import { Activity, AlertTriangle, ShieldAlert, Eye, Cpu } from 'lucide-react';

const StatsCard = ({ title, value, icon: Icon, color, subtext, trend }) => (
  <div className="bg-cyber-card rounded-xl p-6 border border-cyber-border shadow-lg relative overflow-hidden group hover:border-cyber-primary/50 transition-all duration-300">
    {/* Glow effect */}
    <div className={`absolute -right-6 -top-6 w-24 h-24 bg-${color?.replace('text-', '')}/10 rounded-full blur-2xl group-hover:bg-${color?.replace('text-', '')}/20 transition-all`}></div>

    <div className="flex items-center justify-between relative z-10">
      <div>
        <p className="text-slate-500 text-xs font-mono uppercase tracking-widest mb-1">{title}</p>
        <h3 className="text-4xl font-bold text-white font-display tracking-wide">{value}</h3>
      </div>
      <div className={`p-3 rounded-lg bg-cyber-dark border border-cyber-border ${color} shadow-[0_0_15px_rgba(0,0,0,0.5)]`}>
        <Icon size={28} />
      </div>
    </div>

    <div className="mt-4 flex items-center justify-between">
      {subtext && <p className="text-slate-400 text-xs font-mono">{'>'} {subtext}</p>}
      {/* Fake trendline or mini chart indicator */}
      <div className="h-1 w-12 bg-cyber-dark rounded overflow-hidden">
        <div className={`h-full ${color?.replace('text-', 'bg-')} w-2/3 animate-pulse`}></div>
      </div>
    </div>
  </div>
);

const StatsCards = ({ stats }) => {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
      <StatsCard
        title="Total Events"
        value={stats.total_events || 0}
        icon={Activity}
        color="text-cyber-secondary"
        subtext="SYSTEM_ACTIVE"
      />
      <StatsCard
        title="Critical Threats"
        value={stats.high_severity || 0}
        icon={ShieldAlert}
        color="text-cyber-alert"
        subtext="IMMEDIATE_ACTION_REQ"
      />
      <StatsCard
        title="Hidden Processes"
        value={stats.suspicious_processes || 0}
        icon={Eye}
        color="text-cyber-primary"
        subtext="ROOTKIT_SCAN_ACTIVE"
      />
      <StatsCard
        title="Anomalies"
        value={stats.medium_severity || 0}
        icon={AlertTriangle}
        color="text-cyber-warning"
        subtext="HEURISTIC_DETECTION"
      />
    </div>
  );
};

export default StatsCards;
