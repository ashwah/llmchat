const express = require('express');

// A simple node js app that send a bit of sample json on its root path.
const app = express();

app.get('/', (req, res) => {
    const sampleJson = {
        message: 'Hello, test!'
    };
    res.json(sampleJson);
});

app.listen(3000, () => {
    console.log('Server is running on port 3000');
});
