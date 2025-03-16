// import React, { useEffect, useState } from "react";
// import axios from "axios";
// import { Box, Typography, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper } from "@mui/material";

// interface DailyTask {
//   id: number;
//   day_number: number;
//   topic_name: string;
//   wrong_count: number;
//   total_questions: number;
//   error_rate: number;
// }

// const Performance = () => {
//   const [tasks, setTasks] = useState<DailyTask[]>([]);

//   useEffect(() => {
//     fetchPerformanceData();
//   }, []);

//   const fetchPerformanceData = async () => {
//     try {
//       const response = await axios.get("http://localhost:5001/api/performance-analysis");
//       setTasks(response.data);
//     } catch (error) {
//       console.error("Error fetching performance analysis:", error);
//     }
//   };
//   return (
//     <Box p={4}>
//       <Typography variant="h4">📊 Performance Analysis</Typography>

//       {tasks.length > 0 ? (
//         <TableContainer component={Paper} sx={{ mt: 3 }}>
//           <Table>
//             <TableHead>
//               <TableRow>
//                 <TableCell>Day</TableCell>
//                 <TableCell>Topic</TableCell>
//                 <TableCell>Wrong Answers</TableCell>
//                 <TableCell>Total Questions</TableCell>
//                 <TableCell>Error Rate</TableCell>
//               </TableRow>
//             </TableHead>
//             <TableBody>
//               {tasks.map((task) => (
//                 <TableRow key={task.id}>
//                   <TableCell>{`Day ${task.day_number}`}</TableCell>
//                   <TableCell>{task.topic_name}</TableCell>
//                   <TableCell>{task.wrong_count}</TableCell>
//                   <TableCell>{task.total_questions}</TableCell>
//                   <TableCell>{(task.error_rate * 100).toFixed(2)}%</TableCell>
//                 </TableRow>
//               ))}
//             </TableBody>
//           </Table>
//         </TableContainer>
//       ) : (
//         <Typography sx={{ mt: 2, color: "gray" }}>No performance data available.</Typography>
//       )}
//     </Box>
//   );
// };

// export default Performance;
import React from "react";
import { Box, Typography } from "@mui/material";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, Line, ResponsiveContainer } from "recharts";

const data = [
  { day: "Day 1", topic: "Recursion", completed: 10, correct: 7, accuracy: 70 },
  { day: "Day 2", topic: "Sorting", completed: 12, correct: 9, accuracy: 75 },
  { day: "Day 3", topic: "Dynamic Prog.", completed: 15, correct: 10, accuracy: 66 },
  { day: "Day 4", topic: "Graphs", completed: 9, correct: 7, accuracy: 77 },
  { day: "Day 5", topic: "Greedy", completed: 14, correct: 11, accuracy: 78 },
  { day: "Day 6", topic: "Binary Search", completed: 11, correct: 9, accuracy: 81 },
  { day: "Day 7", topic: "Divide & Conq.", completed: 13, correct: 12, accuracy: 92 },
];

const Performance = () => {
  return (
    <Box p={4}>
      <Typography variant="h4">📊 Performance Analysis</Typography>

      <ResponsiveContainer width="100%" height={400}>
        <BarChart data={data} margin={{ top: 30, right: 50, left: 0, bottom: 30 }}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="day" />
          {/* 左边 Y 轴 for 完成 & 正确数量 */}
          <YAxis yAxisId="left" />
          {/* 右边 Y 轴 for accuracy % */}
          <YAxis yAxisId="right" orientation="right" domain={[0, 100]} tickFormatter={(value) => `${value}%`}/>
          <Tooltip />
          <Legend />
          <Bar yAxisId="left" dataKey="completed" fill="#8884d8" name="Completed" />
          <Bar yAxisId="left" dataKey="correct" fill="#82ca9d" name="Correct" />
          <Line
            yAxisId="right"
            type="monotone"
            dataKey="accuracy"
            stroke="#ff7300"
            strokeDasharray="5 5"
            name="Accuracy (%)"
          />
        </BarChart>
      </ResponsiveContainer>
    </Box>
  );
};

export default Performance;