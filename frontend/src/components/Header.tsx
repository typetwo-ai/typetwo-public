// components/Header.tsx
import React from 'react';

const Header: React.FC = () => {
  return (
    <header className="w-full py-6 container mx-auto">
      <img
        src="/011-logo-svg.svg"
        alt="Logo"
        className="h-14 w-auto"
      />
    </header>
  );
};

export default Header;
