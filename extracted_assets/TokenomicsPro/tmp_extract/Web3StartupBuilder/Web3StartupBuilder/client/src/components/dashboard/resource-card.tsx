import { Link } from "wouter";
import { useState } from "react";

interface ResourceCardProps {
  title: string;
  description: string;
  backgroundClass: string;
  icon: React.ReactNode;
  linkText: string;
  linkUrl: string;
}

export const ResourceCard: React.FC<ResourceCardProps> = ({
  title,
  description,
  backgroundClass,
  icon,
  linkText,
  linkUrl,
}) => {
  // Track hover state for the arrow animation
  const [isHovered, setIsHovered] = useState(false);

  return (
    <div 
      className="bg-card rounded-xl shadow-md hover:shadow-lg transition-shadow overflow-hidden border border-border"
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      <div className={`h-40 ${backgroundClass} relative`}>
        <div className="absolute inset-0 flex items-center justify-center">
          <div className="h-16 w-16 text-white opacity-40">
            {icon}
          </div>
        </div>
      </div>
      <div className="p-5">
        <h3 className="font-semibold text-foreground mb-2">{title}</h3>
        <p className="text-sm text-muted-foreground mb-4">{description}</p>
        <Link href={linkUrl} className="text-primary font-medium text-sm flex items-center gap-1 hover:underline">
          <span>{linkText}</span>
          <svg 
            xmlns="http://www.w3.org/2000/svg" 
            viewBox="0 0 24 24" 
            fill="none" 
            stroke="currentColor" 
            strokeWidth="2" 
            strokeLinecap="round" 
            strokeLinejoin="round" 
            className={`h-4 w-4 transition-transform duration-200 ${isHovered ? 'translate-x-1' : ''}`}
          >
            <line x1="5" y1="12" x2="19" y2="12"></line>
            <polyline points="12 5 19 12 12 19"></polyline>
          </svg>
        </Link>
      </div>
    </div>
  );
};
