export interface RegionalData {
    id: number;
    submission_date: string;
    region_code: string;
    region_name: string;
    total_positive_cases: number;
}

export type SortableField = 'region_name' | 'total_positive_cases';
export type SortOrder = 'asc' | 'desc';