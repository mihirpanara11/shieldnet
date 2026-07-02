import React from 'react';
import { NavLink } from 'react-router-dom';

const links = [
  { to: '/', label: 'Dashboard' },
  { to: '/threats', label: 'Threats' },
  { to: '/devices', label: 'Devices' },
  { to: '/zones', label: 'Zones' },
  { to: '/federated', label: 'Federated' },
  { to: '/settings', label: 'Settings' },
];

const Sidebar: React.FC = () => {
  return (
    <aside style={{
      width: '260px',
      background: '#004D40',
      color: 'white',
      padding: '16px 0',
      fontFamily: 'Calibri, sans-serif',
      flexShrink: 0,
    }}>
      {links.map(link => (
        <NavLink
          key={link.to}
          to={link.to}
          end={link.to === '/'}
          style={({ isActive }) => ({
            display: 'block',
            padding: '12px 24px',
            color: isActive ? '#FF8F00' : 'rgba(255,255,255,0.85)',
            textDecoration: 'none',
            fontSize: '14px',
            fontWeight: isActive ? 700 : 400,
            background: isActive ? 'rgba(255,255,255,0.1)' : 'transparent',
            borderLeft: isActive ? '4px solid #FF8F00' : '4px solid transparent',
            transition: 'all 0.2s',
          })}
        >
          {link.label}
        </NavLink>
      ))}
    </aside>
  );
};

export default Sidebar;
