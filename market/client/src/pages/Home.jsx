import { Button, Grid, Container, Modal } from '@mui/material';
import React, { useState } from 'react';
// import LoginModal from '../../components/home/LoginModal';
// import SignupModal from '../../components/home/SignupModal';

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
       <Container maxWidth='auto'
             style={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                backgroundColor: 'lightgrey',
                minHeight: 'auto',
                padding: '10px',
             }}>
         <Grid container>
            <Grid item sx={{ margin: 'auto' }}>
              <Button
                onClick={handleLogOpen}
                variant='contained'
                color='primary'
                sx={{ width: '150px', height: '50px'}}
              >
                  Login
              </Button>
            </Grid>
            <Grid item sx={{ margin: 'auto' }}>
              <Button
                onClick={handleRegOpen}
                variant='contained'
                color='primary'
                sx={{ width: '150px', height: '50px'}}
              >
                  Register
              </Button>
            </Grid>
         </Grid>
       </Container>
  )
}

export default Home