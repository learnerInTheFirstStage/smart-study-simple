import React, { useEffect, useState } from "react";
import axios from "axios";
import { Box, Typography, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper } from "@mui/material";

interface DailyTask {
  id: number;
  day_number: number;
  topic_name: string;
  wrong_count: number;
  total_questions: number;
  error_rate: number;
}

const Performance = () => {
  const [tasks, setTasks] = useState<DailyTask[]>([]);

  useEffect(() => {
    fetchPerformanceData();
  }, []);

  const fetchPerformanceData = async () => {
    try {
      const response = await axios.get("http://localhost:5000/api/performance-analysis");
      setTasks(response.data);
    } catch (error) {
      console.error("Error fetching performance analysis:", error);
    }
  };
  return (
    <Box p={4}>
      <Typography variant="h4">📊 Performance Analysis</Typography>

      {tasks.length > 0 ? (
        <TableContainer component={Paper} sx={{ mt: 3 }}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Day</TableCell>
                <TableCell>Topic</TableCell>
                <TableCell>Wrong Answers</TableCell>
                <TableCell>Total Questions</TableCell>
                <TableCell>Error Rate</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {tasks.map((task) => (
                <TableRow key={task.id}>
                  <TableCell>{`Day ${task.day_number}`}</TableCell>
                  <TableCell>{task.topic_name}</TableCell>
                  <TableCell>{task.wrong_count}</TableCell>
                  <TableCell>{task.total_questions}</TableCell>
                  <TableCell>{(task.error_rate * 100).toFixed(2)}%</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      ) : (
        <Typography sx={{ mt: 2, color: "gray" }}>No performance data available.</Typography>
      )}
    </Box>
  );
};

export default Performance;