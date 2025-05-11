import React, { useState, useEffect, useCallback } from 'react';
import './App.css';
import RegionTable from './components/RegionTable';
import DateSelector from './components/DateSelector';
import { getRegionalData } from './services/apiService';
import type { RegionalData } from './types/regionalData';

export type SortableField = 'region_name' | 'total_positive_cases';
export type SortOrder = 'asc' | 'desc';

function App() {
  const [regionalData, setRegionalData] = useState<RegionalData[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedDateString, setSelectedDateString] = useState<string | null>(null);
  const [sortBy, setSortBy] = useState<SortableField>('total_positive_cases');
  const [sortOrder, setSortOrder] = useState<SortOrder>('desc');

  const fetchData = useCallback(async (
    dateString: string | null,
    currentSortBy: SortableField,
    currentSortOrder: SortOrder
  ) => {
    setIsLoading(true);
    try {
      const data = await getRegionalData(dateString, currentSortBy, currentSortOrder);
      setRegionalData(data);
      setError(null);
    } catch (err) {
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError('An unknown error occurred');
      }
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchData(selectedDateString, sortBy, sortOrder);
  }, [fetchData, selectedDateString, sortBy, sortOrder]);

  const handleDateChange = (newDateString: string | null) => {
    setSelectedDateString(newDateString);
  };

  const handleSortChange = (newSortBy: SortableField) => {
    if (newSortBy === sortBy) {
      setSortOrder(prevOrder => (prevOrder === 'asc' ? 'desc' : 'asc'));
    } else {
      setSortBy(newSortBy);
      setSortOrder(newSortBy === 'total_positive_cases' ? 'desc' : 'asc');
    }
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
        <RegionTable 
          data={regionalData} 
          isLoading={isLoading} 
          error={error}
          onSort={handleSortChange}
          currentSortBy={sortBy}
          currentSortOrder={sortOrder}
        />
      </main>
      <footer className="app-footer">
        <p>Data sourced from Protezione Civile Italiana.</p>
        <p>Data organized by <a href="https://github.com/ChipJoker99">ChipJoker99</a>.</p>
      </footer>
    </div>
  );
}

export default App;