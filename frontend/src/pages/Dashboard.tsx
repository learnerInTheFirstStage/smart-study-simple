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
      } catch (error) {
        console.error('Error fetching completed tasks count:', error);
      }
    };

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
    <Box p={4} maxWidth="800px" mx="auto">
      <Typography variant="h4" mb={3} textAlign="center">🎓 WELCOME BACK TO STUDY</Typography>

      <Typography variant="subtitle1">YOUR PROGRESS:</Typography>
      <LinearProgress variant="determinate" value={progress} sx={{ height: 10, borderRadius: 5, mt: 1 }} />
      <Typography variant="body2" mt={1} mb={3}>{progress}% COMPLETED</Typography>

      {/* RECOMMENDED REVIEW CONTENT */}
      <Box>
        <Typography variant="h6">📌 RECOMMENDED REVIEW CONTENT</Typography>
        {loading ? (
          <Box display="flex" justifyContent="center" mt={2}>
            <CircularProgress />
          </Box>
        ) : (
          <>
            {topReviewTasks.length > 0 ? (
              <ul style={{ paddingLeft: "20px" }}>
                {topReviewTasks.map((task, index) => (
                  <li key={index} style={{ marginBottom: "10px" }}>
                    <strong>{task.topic_name}</strong> (Day {task.day_number}) - <em>{task.objectives}</em><br />
                    <small>Wrong Count: {task.wrong_count} | Total Questions: {task.total_questions}</small>
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

      {/* STUDY PLAN SECTION */}
      <Box mt={5}>
        <Typography variant="h6">📚 STUDY PLAN</Typography>
        {studyPlanExists ? (
          <Box mt={2}>
            <Typography variant="subtitle1">✅ YOU ALREADY HAVE A STUDY PLAN!</Typography>
            <Box mt={2} display="flex" gap={2}>
              <Button variant="contained" color="primary" component={Link} to="/practice" fullWidth>
                START PRACTICING
              </Button>
              <Button variant="outlined" color="secondary" component={Link} to="/schedule" fullWidth>
                VIEW YOUR STUDY PLAN
              </Button>
            </Box>
          </Box>
        ) : (
          <Box mt={2}>
            <Typography variant="subtitle1">❌ NO STUDY PLAN FOUND. PLEASE UPLOAD STUDY MATERIAL.</Typography>
            <Box mt={2}>
              <Button variant="contained" color="primary" component={Link} to="/notes" fullWidth>
                UPLOAD MATERIAL
              </Button>
            </Box>
          </Box>
        )}
      </Box>
    </Box>
  );
};

export default Dashboard;