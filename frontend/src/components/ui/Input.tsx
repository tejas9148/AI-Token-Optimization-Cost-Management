import React from 'react';

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  variant?: 'default' | 'outline';
  size?: 'sm' | 'md' | 'lg';
}

const Input: React.FC<InputProps> = ({
  variant = 'default',
  size = 'md',
  className = '',
  ...props
}) => {
  const baseClasses = 'block w-full rounded border-border-input bg-input px-3 py-2 text-sm ring-offset-white placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50';
  
  const variantClasses = {
    default: '',
    outline: 'border-border',
  };
  
  const sizeClasses = {
    sm: 'h-9 text-sm',
    md: 'h-10',
    lg: 'h-11 text-lg',
  };

  return (
    <input
      type="text"
      className={`${baseClasses} ${variantClasses[variant]} ${sizeClasses[size]} ${className}`}
      {...props}
    />
  );
};

export default Input;
