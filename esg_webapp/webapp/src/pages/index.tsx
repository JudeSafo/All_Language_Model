import React from 'react';
import Dropdown from '../components/Dropdown';
import PDFViewer from '../components/PDFViewer';
import QueryInput from '../components/QueryInput';
import DisplayArea from '../components/DisplayArea';
import axios from 'axios';

const HomePage: React.FC = () => {
  const [selectedPDF, setSelectedPDF] = React.useState('');
  const [displayContent, setDisplayContent] = React.useState('');
  const [query, setQuery] = React.useState(''); // Define the query state here

  const handleDropdownChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    setSelectedPDF(event.target.value);
    setQuery(''); // Clear the query state when the dropdown selection changes
    setDisplayContent(''); // Clear the display content when the dropdown selection changes
  };

  const handleQuestion = async (query: string) => {
    setDisplayContent('Answer to the question goes here');
  };

  const handleSummarize = async (query: string) => {
    setDisplayContent('Summary goes here');
  };

  // Derive the JSON file name from the selected PDF file
  const getJsonFileName = () => {
    if (!selectedPDF) return '';
    const pdfName = selectedPDF.split('/').pop();
    return pdfName?.replace('.pdf', '_parsed_sections.json') || '';
  };

  return (
    <div className="app-container">
      <header>
        <Dropdown
          options={[
            { value: '/pdfs/Post_Holdings_ESG_Report.pdf', label: 'POST' },
            { value: '/pdfs/KraftHeinz-2022-ESG-Report.pdf', label: 'KRAFT' },
            { value: '/pdfs/General_Mills.pdf', label: 'GEN' },
            { value: '/pdfs/pepsico-2022-green-bond-report.pdf', label: 'PEPSI' },
            { value: '/pdfs/2019_Business_Report_Coca-Cola_Company.pdf', label: 'COKE' },
            { value: '/pdfs/KELLOGG_COMPANYS_GLOBAL_CODE_OF_ETHICS.pdf', label: 'KELLOG' },
          ]}
          onChange={handleDropdownChange}
          selectedValue={selectedPDF} // Pass the selectedPDF state as the selectedValue prop
        />
      </header>
      <main style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', height: '100%' }}>
        <div className="pdf-viewer" style={{ height: '100%', display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
          <PDFViewer file={selectedPDF} />
        </div>
        <div className="query-section" style={{ height: '100%', display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
          <QueryInput
            jsonFileName={getJsonFileName()} // Pass the derived JSON file name as a prop
            onAnswerReceived={handleQuestion}
            onSummaryReceived={handleSummarize}
            query={query} // Pass the query state as a prop
            setQuery={setQuery} // Pass the setQuery function as a prop
          />
          <DisplayArea content={displayContent} />
        </div>
      </main>
    </div>
  );
};

export default HomePage;
