import React from 'react';
import { Link } from "wouter";

interface QuickStartCardProps {
  title: string;
  description: string;
  icon: React.ReactNode;
  gradient: string;
  buttonText: string;
  buttonLink: string;
  buttonColor: string;
  shadowColor: string;
}

export const QuickStartCard: React.FC<QuickStartCardProps> = ({
  title,
  description,
  icon,
  gradient,
  buttonText,
  buttonLink,
  buttonColor,
  shadowColor,
}) => {
  return (
    <div 
      className={`${gradient} rounded-xl p-6 text-white shadow-lg ${shadowColor} h-full flex flex-col`}
    >
      <div className="flex justify-between items-start mb-4">
        <h3 className="text-xl font-semibold">{title}</h3>
        <span className="h-10 w-10 rounded-full bg-white/20 flex items-center justify-center">
          {icon}
        </span>
      </div>
      <p className="mb-4 text-white/80">{description}</p>
      <Link href={buttonLink} className={`mt-auto text-sm py-2 px-4 bg-white ${buttonColor} rounded-lg font-medium hover:bg-opacity-90 transition-colors inline-block`}>
        {buttonText}
      </Link>
    </div>
  );
};