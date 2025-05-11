import React, { useState, useEffect, useCallback } from 'react';
import './App.css';
import RegionTable from './components/RegionTable';
import DateSelector from './components/DateSelector';
import { getRegionalData } from './services/apiService';
import type { RegionalData, SortableField, SortOrder } from './types/regionalData';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faDownload } from '@fortawesome/free-solid-svg-icons';

const API_BASE_URL_FOR_EXPORT = import.meta.env.VITE_API_BACKEND_URL || 'http://127.0.0.1:8000/api/v1';

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

  const handleExport = () => {

    const params = new URLSearchParams();

    if (selectedDateString) {
      params.append('report_date', selectedDateString);
    }

    params.append('sort_by', sortBy);
    params.append('sort_order', sortOrder);

    const queryString = params.toString();
    const exportUrl = `${API_BASE_URL_FOR_EXPORT}/export/regions.xlsx${queryString ? `?${queryString}` : ''}`;
    
    console.log("Export URL:", exportUrl); // DEBUG LOG

    window.open(exportUrl, '_blank'); 
  };

  return (
    <div className="App">
      <header className="app-header">
        <h1>Italian COVID-19 Regional Data</h1>
      </header>
      <main>
      <div className="controls-container">
          <DateSelector 
            onDateChange={handleDateChange} 
            initialDate={selectedDateString || getTodayForSelector()}
          />
          <button 
            onClick={handleExport} 
            className="export-button" 
            disabled={isLoading || !!error || regionalData.length === 0}
            title="Download data as Excel file"
          >
            <FontAwesomeIcon icon={faDownload} style={{ marginRight: '8px' }}/>
            Download Fetched Data
          </button>
        </div>
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