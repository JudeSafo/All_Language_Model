import type { NextApiRequest, NextApiResponse } from 'next';
import axios from 'axios';

const handler = async (req: NextApiRequest, res: NextApiResponse) => {
  if (req.method === 'POST') {
    try {
      const { text, mode, json_file } = req.body; // Extract the json_file field from the request body

      // Log the request payload
      console.log('Request payload for generate_summary:', { text, mode, json_file });

      const response = await axios.post('http://3.133.103.207/generate_summary', { text, mode, json_file });

      // Check if the external API response contains an error
      if (response.data.error) {
        console.error('External API error:', response.data.error);
        return res.status(500).json({ error: response.data.error });
      }

      res.status(200).json(response.data);
    } catch (error) {
      console.error('Error fetching summary:', error);
      res.status(500).json({ error: 'An error occurred while processing the request.' });
    }
  } else {
    res.status(405).json({ error: 'Method not allowed.' });
  }
};

export default handler;

