# Esports Manager Challenge for VCT

1. Project Overview

Esports Manager Challenge for VCT is a front-end web application that allows users to chat with using AI. Users can ask AI questions, there will be some APIs for requests of users. They can interact with AI through a chat interface. The application will be built using NextJS14/React with TypeScript for the front-end and Python for the backend.

2. Core Features

A Chat interface

- This interface can be similar to ChatGPT
- Allow users to chat with AI
- Application will send request to the back-end which will built on AWS bedrock and we will implement in another application then, now we can use a mock API implementation
- AI will use the back-end response and interact with users

3. Technical Stack

- Frontend: NextJS 14 and React with TypeScript
- Backend(implement by another project): NextJS API Routes
- UI Components: Shadcn
- CSS: Tailwind CSS
- API Requests: axios
- Full-text Serach: lunr.js
- State Management: Redux Toolkit

4. API Routes

- /api/chat
POST `/`: Send a message and get AI response

5. User Interface Design

## Color Palette

- Deep Blue: #1A237E
- Teal: #00BFA5
- Coral: #FF5252
- Light Gray: #F5F5F5
- Dark Gray: #424242

## Typography

- Primary Font: Roboto
- Heading Font: Montserrat

## Logo

- A stylized ‘VCT AI Manager’ text where the ‘AI’ transforms into a lightning

## Layout

- Clean, uncluttered interface
- Intuitive navigation
- Responsive design for desktop and mobile
