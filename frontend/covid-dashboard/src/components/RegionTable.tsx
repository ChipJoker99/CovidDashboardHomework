import React from 'react';
import type { RegionalData } from '../types/regionalData';
import './RegionTable.css';

interface RegionTableProps {
  data: RegionalData[];
  isLoading: boolean;
  error: string | null;
}

const RegionTable: React.FC<RegionTableProps> = ({ data, isLoading, error }) => {
  if (isLoading) {
    return <div className="status-message">Loading data...</div>;
  }

  if (error) {
    return <div className="status-message error-message">Error: {error}</div>;
  }

  if (!data || data.length === 0) {
    return <div className="status-message">No data available for the selected criteria.</div>;
  }

  return (
    <table className="region-table">
      <thead>
        <tr>
          <th>Region Name</th>
          <th>Total Positive Cases</th>
          <th>Submission Date</th> 
        </tr>
      </thead>
      <tbody>
        {data.map((region) => (
          <tr key={region.region_code + region.submission_date}>
            <td>{region.region_name}</td>
            <td>{region.total_positive_cases.toLocaleString()}</td>
            <td>{region.submission_date}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
};

export default RegionTable;