import { TextField, Button, Container, Grid } from '@mui/material';
import React, { useState } from 'react';

const SignupModal = ({navigate, handleClose}) =>{
    const [usernames,setUser] = useState('')
    const [passwords, setPass] = useState('')
    var redirect = 0;

    const handleUser = (e) => {
        setUser(e.target.value);
    };

    const handlePass = (e) => {
        setPass(e.target.value);
    };

    const handleRedirect = (e) => {
        console.log("value below should update")
        console.log(e);
        redirect = e
        console.log(redirect);
    }

    const sendData = async () => {
        //TODO: Implement send to backend
        const response = await fetch('http://localhost:8080/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                username: usernames,
                password: passwords,
            }),
        });
        if (!response.ok) {
            throw new Error('User was not logged in');
        }

        const responseData = await response.json();
        console.log(responseData);
        console.log("last statement was responseData")
        handleRedirect(responseData);
        handleClose();
    }

    const changeLink = () =>{
        console.log("Checking if redirect");
        console.log(typeof redirect);
        console.log(redirect);
        if (redirect === 1){
            console.log("Redirecting");
            navigate("/Auction");
        }
    }

    const clicked = async () =>{
        await sendData();
        changeLink();
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
                    value={usernames}
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
                    value={passwords}
                />
            </Grid>
            <Grid item xs={6}>
                <Button
                    onClick={clicked}
                    variant="contained"
                    color="primary"
                    sx={{ width: '150px', height: '50px'}}
                >
                    Login
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