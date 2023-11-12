import React from 'react'
import {Badge, Card, CardActionArea, CardContent, CardMedia,
    Modal, Typography, Box, Button, TextField,} from "@mui/material";


const NewListing = (props) => {

    const handleNewBid = async () => {

        const response = await fetch('http://localhost:8080/newListing', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                item_name: "Child slave",
                item_description: "Straight from Mongolia, well disciplined",
                start_date: "filler",
                end_date: "???",
                price: 1230.0,
                photo: "b",
            }),
        });
        if (!response.ok) {
            console.log(response.ok)
            throw new Error('User was not registered');
        }
    };
    return (
            <>
                <Button
                    sx={{
                        position: 'absolute',
                        right: 5,
                    }}
                    onClick={handleNewBid}
                >
                    Make New Request
                </Button>
            </>
        );

}

export default NewListing