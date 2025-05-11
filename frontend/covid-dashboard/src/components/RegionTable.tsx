import React from 'react';
import type { RegionalData, SortableField, SortOrder } from '../types/regionalData';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faSort, faSortUp, faSortDown } from '@fortawesome/free-solid-svg-icons';
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

  const getSortIcon = (field: SortableField) => {
    if (currentSortBy === field) {
      return currentSortOrder === 'asc' ? faSortUp : faSortDown;
    }
    return faSort;
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
              Region Name
              <FontAwesomeIcon icon={getSortIcon('region_name')} className="sort-icon" />
            </th>
            <th
              onClick={() => !isLoading && onSort('total_positive_cases')}
              className={`${currentSortBy === 'total_positive_cases' ? 'active' : ''} sortable ${isLoading ? 'disabled' : ''}`}
            >
              Total Positive Cases
              <FontAwesomeIcon icon={getSortIcon('total_positive_cases')} className="sort-icon" />
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