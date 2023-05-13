import '../styles/global.css';
import React, { useState } from 'react';
import Dropdown from '../components/Dropdown';
import PDFViewer from '../components/PDFViewer';
import QueryInput from '../components/QueryInput';
import DisplayArea from '../components/DisplayArea';
import type { AppProps } from 'next/app';

function MyApp({ Component, pageProps }: AppProps) {
  const defaultPDF = '/pdfs/Post_Holdings_ESG_Report.pdf';
  const [selectedPDF, setSelectedPDF] = useState(defaultPDF);
  const [displayContent, setDisplayContent] = useState('');
  const [query, setQuery] = useState(''); // Define the query state here

  const handleDropdownChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
    setSelectedPDF(event.target.value);
    setQuery(''); // Clear the query state when the dropdown selection changes
    setDisplayContent(''); // Clear the display content when the dropdown selection changes
  };

  const handleAnswerReceived = (answer: string) => {
    setDisplayContent(answer);
  };

  const handleSummaryReceived = (summary: string) => {
    setDisplayContent(summary);
  };

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
            { value: defaultPDF, label: 'POST' },
            { value: '/pdfs/KraftHeinz-2022-ESG-Report.pdf', label: 'KRAFT' },
            { value: '/pdfs/pepsico-2022-green-bond-report.pdf', label: 'PEPSI' },
            { value: '/pdfs/General_Mills.pdf', label: 'GEN' },
            { value: '/pdfs/2019_Business_Report_Coca-Cola_Company.pdf', label: 'COKE' },
            { value: '/pdfs/KELLOGG_COMPANYS_GLOBAL_CODE_OF_ETHICS.pdf', label: 'KELLOG' },
            // Add more options as needed
          ]}
          onChange={handleDropdownChange}
          selectedValue={selectedPDF} // Pass the selectedPDF state as the selectedValue prop
        />
      </header>
      <main>
        <div className="query-section">
          <QueryInput
            jsonFileName={getJsonFileName()}
            onAnswerReceived={handleAnswerReceived}
            onSummaryReceived={handleSummaryReceived}
            query={query} // Pass the query state as a prop
            setQuery={setQuery} // Pass the setQuery function as a prop
          />
          <DisplayArea content={displayContent} />
        </div>
        <div className="pdf-viewer">
          <PDFViewer file={selectedPDF} />
        </div>
      </main>
    </div>
  );
}

export default MyApp;
