import React from 'react';

function DateInput({ selectedDate, onDateChange }) {
  const today = new Date().toISOString().split('T')[0]; // Format: YYYY-MM-DD

  return (
    <div style={{ margin: '20px', color: '#FBFAE4' }}>
      <label htmlFor="date-picker">2. Izberi datum:</label><br />
      <input
        id="date-picker"
        type="date"
        max={today}
        value={selectedDate}
        onChange={(e) => onDateChange(e.target.value)}
        style={{
          padding: '8px',
          marginTop: '5px',
          borderRadius: '4px',
          border: '1px solid #ccc',
          backgroundColor: '#256b68',
          color: '#FBFAE4'
        }}
      />
    </div>
  );
}

export default DateInput;


