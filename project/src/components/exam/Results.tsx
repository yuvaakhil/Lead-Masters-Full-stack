import React from 'react';
import { useSelector } from 'react-redux';
import { useNavigate } from 'react-router-dom';
import { CheckCircle, XCircle, RotateCcw, Home, Trophy, Target, Clock } from 'lucide-react';
import { RootState } from '../../store/store';

const Results: React.FC = () => {
  const navigate = useNavigate();
  const { result } = useSelector((state: RootState) => state.exam);

  if (!result) {
    navigate('/dashboard');
    return null;
  }

  const getScoreColor = (score: number) => {
    if (score >= 80) return 'text-green-600';
    if (score >= 60) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getPerformanceText = (score: number) => {
    if (score >= 90) return 'Excellent!';
    if (score >= 80) return 'Great job!';
    if (score >= 70) return 'Good work!';
    if (score >= 60) return 'Not bad!';
    return 'Keep practicing!';
  };

  const formatDuration = (startTime: string, endTime: string) => {
    const start = new Date(startTime);
    const end = new Date(endTime);
    const durationMs = end.getTime() - start.getTime();
    const minutes = Math.floor(durationMs / 60000);
    const seconds = Math.floor((durationMs % 60000) / 1000);
    return `${minutes}m ${seconds}s`;
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="text-center">
            <Trophy className="w-16 h-16 text-yellow-500 mx-auto mb-4" />
            <h1 className="text-3xl font-bold text-gray-900">Exam Complete!</h1>
            <p className="text-gray-600 mt-2">Here are your results</p>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Score Card */}
        <div className="bg-white rounded-xl shadow-sm border p-8 mb-8">
          <div className="text-center mb-8">
            <div className={`text-6xl font-bold mb-2 ${getScoreColor(result.score || 0)}`}>
              {Math.round(result.score || 0)}%
            </div>
            <h2 className="text-2xl font-semibold text-gray-900 mb-2">
              {getPerformanceText(result.score || 0)}
            </h2>
            <p className="text-gray-600">{result.exam.title}</p>
          </div>

          {/* Score Breakdown */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
            <div className="text-center p-4 bg-green-50 rounded-lg">
              <CheckCircle className="w-8 h-8 text-green-600 mx-auto mb-2" />
              <div className="text-2xl font-bold text-green-600">
                {result.correct_answers}
              </div>
              <p className="text-sm text-gray-600">Correct Answers</p>
            </div>

            <div className="text-center p-4 bg-red-50 rounded-lg">
              <XCircle className="w-8 h-8 text-red-600 mx-auto mb-2" />
              <div className="text-2xl font-bold text-red-600">
                {result.total_questions - result.correct_answers}
              </div>
              <p className="text-sm text-gray-600">Incorrect Answers</p>
            </div>

            <div className="text-center p-4 bg-blue-50 rounded-lg">
              <Target className="w-8 h-8 text-blue-600 mx-auto mb-2" />
              <div className="text-2xl font-bold text-blue-600">
                {result.total_questions}
              </div>
              <p className="text-sm text-gray-600">Total Questions</p>
            </div>
          </div>

          {/* Additional Details */}
          <div className="border-t pt-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="flex items-center space-x-3">
                <Clock className="w-6 h-6 text-gray-400" />
                <div>
                  <p className="text-sm text-gray-600">Time Taken</p>
                  <p className="font-medium text-gray-900">
                    {result.end_time && formatDuration(result.start_time, result.end_time)}
                  </p>
                </div>
              </div>

              <div className="flex items-center space-x-3">
                <Trophy className="w-6 h-6 text-gray-400" />
                <div>
                  <p className="text-sm text-gray-600">Difficulty</p>
                  <p className="font-medium text-gray-900 capitalize">
                    {result.exam.difficulty}
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Performance Analysis */}
        <div className="bg-white rounded-xl shadow-sm border p-8 mb-8">
          <h3 className="text-xl font-semibold text-gray-900 mb-4">Performance Analysis</h3>
          
          <div className="space-y-4">
            <div>
              <div className="flex justify-between mb-2">
                <span className="text-sm text-gray-600">Accuracy</span>
                <span className="text-sm font-medium">{Math.round(result.score || 0)}%</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div 
                  className={`h-2 rounded-full ${
                    (result.score || 0) >= 80 ? 'bg-green-500' :
                    (result.score || 0) >= 60 ? 'bg-yellow-500' : 'bg-red-500'
                  }`}
                  style={{ width: `${result.score || 0}%` }}
                ></div>
              </div>
            </div>

            <div className="pt-4 border-t">
              <h4 className="font-medium text-gray-900 mb-2">Recommendations</h4>
              <ul className="text-sm text-gray-600 space-y-1">
                {(result.score || 0) >= 80 ? (
                  <>
                    <li>• Excellent performance! You've mastered this topic.</li>
                    <li>• Consider taking more advanced exams to challenge yourself.</li>
                  </>
                ) : (result.score || 0) >= 60 ? (
                  <>
                    <li>• Good job! You have a solid understanding of the material.</li>
                    <li>• Review the topics you missed to improve further.</li>
                  </>
                ) : (
                  <>
                    <li>• Consider reviewing the study materials more thoroughly.</li>
                    <li>• Practice with similar questions to improve your understanding.</li>
                    <li>• Don't give up! Learning takes time and practice.</li>
                  </>
                )}
              </ul>
            </div>
          </div>
        </div>

        {/* Actions */}
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <button
            onClick={() => navigate('/dashboard')}
            className="flex items-center justify-center space-x-2 bg-gradient-to-r from-blue-600 to-indigo-600 text-white px-6 py-3 rounded-lg hover:from-blue-700 hover:to-indigo-700 transition-all duration-200"
          >
            <Home className="w-5 h-5" />
            <span>Back to Dashboard</span>
          </button>
        </div>
      </main>
    </div>
  );
};

export default Results;