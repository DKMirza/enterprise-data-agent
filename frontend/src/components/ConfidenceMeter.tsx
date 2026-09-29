interface ConfidenceMeterProps {
  confidence: number;
  size?: 'sm' | 'md' | 'lg';
  showLabel?: boolean;
}

const ConfidenceMeter = ({ 
  confidence, 
  size = 'md',
  showLabel = true 
}: ConfidenceMeterProps) => {
  const percentage = Math.round(confidence * 100);
  
  // Determine color based on confidence level
  const getColor = () => {
    if (confidence >= 0.90) return 'bg-green-500';
    if (confidence >= 0.75) return 'bg-yellow-500';
    if (confidence >= 0.60) return 'bg-orange-500';
    return 'bg-red-500';
  };

  const sizeClasses = {
    sm: 'h-2',
    md: 'h-3',
    lg: 'h-4',
  };

  return (
    <div className="w-full">
      {showLabel && (
        <div className="flex items-center justify-between mb-1">
          <span className="text-sm font-medium text-slate-700">Confidence Score</span>
          <span className={`text-sm font-bold ${getColor().replace('bg-', 'text-')}`}>
            {percentage}%
          </span>
        </div>
      )}
      <div className={`w-full bg-slate-200 rounded-full overflow-hidden ${sizeClasses[size]}`}>
        <div
          className={`${getColor()} h-full transition-all duration-500 ease-out`}
          style={{ width: `${percentage}%` }}
        />
      </div>
    </div>
  );
};

export default ConfidenceMeter;
