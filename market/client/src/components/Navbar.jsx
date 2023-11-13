import React from 'react';
import { AppBar, Toolbar, Button, Typography } from '@mui/material';
import { Link } from 'react-router-dom';

const Navbar = () => {

    const deleteCookie = (cookieName) => {
        document.cookie = `${cookieName}=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;`;
    };


    const handleLogout = async () => {
        // Add your logout logic here
        deleteCookie("cookie_name")
        const response = await fetch('http://localhost:8080/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body:{
                Data: 'Delete the cookie'
            },
        });
        if (!response.ok) {
            throw new Error('User was not logged out');
        }

        const responseData = await response.json();
        console.log(responseData);
    };

    return (
        <AppBar position="static">
            <Toolbar>
                <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
                    My Auction App
                </Typography>
                <Button color="inherit" component={Link} to="/Auction">
                    Auction
                </Button>
                <Button color="inherit" component={Link} to="/Winnings">
                    Auctions Won
                </Button>
                <Button color="inherit" component={Link} to="/MyAuction">
                    Auctions Posted
                </Button>
                <Button color="inherit" onClick={handleLogout} component={Link} to="/">
                    Logout
                </Button>
            </Toolbar>
        </AppBar>
    );
};

export default Navbar;