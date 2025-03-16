import React, { useEffect, useState } from "react";
import { Box, Typography, Button, LinearProgress, CircularProgress } from "@mui/material";
import { Link } from "react-router-dom";
import axios from "axios";


interface DailyTask {
  day_number: number;
  topic_name: string;
  objectives: string;
  wrong_count: number;
  total_questions: number;
}

const Dashboard = () => {
  const [progress, setProgress] = useState<number>(0);
  const [loading, setLoading] = useState(false);
  const [studyPlanExists, setStudyPlanExists] = useState<boolean>(false);
  const [topReviewTasks, setTopReviewTasks] = useState<DailyTask[]>([]);

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

    const fetchTopReviewTasks = async () => {
      try {
        setLoading(true);
        const response = await axios.get("http://localhost:5000/api/top-review-tasks");
        setTopReviewTasks(response.data);
        setLoading(false);
      } catch (error) {
        console.error("Error fetching top review tasks:", error);
        setLoading(false);
      }
    };

    const fetchStudyPlanExistence = async () => {
      try {
        const response = await axios.get("http://localhost:5000/api/study-plan");
        setStudyPlanExists(response.data.study_plan_exists);
      } catch (error) {
        console.error("Error checking study plan existence:", error);
      }
    };

    fetchProgress();
    fetchTopReviewTasks();
    fetchStudyPlanExistence();
  }, []);

  return (
    
    <Box p={4}>
      <Typography variant="h4">WELCOME BACK TO STUDY 🎓</Typography>
      <Typography variant="subtitle1" mt={2}>YOUR PROGRESS:</Typography>
      <LinearProgress variant="determinate" value={progress} sx={{ height: 10, borderRadius: 5, mt: 1 }} />
      <Typography variant="body2" mt={1}>{progress}% COMPLETED</Typography>

      <Box mt={3}>
        <Typography variant="h6">📌 RECOMMENDED REVIEW CONTENT</Typography>
        {loading ? (
          <Box display="flex" justifyContent="center" mt={2}>
            <CircularProgress />
          </Box>
        ) : (
          <>
            {/* Display Top Review Tasks */}
            {topReviewTasks.length > 0 ? (
              <ul>
                {topReviewTasks.map((task, index) => (
                  <li key={index}>
                    <strong>{task.topic_name}</strong> (Day {task.day_number}) - 
                    <em> {task.objectives}</em>
                    <br />
                    <small>
                      Wrong Count: {task.wrong_count} | Total Questions: {task.total_questions}
                    </small>
                  </li>
                ))}
              </ul>
            ) : (
              <Typography variant="subtitle1" sx={{ mt: 2, color: "gray" }}>
                No recommended review tasks available.
              </Typography>
            )}
          </>
        )}
      </Box>

      <Box p={4}>
      {/* Conditionally Render Based on Study Plan Existence */}
      {studyPlanExists ? (
        <>
          {/* If a study plan exists */}
          <Typography variant="h6">You already have a study plan!</Typography>
          <Box mt={3}>
            <Button variant="contained" color="primary" component={Link} to="/practice">
              Start Practicing
            </Button>
            <Button variant="outlined" color="secondary" component={Link} to="/schedule" sx={{ ml: 2 }}>
              View Your Study Plan
            </Button>
          </Box>
        </>
      ) : (
        <>
          {/* If no study plan exists */}
          <Typography variant="h6" sx={{ mb: 2 }}>
            No study plan found. Please upload study material.
          </Typography>
          <Box mt={3}>
            <Button variant="contained" color="primary" component={Link} to="/notes">
              Upload Material
            </Button>
          </Box>
        </>
      )}
    </Box>
    </Box>
  );
};

export default Dashboard;