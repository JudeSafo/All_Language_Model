import React from 'react';

interface DropdownOption {
  value: string;
  label: string;
}

interface DropdownProps {
  options: DropdownOption[];
  onChange: (event: React.ChangeEvent<HTMLSelectElement>) => void;
  selectedValue: string; // Add a new prop for the selected value
}

const Dropdown: React.FC<DropdownProps> = ({ options, onChange, selectedValue }) => {
  return (
    <select onChange={onChange} value={selectedValue}> 
      <option value="">Select a PDF</option>
      {options.map((option, index) => (
        <option key={index} value={option.value}>
          {option.label}
        </option>
      ))}
    </select>
  );
};

export default Dropdown;

