import type { NextApiRequest, NextApiResponse } from 'next';
import fs from 'fs';
import path from 'path';

const logFilePath = path.join(process.cwd(), 'logs.json');

const handler = async (req: NextApiRequest, res: NextApiResponse) => {
  if (req.method === 'POST') {
    try {
      const logData = req.body;

      fs.readFile(logFilePath, 'utf-8', (err, data) => {
        if (err) {
          console.error('Error reading logs:', err);
          res.status(500).json({ error: 'An error occurred while reading the logs.' });
          return;
        }

        const logs = JSON.parse(data);
        logs.push(logData);

        fs.writeFile(logFilePath, JSON.stringify(logs, null, 2), 'utf-8', (writeErr) => {
          if (writeErr) {
            console.error('Error writing logs:', writeErr);
            res.status(500).json({ error: 'An error occurred while writing the logs.' });
          } else {
            res.status(200).json({ message: 'Log saved successfully.' });
          }
        });
      });
    } catch (error) {
      console.error('Error logging user interaction:', error);
      res.status(500).json({ error: 'An error occurred while logging user interaction.' });
    }
  } else {
    res.status(405).json({ error: 'Method not allowed.' });
  }
};

export default handler;

