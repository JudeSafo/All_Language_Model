import React from 'react';

interface PDFViewerProps {
  file: string;
}

const PDFViewer: React.FC<PDFViewerProps> = ({ file }) => {
  if (!file) {
    return <div>No PDF file selected.</div>;
  }

  return (
    <iframe
      src={file}
      style={{ width: '80%', height: '80vh', border: 'none' }}
      title="PDF Viewer"
    ></iframe>
  );
};

export default PDFViewer;

