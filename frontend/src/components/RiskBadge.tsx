import { AlertCircle, CheckCircle, AlertTriangle } from 'lucide-react';

interface RiskBadgeProps {
  riskLevel: 'LOW' | 'MEDIUM' | 'HIGH';
  className?: string;
}

const RiskBadge = ({ riskLevel, className = '' }: RiskBadgeProps) => {
  const getRiskConfig = () => {
    switch (riskLevel) {
      case 'LOW':
        return {
          color: 'bg-green-100 text-green-800 border-green-300',
          icon: CheckCircle,
          label: 'Auto-Merge Safe',
        };
      case 'MEDIUM':
        return {
          color: 'bg-yellow-100 text-yellow-800 border-yellow-300',
          icon: AlertTriangle,
          label: 'Review Required',
        };
      case 'HIGH':
        return {
          color: 'bg-red-100 text-red-800 border-red-300',
          icon: AlertCircle,
          label: 'Investigate',
        };
      default:
        return {
          color: 'bg-slate-100 text-slate-800 border-slate-300',
          icon: AlertCircle,
          label: riskLevel,
        };
    }
  };

  const config = getRiskConfig();
  const Icon = config.icon;

  return (
    <span className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-sm font-medium border ${config.color} ${className}`}>
      <Icon className="w-4 h-4" />
      {config.label}
    </span>
  );
};

export default RiskBadge;
