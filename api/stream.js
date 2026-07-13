const play = require('play-dl');

module.exports = async (req, res) => {
  // Set CORS headers
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS');
  
  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  const videoId = req.query.videoId;
  
  if (!videoId) {
    return res.status(400).json({ error: 'videoId is required' });
  }

  try {
    const videoUrl = `https://www.youtube.com/watch?v=${videoId}`;
    
    // Set headers for audio streaming
    res.setHeader('Content-Type', 'audio/mp4');
    res.setHeader('Transfer-Encoding', 'chunked');

    // Get the audio stream using play-dl
    const streamSource = await play.stream(videoUrl, { discordPlayerCompatibility: false });
    
    // play.stream returns an object with a .stream property which is a PassThrough stream
    const audioStream = streamSource.stream;

    audioStream.on('error', (err) => {
      console.error('play-dl stream error:', err);
      if (!res.headersSent) {
        res.status(500).json({ error: 'Failed to stream audio' });
      } else {
        res.end();
      }
    });

    // Pipe the stream directly to the HTTP response
    audioStream.pipe(res);
  } catch (error) {
    console.error('Server error:', error);
    if (!res.headersSent) {
      res.status(500).json({ error: error.message });
    }
  }
};
