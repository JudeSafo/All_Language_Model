import React from 'react';
import axios from 'axios';

interface QueryInputProps {
  jsonFileName: string;
  onAnswerReceived: (answer: string) => void;
  onSummaryReceived: (summary: string) => void;
  query: string; // Add this prop to receive the query state
  setQuery: (query: string) => void; // Add this prop to receive the setQuery function
}

const QueryInput: React.FC<QueryInputProps> = ({ jsonFileName, onAnswerReceived, onSummaryReceived, query, setQuery }) => {
  const handleQuestionClick = async () => {
    try {
      const response = await axios.post('/api/answer_question', { text: query, json_file: jsonFileName });
      const answerText = response.data.answer;
      onAnswerReceived(answerText);
    } catch (error) {
      console.error('Error fetching answer:', error);
    }
  };

  const handleSummarizeClick = async () => {
    try {
      const response = await axios.post('/api/generate_summary', { text: query, mode: 'lengthen', json_file: jsonFileName });
      const summaryArray = response.data.summary;
      if (summaryArray && summaryArray.length > 0) {
        const summaryText = summaryArray[0].summary_text;
        onSummaryReceived(summaryText);
      }
    } catch (error) {
      console.error('Error fetching summary:', error);
    }
  };

  const buttonStyle = {
    backgroundColor: 'blue',
    color: 'white',
    padding: '8px 16px',
    margin: '0 4px',
    border: 'none',
    cursor: 'pointer',
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
      <textarea
        value={query} // Use the query prop as the value
        onChange={(e) => setQuery(e.target.value)} // Use the setQuery prop to update the query state
        style={{ width: '400px', height: '100px', marginBottom: '10px' }}
        placeholder="Enter your query here..."
      />
      <div>
        <button style={buttonStyle} onClick={handleQuestionClick}>
          Question
        </button>
        <button style={buttonStyle} onClick={handleSummarizeClick}>
          Summarize
        </button>
      </div>
    </div>
  );
};

export default QueryInput;
