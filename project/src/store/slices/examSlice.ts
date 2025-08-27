import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';
import api from '../../services/api';

interface Choice {
  id: number;
  choice_text: string;
}

interface Question {
  id: number;
  question_text: string;
  choices: Choice[];
}

interface Exam {
  id: number;
  title: string;
  description: string;
  duration_minutes: number;
  total_questions: number;
  difficulty: string;
}

interface ExamSession {
  session_id: string;
  exam: Exam;
  start_time: string;
  status: string;
  score?: number;
  total_questions: number;
  correct_answers: number;
}

interface ExamState {
  availableExams: Exam[];
  currentSession: ExamSession | null;
  questions: Question[];
  currentQuestionIndex: number;
  answers: Record<number, number | null>;
  timeRemaining: number;
  isLoading: boolean;
  error: string | null;
  result: ExamSession | null;
}

const initialState: ExamState = {
  availableExams: [],
  currentSession: null,
  questions: [],
  currentQuestionIndex: 0,
  answers: {},
  timeRemaining: 0,
  isLoading: false,
  error: null,
  result: null,
};

export const fetchAvailableExams = createAsyncThunk(
  'exam/fetchAvailableExams',
  async (_, { rejectWithValue }) => {
    try {
      const response = await api.get('/exams/available/');
      return response.data;
    } catch (error: any) {
      return rejectWithValue(error.response.data);
    }
  }
);

export const startExam = createAsyncThunk(
  'exam/startExam',
  async (examId: number, { rejectWithValue }) => {
    try {
      const response = await api.post(`/exams/${examId}/start/`);
      return response.data;
    } catch (error: any) {
      return rejectWithValue(error.response.data);
    }
  }
);

export const fetchExamQuestions = createAsyncThunk(
  'exam/fetchExamQuestions',
  async (sessionId: string, { rejectWithValue }) => {
    try {
      const response = await api.get(`/exams/session/${sessionId}/questions/`);
      return response.data;
    } catch (error: any) {
      return rejectWithValue(error.response.data);
    }
  }
);

export const submitAnswer = createAsyncThunk(
  'exam/submitAnswer',
  async (payload: { sessionId: string; questionId: number; choiceId: number | null }, { rejectWithValue }) => {
    try {
      const response = await api.post(`/exams/session/${payload.sessionId}/answer/`, {
        question_id: payload.questionId,
        choice_id: payload.choiceId,
      });
      return response.data;
    } catch (error: any) {
      return rejectWithValue(error.response.data);
    }
  }
);

export const submitExam = createAsyncThunk(
  'exam/submitExam',
  async (sessionId: string, { rejectWithValue }) => {
    try {
      const response = await api.post(`/exams/session/${sessionId}/submit/`);
      return response.data;
    } catch (error: any) {
      return rejectWithValue(error.response.data);
    }
  }
);

const examSlice = createSlice({
  name: 'exam',
  initialState,
  reducers: {
    setCurrentQuestionIndex: (state, action: PayloadAction<number>) => {
      state.currentQuestionIndex = action.payload;
    },
    setAnswer: (state, action: PayloadAction<{ questionId: number; choiceId: number | null }>) => {
      state.answers[action.payload.questionId] = action.payload.choiceId;
    },
    setTimeRemaining: (state, action: PayloadAction<number>) => {
      state.timeRemaining = action.payload;
    },
    clearExam: (state) => {
      state.currentSession = null;
      state.questions = [];
      state.currentQuestionIndex = 0;
      state.answers = {};
      state.timeRemaining = 0;
      state.result = null;
      state.error = null;
    },
    clearError: (state) => {
      state.error = null;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchAvailableExams.fulfilled, (state, action) => {
        state.availableExams = action.payload;
      })
      .addCase(startExam.fulfilled, (state, action) => {
        state.currentSession = action.payload.session;
        state.error = null;
      })
      .addCase(fetchExamQuestions.fulfilled, (state, action) => {
        state.questions = action.payload.questions;
        state.timeRemaining = 5*60;
      })
      .addCase(submitExam.fulfilled, (state, action) => {
        state.result = action.payload.result;
        state.currentSession = null;
      })
      .addMatcher(
        (action) => action.type.endsWith('/pending'),
        (state) => {
          state.isLoading = true;
          state.error = null;
        }
      )
      .addMatcher(
        (action) => action.type.endsWith('/fulfilled'),
        (state) => {
          state.isLoading = false;
        }
      )
      .addMatcher(
        (action) => action.type.endsWith('/rejected'),
        (state, action: PayloadAction<any>) => {
          state.isLoading = false;
          state.error = action.payload.error || 'Something went wrong';
        }
      );
  },
});

export const { setCurrentQuestionIndex, setAnswer, setTimeRemaining, clearExam, clearError } = examSlice.actions;
export default examSlice.reducer;