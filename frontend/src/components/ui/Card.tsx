import React from 'react';

interface CardProps {
  children: React.ReactNode;
  className?: string;
  header?: React.ReactNode;
  footer?: React.ReactNode;
}

const Card: React.FC<CardProps> = ({
  children,
  className = '',
  header,
  footer,
}) => {
  return (
    <div className={`${className} bg-card text-card-foreground shadow-sm rounded-lg border border-border`}>
      {header && <div className="px-6 py-4 border-b border-border">{header}</div>}
      <div className="px-6 py-4">{children}</div>
      {footer && <div className="px-6 py-4 border-t border-border">{footer}</div>}
    </div>
  );
};

export default Card;
