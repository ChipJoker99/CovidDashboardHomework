import React, { useState } from 'react';
import './DateSelector.css';

interface DateSelectorProps {
  onDateChange: (date: string | null) => void;
  initialDate?: string | null;
}

const DateSelector: React.FC<DateSelectorProps> = ({ onDateChange, initialDate }) => {
  const getTodayString = () => new Date().toISOString().split('T')[0];

  const [selectedDate, setSelectedDate] = useState<string>(initialDate || getTodayString());

  const handleDateChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setSelectedDate(event.target.value);
    onDateChange(event.target.value);
  };

  const handleShowToday = () => {
    const today = getTodayString();
    setSelectedDate(today);
    onDateChange(null);
  };

  const minDate = "2020-02-24";
  const maxDate = getTodayString();

  return (
    <div className="date-selector-container">
      <label htmlFor="report-date">Select Report Date: </label>
      <input
        type="date"
        id="report-date"
        value={selectedDate}
        onChange={handleDateChange}
        min={minDate}
        max={maxDate}
      />
      <button onClick={handleShowToday} className="today-button">
        Show Latest Data
      </button>
    </div>
  );
};

export default DateSelector;