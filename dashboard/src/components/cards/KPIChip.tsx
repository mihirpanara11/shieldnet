import React from 'react';

interface KPIChipProps {
  label: string;
  value: string | number;
  accentColor: 'teal' | 'amber' | 'teal600' | 'red';
  blinking?: boolean;
  subtitle?: string;
}

const ACCENT_COLORS = {
  teal:    { border: '#00695C', bg: '#E0F2F1', text: '#004D40' },
  amber:   { border: '#FF8F00', bg: '#FFF8E1', text: '#FF6F00' },
  teal600: { border: '#00897B', bg: '#E0F2F1', text: '#004D40' },
  red:     { border: '#C62828', bg: '#FFEBEE', text: '#B71C1C' },
};

export const KPIChip: React.FC<KPIChipProps> = ({
  label, value, accentColor, blinking = false, subtitle
}) => {
  const colors = ACCENT_COLORS[accentColor];
  return (
    <div
      style={{
        borderTop: `4px solid ${colors.border}`,
        backgroundColor: colors.bg,
        borderRadius: '8px',
        padding: '20px 24px',
        boxShadow: '0 2px 8px rgba(0,0,0,0.08)',
        flex: 1,
        minWidth: '180px',
      }}
    >
      <div style={{
        fontSize: '42px',
        fontWeight: 700,
        fontFamily: 'Cambria, Georgia, serif',
        color: colors.text,
        lineHeight: 1.1,
      }}>
        {value}
      </div>
      <div style={{
        fontSize: '13px',
        fontWeight: 700,
        color: '#37474F',
        marginTop: '6px',
        fontFamily: 'Calibri, sans-serif',
        textTransform: 'uppercase',
        letterSpacing: '0.04em',
      }}>
        {label}
      </div>
      {subtitle && (
        <div style={{
          fontSize: '11px',
          color: '#78909C',
          marginTop: '4px',
          fontFamily: 'Calibri, sans-serif',
        }}>
          {subtitle}
        </div>
      )}
    </div>
  );
};
