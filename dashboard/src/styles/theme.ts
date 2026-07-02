export const colors = {
  teal: {
    900: '#004D40',
    800: '#00695C',
    700: '#00796B',
    600: '#00897B',
    light: '#E0F2F1',
    mid: '#B2DFDB',
    accent: '#4DD0C4',
  },
  amber: {
    800: '#FF8F00',
    700: '#FFA000',
    light: '#FFF8E1',
    xlight: '#FFFDE7',
  },
  neutral: {
    dark: '#212121',
    mid: '#37474F',
    grey500: '#607D8B',
    grey400: '#78909C',
    cardBorder: '#CFD8DC',
    divider: '#ECEFF1',
    offWhite: '#FAFAFA',
    white: '#FFFFFF',
  },
  semantic: {
    alertRed: '#C62828',
    redLight: '#FF6B6B',
    successGreen: '#2E7D32',
    warningOrange: '#E65100',
    darkBg: '#1A1A2E',
    veryDark: '#1B2B2A',
  },
} as const;

export const typography = {
  fontFamily: {
    body: '"Calibri", "Roboto", "Segoe UI", sans-serif',
    heading: '"Cambria", "Georgia", serif',
    mono: '"Consolas", "Courier New", monospace',
  },
  fontSize: {
    display: '52px',
    sectionTitle: '28px',
    cardHeading: '18px',
    body: '14px',
    caption: '11px',
    badge: '12px',
    kpi: '42px',
  },
} as const;

export const spacing = {
  lineHeight: '1.5',
  headingLineHeight: '1.2',
  paragraphGap: '8px',
  sectionGap: '24px',
  letterSpacingLabel: '0.04em',
} as const;
