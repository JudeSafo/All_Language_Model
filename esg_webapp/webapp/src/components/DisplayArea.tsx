import React from 'react';

interface DisplayAreaProps {
  content: string;
}

const DisplayArea: React.FC<DisplayAreaProps> = ({ content }) => {
  return <div>{content}</div>;
};

export default DisplayArea;

