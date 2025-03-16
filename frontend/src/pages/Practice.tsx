// import React, { useState, useEffect } from "react";
// import { Box, Typography, Button, Radio, RadioGroup, FormControlLabel, TextField, CircularProgress } from "@mui/material";

// interface Question {
//   id: number;
//   type: "multiple-choice" | "fill-in-the-blank" | "open-ended";
//   question: string;
//   options?: string[];
//   correctAnswer?: string; // AI-generated questions may not always have predefined answers
// }

// const Practice = () => {
//   const [questions, setQuestions] = useState<Question[]>([]);
//   const [index, setIndex] = useState(0);
//   const [selectedOption, setSelectedOption] = useState<string | null>(null);
//   const [userAnswer, setUserAnswer] = useState("");
//   const [result, setResult] = useState<string | null>(null);
//   const [loading, setLoading] = useState(true);
//   const [isFinished, setIsFinished] = useState(false);

//   const currentQuestion = questions[index];

//   // Fetch AI-generated questions from backend
//   useEffect(() => {
//     fetch("http://localhost:5000/api/questions") // Replace with actual backend URL
//       .then((res) => res.json())
//       .then((data) => {
//         setQuestions(data);
//         setLoading(false);
//       })
//       .catch((err) => {
//         console.error("Error fetching questions:", err);
//         setLoading(false);
//       });
//   }, []);

//   // Submit answer and store in localStorage + Backend
//   const submitAnswer = () => {
//     if (!currentQuestion) return;

//     const userResponse = {
//       questionId: currentQuestion.id,
//       question: currentQuestion.question,
//       userAnswer: currentQuestion.type === "multiple-choice" ? selectedOption : userAnswer,
//       correctAnswer: currentQuestion.correctAnswer || "N/A",
//       isCorrect: currentQuestion.correctAnswer
//         ? userAnswer.trim().toLowerCase() === currentQuestion.correctAnswer.toLowerCase()
//         : null, // Open-ended questions are not automatically graded
//       timestamp: new Date().toLocaleString(),
//     };

//     // Store quiz attempt in local storage
//     const storedHistory = JSON.parse(localStorage.getItem("quizHistory") || "[]");
//     storedHistory.push(userResponse);
//     localStorage.setItem("quizHistory", JSON.stringify(storedHistory));

//     // Send answer to backend for storage
//     fetch("http://localhost:5000/api/submit-answer", {
//       method: "POST",
//       headers: { "Content-Type": "application/json" },
//       body: JSON.stringify(userResponse),
//     })
//       .then((res) => res.json())
//       .then((data) => {
//         setResult(data.feedback || "✔ Answer submitted! (Self-review required)");
//       })
//       .catch((err) => {
//         console.error("Error submitting answer:", err);
//       });
//   };

//   // Move to next question or finish quiz
//   const handleNextQuestion = () => {
//     if (index < questions.length - 1) {
//       setIndex(index + 1);
//       setSelectedOption(null);
//       setUserAnswer("");
//       setResult(null);
//     } else {
//       setIsFinished(true);
//     }
//   };

//   return (
//     <Box p={4}>
//       <Typography variant="h4">You are in practicing zone!!! 📝</Typography>

//       {loading ? (
//         <CircularProgress />
//       ) : isFinished ? (
//         <Typography variant="h5" mt={4}>🎯 Quiz Completed! Check your results.</Typography>
//       ) : (
//         <>
//           <Typography variant="h5" mt={3}>{currentQuestion?.question}</Typography>

//           {/* Question Type: Multiple Choice */}
//           {currentQuestion?.type === "multiple-choice" && currentQuestion?.options && (
//             <RadioGroup value={selectedOption} onChange={(e) => setSelectedOption(e.target.value)}>
//               {currentQuestion.options.map((option, i) => (
//                 <FormControlLabel key={i} value={option} control={<Radio />} label={option} />
//               ))}
//             </RadioGroup>
//           )}

//           {/* Question Type: Fill-in-the-Blank */}
//           {currentQuestion?.type === "fill-in-the-blank" && (
//             <TextField label="Enter your answer" variant="outlined" fullWidth sx={{ mt: 2 }} value={userAnswer} onChange={(e) => setUserAnswer(e.target.value)} />
//           )}

//           {/* Question Type: Open-ended */}
//           {currentQuestion?.type === "open-ended" && (
//             <TextField
//               label="Write your answer"
//               multiline
//               rows={4}
//               variant="outlined"
//               fullWidth
//               sx={{ mt: 2 }}
//               value={userAnswer}
//               onChange={(e) => setUserAnswer(e.target.value)}
//             />
//           )}

//           {/* Submit Answer Button */}
//           {!result && (
//             <Button
//               variant="contained"
//               color="primary"
//               sx={{ mt: 2 }}
//               onClick={submitAnswer}
//               disabled={currentQuestion.type === "multiple-choice" ? !selectedOption : !userAnswer}
//             >
//               Submit Answer
//             </Button>
//           )}

//           {/* Next Question / View Results Button */}
//           {result && (
//             <Button
//               variant="contained"
//               color="secondary"
//               sx={{ mt: 2 }}
//               onClick={handleNextQuestion}
//             >
//               {index === questions.length - 1 ? "View Your Results" : "Next Question"}
//             </Button>
//           )}
//         </>
//       )}
//     </Box>
//   );
// };

// export default Practice;


// Static
import React, { useState, useEffect } from "react";
import { Box, Typography, Button, Radio, RadioGroup, FormControlLabel, TextField } from "@mui/material";
import axios from "axios";

interface Question {
  id: number;
  type: "multiple-choice" | "fill-in-the-blank" | "open-ended";
  question: string;
  options?: string[];
  correctAnswer: string;
}

const questions: Question[] = [
  { id: 1, type: "multiple-choice", question: "What is recursion?", options: ["Loop", "Function calling itself", "Data structure"], correctAnswer: "Function calling itself" },
  { id: 2, type: "fill-in-the-blank", question: "What does AI stand for?", correctAnswer: "Artificial Intelligence" },
  { id: 3, type: "open-ended", question: "Explain the concept of time complexity.", correctAnswer: "" },
];

const Practice = () => {
  const [index, setIndex] = useState(0);
  const [selectedOption, setSelectedOption] = useState<string | null>(null);
  const [userAnswer, setUserAnswer] = useState("");
  const [result, setResult] = useState<string | null>(null);
  const [timeLeft, setTimeLeft] = useState(30);
  const [score, setScore] = useState({ correct: 0, incorrect: 0 });
  const [isFinished, setIsFinished] = useState(false);

  const currentQuestion = questions[index];

  // Timer function
  useEffect(() => {
    if (timeLeft === 0) {
      setResult("⏳ Time's up! Try the next question.");
    }
    const timer = setInterval(() => {
      setTimeLeft((prev) => (prev > 0 ? prev - 1 : 0));
    }, 1000);
    return () => clearInterval(timer);
  }, [timeLeft]);

  // Submit answer and store in localStorage
  const submitAnswer = () => {
    if (!currentQuestion) return;

    // Normalize answers for correct comparison
    const formattedUserAnswer = currentQuestion.type === "multiple-choice"
    ? selectedOption?.trim().toLowerCase()
    : userAnswer.trim().toLowerCase();

    const formattedCorrectAnswer = currentQuestion.correctAnswer.trim().toLowerCase();

    const isCorrect = formattedUserAnswer === formattedCorrectAnswer;

    const userResponse = {
        questionId: currentQuestion.id,
        question: currentQuestion.question,
        userAnswer: selectedOption || userAnswer, // Store the raw answer
        correctAnswer: currentQuestion.correctAnswer,
        isCorrect: isCorrect,
        timestamp: new Date().toLocaleString(),
      };    

    // // Store quiz attempt in local storage
    // const storedHistory = JSON.parse(localStorage.getItem("quizHistory") || "[]");
    // storedHistory.push(userResponse);
    // localStorage.setItem("quizHistory", JSON.stringify(storedHistory));

    // // Trigger storage event to notify QuizHistory.tsx
    // window.dispatchEvent(new Event("storage"));

    // Update result message
    const handleSubmitAnswer = async (isCorrect: boolean | null, taskId: number) => {
      setResult(
        isCorrect === true
          ? "✅ Correct!"
          : isCorrect === false
          ? `❌ Incorrect. Correct answer: ${formattedCorrectAnswer}`
          : "✔ Answer submitted! (Self-review required)"
      );
    
      // Call API to update DailyTask
      try {
        await axios.post("http://localhost:5001/api/update-daily-task", {
          task_id: taskId,
          is_correct: isCorrect,
        });
        console.log("Daily task updated successfully!");
      } catch (error) {
        console.error("Error updating daily task:", error);
      }
    };

    handleSubmitAnswer(userResponse.isCorrect, userResponse.questionId);

    // Update score count
    if (userResponse.isCorrect === true) {
      setScore((prev) => ({ ...prev, correct: prev.correct + 1 }));
    } else if (userResponse.isCorrect === false) {
      setScore((prev) => ({ ...prev, incorrect: prev.incorrect + 1 }));
    }
  };

  // Move to the next question or finish the quiz
  const handleNextQuestion = () => {
    if (index < questions.length - 1) {
      setIndex(index + 1);
      setSelectedOption(null);
      setUserAnswer("");
      setResult(null);
      setTimeLeft(30);
    } else {
      setIsFinished(true);
    }
  };

  return (
    <Box p={4}>
      <Typography variant="h4">You are in practicing zone!!! 📝</Typography>

      {!isFinished ? (
        <>
          <Typography variant="h5" mt={3}>{currentQuestion.question}</Typography>

          {/* Timer Display */}
          <Typography variant="subtitle1" mt={1}>⏳ Time remaining: {timeLeft} seconds</Typography>

          {/* Question Type: Multiple Choice */}
          {currentQuestion.type === "multiple-choice" && currentQuestion.options && (
            <RadioGroup value={selectedOption} onChange={(e) => setSelectedOption(e.target.value)}>
              {currentQuestion.options.map((option, i) => (
                <FormControlLabel key={i} value={option} control={<Radio />} label={option} />
              ))}
            </RadioGroup>
          )}

          {/* Question Type: Fill-in-the-Blank */}
          {currentQuestion.type === "fill-in-the-blank" && (
            <TextField label="Enter your answer" variant="outlined" fullWidth sx={{ mt: 2 }} value={userAnswer} onChange={(e) => setUserAnswer(e.target.value)} />
          )}

          {/* Question Type: Open-ended */}
          {currentQuestion.type === "open-ended" && (
            <TextField
              label="Write your answer"
              multiline
              rows={4}
              variant="outlined"
              fullWidth
              sx={{ mt: 2 }}
              value={userAnswer}
              onChange={(e) => setUserAnswer(e.target.value)}
            />
          )}

          {/* Result Display */}
          {result && <Typography variant="h6" mt={2}>{result}</Typography>}

          {/* Submit Answer Button (Always Visible) */}
          {!result && (
            <Button
              variant="contained"
              color="primary"
              sx={{ mt: 2 }}
              onClick={submitAnswer}
              disabled={currentQuestion.type === "multiple-choice" ? !selectedOption : !userAnswer}
            >
              Submit Answer
            </Button>
          )}

          {/* Next Question / View Results Button */}
          {result && (
            <Button
              variant="contained"
              color="secondary"
              sx={{ mt: 2 }}
              onClick={handleNextQuestion}
            >
              {index === questions.length - 1 ? "View Your Results" : "Next Question"}
            </Button>
          )}
        </>
      ) : (
        // Summary Display after finishing all questions
        <Box mt={4}>
          <Typography variant="h5">🎯 Quiz Summary</Typography>
          <Typography variant="h6">✅ Correct Answers: {score.correct}</Typography>
          <Typography variant="h6">❌ Incorrect Answers: {score.incorrect}</Typography>
        </Box>
      )}
    </Box>
  );
};

export default Practice;