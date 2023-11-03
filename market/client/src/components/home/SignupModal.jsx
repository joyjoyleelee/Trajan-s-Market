import { TextField, Button, Container, Grid } from '@mui/material';
import React, { useState } from 'react';

const SignupModal = ({handleClose}) =>{
    const [username,setUser] = useState('')
    const [password, setPass] = useState('')
    const [disName, setDisName] = useState('')

    const handleUser = (e) => {
        setUser(e.target.value);
    };

    const handlePass = (e) => {
        setPass(e.target.value);
    };

    const handleDisName = (e) => {
        setDisName(e.target.value);
    };

    const sendData = () =>{
        //TODO: Implement send to backend
        handleClose();
    }

    return (
        <Container maxWidth="auto"
                   style={{ display: 'flex',
                       alignItems: 'center',
                       justifyContent: 'center',
                       backgroundColor: 'lightgrey',
                       minHeight: 'auto',
                       padding:'10px',}}>
            <Grid container spacing={2}>
            <Grid item xs={12}>
                <TextField
                    label="Username"
                    required
                    type="text"
                    variant="outlined"
                    value={username}
                    onChange={handleUser}
                />
            </Grid>
            <Grid item xs={12}>
                <TextField
                    label="Password"
                    required
                    type="password"
                    variant="outlined"
                    onChange={handlePass}
                    value={password}
                />
            </Grid>
            <Grid item xs={12}>
                <TextField
                    label="Display Name"
                    required
                    type="text"
                    variant="outlined"
                    onChange={handleDisName}
                    value={disName}
                />
            </Grid>
            <Grid item xs={6}>
                <Button
                    onClick={sendData}
                    variant="contained"
                    color="primary"
                    sx={{ width: '150px', height: '50px'}}
                >
                    Change Password
                </Button>
            </Grid>
            <Grid item xs={6}>
                <Button
                    onClick={handleClose}
                    variant="contained"
                    color="primary"
                    sx={{ width: '150px', height: '50px'}}
                >
                    Cancel
                </Button>
            </Grid>
        </Grid>
    </Container>
    );
};

export default SignupModal