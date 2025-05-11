import React, { useState, useEffect, useCallback } from 'react';
import './App.css';
import RegionTable from './components/RegionTable';
import DateSelector from './components/DateSelector';
import { getRegionalData } from './services/apiService';
import type { RegionalData } from './types/regionalData';

function App() {
  const [regionalData, setRegionalData] = useState<RegionalData[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedDateString, setSelectedDateString] = useState<string | null>(null); 

  const fetchData = useCallback(async (dateString: string | null) => {
    setIsLoading(true);
    setError(null);
    try {
      const data = await getRegionalData(dateString, 'total_positive_cases', 'desc');
      setRegionalData(data);
    } catch (err) {
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError('An unknown error occurred');
      }
      setRegionalData([]);
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchData(selectedDateString);
  }, [fetchData, selectedDateString]);

  const handleDateChange = (newDateString: string | null) => {
    setSelectedDateString(newDateString);
  };
  
  const getTodayForSelector = () => new Date().toISOString().split('T')[0];

  return (
    <div className="App">
      <header className="app-header">
        <h1>Italian COVID-19 Regional Data</h1>
      </header>
      <main>
        <DateSelector 
          onDateChange={handleDateChange} 
          initialDate={selectedDateString || getTodayForSelector()}
        />
        <RegionTable data={regionalData} isLoading={isLoading} error={error} />
      </main>
      <footer className="app-footer">
        <p>Data sourced from Protezione Civile Italiana.</p>
      </footer>
    </div>
  );
}

export default App;