import { useState } from 'react';
import { Routes, Route } from 'react-router-dom';
import Dashboard from './components/Dashboard';
import Quiz from './components/Quiz';
import './index.css';

function App() {
  const [questions, setQuestions] = useState([]);
  const [score, setScore] = useState(null);
  const [studyPlan, setStudyPlan] = useState('');

  return (
    <div className="app-container">
      <Routes>
        <Route 
          path="/" 
          element={
            <Dashboard 
              onUploadSuccess={(data) => {
                setQuestions(data.questions);
                setScore(null);
              }}
            />
          } 
        />
        <Route 
          path="/quiz" 
          element={
            <Quiz 
              questions={questions} 
              onSubmission={(result) => {
                setScore(result.score);
                setStudyPlan(result.studyPlan);
              }}
            />
          } 
        />
      </Routes>
      
      {studyPlan && (
        <div className="study-plan">
          <h3>个性化学习计划</h3>
          <pre>{studyPlan}</pre>
        </div>
      )}
    </div>
  );
}

export default App;