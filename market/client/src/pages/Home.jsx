import { Button, Grid, Container, Modal } from '@mui/material';
import React, { useState } from 'react';
import LoginModal from '../../components/home/LoginModal';
import SignupModal from '../../components/home/SignupModal';

const Home = () => {
  const [logOpen, setLog] = useState(false)
  const [regOpen, setReg] = useState(false)

  const handleLogOpen = () =>{
    setLog(true)
  }

  const handleLogClose = () =>{
    setLog(false)
  }

  const handleRegOpen = () =>{
    setReg(true)
  }

  const handleRegClose = () =>{
    setReg(false)
  }

  return (
      <h1>404 Home Found</h1>
  )
}

export default Home