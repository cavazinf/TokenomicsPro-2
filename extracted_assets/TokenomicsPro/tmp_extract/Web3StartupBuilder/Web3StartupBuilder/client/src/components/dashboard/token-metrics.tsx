import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { PlusIcon } from "lucide-react";

interface TokenMetric {
  label: string;
  value: string;
  icon: React.ReactNode;
  bgColor: string;
  iconColor: string;
}

interface TokenMetricsProps {
  metrics?: TokenMetric[];
  onAddMetric?: () => void;
}

export const TokenMetrics: React.FC<TokenMetricsProps> = ({
  metrics = [
    {
      label: "Token Type",
      value: "ERC-20 Utility Token",
      icon: (
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="h-4 w-4 text-primary-600">
          <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polygon>
        </svg>
      ),
      bgColor: "bg-primary-100",
      iconColor: "text-primary-600"
    },
    {
      label: "Initial Market Cap",
      value: "$1,250,000",
      icon: (
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="h-4 w-4 text-green-600">
          <line x1="12" y1="1" x2="12" y2="23"></line>
          <path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path>
        </svg>
      ),
      bgColor: "bg-green-100",
      iconColor: "text-green-600"
    },
    {
      label: "Initial Token Price",
      value: "$0.025",
      icon: (
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="h-4 w-4 text-purple-600">
          <path d="M12 1v22"></path>
          <path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path>
        </svg>
      ),
      bgColor: "bg-purple-100",
      iconColor: "text-purple-600"
    },
    {
      label: "Circulating Supply",
      value: "50,000,000 (50%)",
      icon: (
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="h-4 w-4 text-orange-600">
          <path d="M12 2L2 7l10 5 10-5-10-5z"></path>
          <path d="M2 17l10 5 10-5"></path>
          <path d="M2 12l10 5 10-5"></path>
        </svg>
      ),
      bgColor: "bg-orange-100",
      iconColor: "text-orange-600"
    }
  ],
  onAddMetric
}) => {
  return (
    <Card>
      <CardHeader className="pb-2">
        <CardTitle className="text-xl font-semibold text-dark">Token Metrics</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {metrics.map((metric, index) => (
            <div key={index} className="p-4 bg-light-100 rounded-lg">
              <div className="text-sm text-dark-50 mb-1">{metric.label}</div>
              <div className="flex justify-between items-center">
                <div className="font-medium">{metric.value}</div>
                <span className={`h-8 w-8 rounded-full ${metric.bgColor} flex items-center justify-center ${metric.iconColor}`}>
                  {metric.icon}
                </span>
              </div>
            </div>
          ))}
        </div>
        
        <Button 
          className="w-full mt-6 bg-primary text-white hover:bg-primary-600"
          onClick={onAddMetric}
        >
          <PlusIcon className="h-4 w-4 mr-2" />
          Add Custom Metric
        </Button>
      </CardContent>
    </Card>
  );
};
