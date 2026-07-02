import React from 'react';

const Navbar: React.FC = () => {
  return (
    <nav style={{
      background: '#004D40',
      color: 'white',
      padding: '0 24px',
      height: '56px',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      fontFamily: 'Calibri, sans-serif',
    }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
        <span style={{ fontWeight: 700, fontSize: '20px', fontFamily: 'Cambria, serif' }}>
          ShieldNet
        </span>
        <span style={{
          background: '#FF8F00',
          color: 'white',
          padding: '2px 8px',
          borderRadius: '4px',
          fontSize: '11px',
          fontWeight: 700,
          letterSpacing: '0.04em',
        }}>
          ALPHA401
        </span>
      </div>
      <div style={{ display: 'flex', alignItems: 'center', gap: '20px' }}>
        <select style={{
          background: 'transparent', color: 'white', border: '1px solid #4DD0C4',
          padding: '4px 8px', borderRadius: '4px', fontSize: '13px',
        }}>
          <option>ZONE-04</option>
          <option>ZONE-01</option>
          <option>ZONE-02</option>
          <option>ZONE-03</option>
        </select>
        <span style={{ position: 'relative', cursor: 'pointer' }}>
          <span style={{ fontSize: '20px' }}>🔔</span>
          <span style={{
            position: 'absolute', top: '-4px', right: '-6px',
            background: '#C62828', color: 'white', fontSize: '10px',
            borderRadius: '50%', padding: '1px 5px', fontWeight: 700,
          }}>3</span>
        </span>
        <span style={{ cursor: 'pointer', fontSize: '13px' }}>Operator</span>
      </div>
    </nav>
  );
};

export default Navbar;
