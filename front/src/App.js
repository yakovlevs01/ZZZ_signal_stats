import React from 'react';
import DataTable from './components/DataTable';
import { ThemeProvider, useTheme } from './ThemeContext';
import styled from 'styled-components';

// Стилизация основного контейнера приложения
const AppContainer = styled.div`
    background-color: ${({ theme }) => theme.background};
    color: ${({ theme }) => theme.color};
    min-height: 100vh;
    padding: 20px;
`;

const ToggleButton = styled.button`
    background-color: ${({ theme }) => theme.color};
    color: ${({ theme }) => theme.background};
    border: none;
    padding: 10px 20px;
    cursor: pointer;
    margin-bottom: 20px;
`;

const App = () => {
  const { toggleTheme } = useTheme();

  return (
    <AppContainer>
      <ToggleButton onClick={toggleTheme}>Toggle Theme</ToggleButton>
      <DataTable />
    </AppContainer>
  );
};

// Обертываем App в ThemeProvider, чтобы обеспечить доступ к теме во всем приложении
export default function WrappedApp() {
  return (
    <ThemeProvider>
      <App />
    </ThemeProvider>
  );
}
