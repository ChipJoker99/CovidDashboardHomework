import React from 'react';
import type { RegionalData } from '../types/regionalData';
import type { SortableField, SortOrder } from '../App';
import './RegionTable.css';

interface RegionTableProps {
  data: RegionalData[];
  isLoading: boolean;
  error: string | null;
  onSort: (field: SortableField) => void;
  currentSortBy: SortableField;
  currentSortOrder: SortOrder;
}

const RegionTable: React.FC<RegionTableProps> = ({ 
  data, 
  isLoading, 
  error,
  onSort,
  currentSortBy,
  currentSortOrder
}) => {

  const getSortIndicator = (field: SortableField): string => {
    if (currentSortBy === field) {
      return currentSortOrder === 'asc' ? ' ▲' : ' ▼';
    }
    return '';
  };

  if (isLoading && data.length === 0 && !error) {
    return <div className="status-message">Loading data...</div>;
  }
  
  if (error && (!isLoading || data.length === 0)) {
    return <div className="status-message error-message">Error: {error}</div>;
  }
  
  if (!isLoading && !error && data.length === 0) {
    return <div className="status-message">No data available for the selected criteria.</div>;
  }

  return (
    <div className="table-wrapper">
      {isLoading && data.length > 0 && (
        <div className="status-message updating-message">Updating data...</div>
      )}
      <table className="region-table">
        <thead>
          <tr>
            <th 
              onClick={() => !isLoading && onSort('region_name')}
              className={`${currentSortBy === 'region_name' ? 'active' : ''} sortable ${isLoading ? 'disabled' : ''}`}
            >
              Region Name{getSortIndicator('region_name')}
            </th>
            <th 
              onClick={() => !isLoading && onSort('total_positive_cases')}
              className={`${currentSortBy === 'total_positive_cases' ? 'active' : ''} sortable ${isLoading ? 'disabled' : ''}`}
            >
              Total Positive Cases{getSortIndicator('total_positive_cases')}
            </th>
            <th>
              Submission Date 
            </th> 
          </tr>
        </thead>
        <tbody>
          {(data && data.length > 0) ? (
            data.map((region) => (
              <tr key={region.region_code + region.submission_date}>
                <td>{region.region_name}</td>
                <td>{region.total_positive_cases.toLocaleString()}</td>
                <td>{region.submission_date}</td>
              </tr>
            ))
          ) : (
            <tr>
              <td colSpan={3} className="status-message">No data to display.</td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
};

export default RegionTable;