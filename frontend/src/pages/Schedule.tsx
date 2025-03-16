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
  

  

  // Extract key topics from database
  const dailyTasks = [
    {
      id: 1,
      day_number: 1,
      topic_name: "File Management",
      objectives: "Learn to use ls, mkdir, cp, and rm commands by practicing with simple commands and examples.",
      completed: false
    },
    {
      id: 2,
      day_number: 2,
      topic_name: "Process Management",
      objectives: "Learn to use ps, kill, and bg commands to manage processes by understanding how to list running processes and stop/resume jobs.",
      completed: true
    },
    {
      id: 3,
      day_number: 3,
      topic_name: "File Permissions",
      objectives: "Learn to use chmod and chown commands to change file permissions by practicing with different permission settings.",
      completed: false
    },
    {
      id: 4,
      day_number: 4,
      topic_name: "Terminal Navigation",
      objectives: "Learn to use cd, pwd, and mkdir commands to navigate directories and understand the concept of path.",
      completed: true
    },
    {
      id: 5,
      day_number: 5,
      topic_name: "File Search and Navigation",
      objectives: "Learn to use locate, grep, and find commands to search for files and navigate the file system.",
      completed: false
    },
    {
      id: 6,
      day_number: 6,
      topic_name: "Copying and Renaming",
      objectives: "Learn to use cp, mv, and rename commands to copy and rename files.",
      completed: true
    },
    {
      id: 7,
      day_number: 7,
      topic_name: "Networking Basics",
      objectives: "Learn basic networking commands like ping, netstat, and ssh to understand networking in Linux.",
      completed: false
    }
  ];
  

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
                  </TableRow>
                </TableHead>
                <TableBody>
                  {dailyTasks.map((task) => (
                    <TableRow key={task.id}>
                      <TableCell>{task.day_number}</TableCell>
                      <TableCell>{task.topic_name}</TableCell>
                      <TableCell>{task.objectives}</TableCell>
                      <TableCell>{task.completed ? "Yes" : "No"}</TableCell>
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