import React, { useState } from 'react';
import axios from 'axios';

export default function Quiz({ questions }) {
  const [answers, setAnswers] = useState({});

  const handleSubmit = async (e) => {
    e.preventDefault();
    const response = await axios.post('http://localhost:5000/api/submit', {
      answers: Object.values(answers),
      weak_areas: Object.keys(answers).filter(k => !answers[k].correct)
    });
    // Handle results display
  };

  return (
    <form onSubmit={handleSubmit}>
      {questions.map((q, index) => (
        <div key={index} className="question-card">
          <h3>{q.question}</h3>
          {q.options.map((option, optIndex) => (
            <label key={optIndex}>
              <input
                type="radio"
                name={`q${index}`}
                onChange={() => setAnswers({
                  ...answers,
                  [index]: {
                    option: optIndex,
                    correct: optIndex === q.correct
                  }
                })}
              />
              {option.replace(' (Correct)', '')}
            </label>
          ))}
        </div>
      ))}
      <button type="submit">Submit Answers</button>
    </form>
  );
}