import React, { useState, useEffect } from "react";
import { Box, Typography, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, CircularProgress } from "@mui/material";
import axios from "axios";

interface DailyTask {
  id: number;
  day_number: number;
  topic_name: string;
  objectives: string;
  completed: boolean;
  total_questions: number;
  wrong_count: number;
}

const Schedule = () => {
  const [loading, setLoading] = useState(false);
  const [dailyTasks, setDailyTasks] = useState<DailyTask[]>([]);

  useEffect(() => {
    fetchDailyTasks();
  }, []);

  // Extract key topics from database
  const fetchDailyTasks = async () => {
    try {
      setLoading(true);
      const response = await axios.get("http://127.0.0.1:5001/api/daily-tasks");
      setDailyTasks(response.data);
      setLoading(false);
    } catch (error) {
      console.error("Error fetching daily tasks:", error);
    }
  };

  return (
    <Box p={4}>
      {/* Loading Indicator */}
      {loading ? (
        <Box display="flex" justifyContent="center" mt={4}>
          <CircularProgress />
        </Box>
      ) : (
        <>
          {/* Display Daily Tasks */}
          {dailyTasks.length > 0 ? (
            <TableContainer component={Paper} sx={{ mt: 3 }}>
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell>Day</TableCell>
                    <TableCell>Topic</TableCell>
                    <TableCell>Objectives</TableCell>
                    <TableCell>Completed</TableCell>
                    <TableCell>Total Questions</TableCell>
                    <TableCell>Wrong Count</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {dailyTasks.map((task) => (
                    <TableRow key={task.id}>
                      <TableCell>{task.day_number}</TableCell>
                      <TableCell>{task.topic_name}</TableCell>
                      <TableCell>{task.objectives}</TableCell>
                      <TableCell>{task.completed ? "Yes" : "No"}</TableCell>
                      <TableCell>{task.total_questions}</TableCell>
                      <TableCell>{task.wrong_count}</TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          ) : (
            <Typography variant="subtitle1" sx={{ mt: 2, color: "gray" }}>
              No daily tasks found.
            </Typography>
          )}
        </>
      )}
    </Box>
  );
};

export default Schedule;