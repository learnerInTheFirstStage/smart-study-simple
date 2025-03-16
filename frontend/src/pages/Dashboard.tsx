import React, { useEffect, useState } from "react";
import { Box, Typography, Button, LinearProgress } from "@mui/material";
import { Link } from "react-router-dom";
import axios from "axios";

const Dashboard = () => {
  const [progress, setProgress] = useState<number>(0);

  useEffect(() => {
    const fetchProgress = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:5000/api/completed-tasks-count');
        setProgress(response.data.completed_tasks_count);
      }
      catch (error) {
        console.error('Error fetching completed tasks count:', error);
      }
    }
    fetchProgress();
  }, []);

  return (
    
    <Box p={4}>
      <Typography variant="h4">WELCOME BACK TO STUDY 🎓</Typography>
      <Typography variant="subtitle1" mt={2}>YOUR PROGRESS:</Typography>
      <LinearProgress variant="determinate" value={progress} sx={{ height: 10, borderRadius: 5, mt: 1 }} />
      <Typography variant="body2" mt={1}>{progress}% COMPLETED</Typography>

      <Box mt={3}>
        <Typography variant="h6">📌 RECOMMENDED REVIEW CONTENT</Typography>
        <ul>
          <li>Data Structure - Hash Table</li>
          <li>Algorithm - Recursive Optimization</li>
          <li>Computer Network - TCP/IP Basics</li>
        </ul>
      </Box>

      <Box mt={3}>
        <Button variant="contained" color="primary" component={Link} to="/practice">Start Practicing</Button>
        <Button variant="outlined" color="secondary" component={Link} to="/schedule" sx={{ ml: 2 }}>View Your Study Plan</Button>
      </Box>
    </Box>
  );
};

export default Dashboard;