import ChatBot from 'react-simple-chatbot';
import React, { useState } from 'react';
import { ThemeProvider } from 'styled-components';
import bot from '../assets/bot.jpg';
import userbotimg from '../assets/user.jpg';
import axios from 'axios';
import ReactMarkdown from 'react-markdown';

const theme = {
  background: 'white',
  headerBgColor: '#237518',
  headerFontColor: 'white',
  headerFontSize: '25px',
  botBubbleColor: '#386150',
  botFontColor: 'white',
  userBubbleColor: '#778f45',
  userFontColor: 'white',
};

function CustChatBot() {
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState('');
  const [generatingAnswer, setGeneratingAnswer] = useState(false);

  async function generateAnswer(questionText, triggerNextStep) {
    setGeneratingAnswer(true);
    setAnswer('Loading your answer... It might take up to 10 seconds');
    try {
      const response = await axios({
        url: `https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=${
          import.meta.env.VITE_API_GENERATIVE_LANGUAGE_CLIENT
        }`,
        method: 'post',
        data: {
          contents: [{ parts: [{ text: questionText }] }],
        },
      });
  
      setAnswer(response.data.candidates[0].content.parts[0].text);
    } catch (error) {
      console.log(error);
      setAnswer('Sorry - Something went wrong. Please try again!');
    }
  
    setGeneratingAnswer(false);
    triggerNextStep();  // Ensure the next step is triggered after the answer is received
  }
  

  const steps = [
    {
      id: '1',
      message: 'What is your question?',
      trigger: 'userInput',
    },
    {
      id: 'userInput',
      user: true,
      trigger: ({ value }, triggerNextStep) => {
        setQuestion(value);  // Set the user input as the question
        generateAnswer(value, triggerNextStep);  // Trigger AI model and trigger the next step after response
      },
    },
    {
      id: 'aiResponse',
      component: (
        <div>
          <ReactMarkdown>{answer}</ReactMarkdown>  {/* Display AI response */}
        </div>
      ),
      asMessage: true,
      trigger: '1',  // Loop back to ask another question
    },
  ];
  

  return (
    <div
      style={{
        width: 'auto',
        padding: '14px',
        height: 'auto',
        position: 'fixed',
        bottom: '75px',
        left: '1px',
      }}
    >
      <ThemeProvider theme={theme}>
        <ChatBot
          headerTitle="PlantRX bot"
          botAvatar={bot}
          userAvatar={userbotimg}
          steps={steps}
          recognitionEnable={true}
          speechSynthesis={{ enable: true, lang: 'hi' }}
          recognitionPlaceholder={'Listening'}
          enableMobileAutoFocus={true}
          enableSmoothScroll={true}
          width={'400px'}
          opened={true}
        />
      </ThemeProvider>
    </div>
  );
}

export default CustChatBot;
