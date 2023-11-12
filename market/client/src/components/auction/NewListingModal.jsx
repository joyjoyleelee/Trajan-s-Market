import { TextField, Button, Container, Grid } from '@mui/material';
import React, { useState } from 'react';

const NewListingModal = ({handleLogClose}) =>{
    const [name, setName] = setState("");
    const [descr, setDescr] = setState("");
    const [price, setPrice] = setPrice(1.0);
    const [endDate, setEndDate] = setState(null);
    const [photo, setPhoto] = setState(null);

    const handleName = (e) => {
        setName(e.target.value);
    };

    const handleDescr = (e) =>{
        setDescr(e.target.value);
    };

    const handlePrice = (e) =>{
        setPrice(e.target.value);
    };

    const handleDate = (date) =>{
        setEndDate(date);
    };

    const sendData = () =>{
    //     Send http
        handleLogClose()
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
            <Grid>
            {/*  Photo  */}
            </Grid>
            <Grid item xs={12}>
                <TextField
                    label="Item Name"
                    required
                    type="text"
                    variant="outlined"
                    value={name}
                    onChange={handleName}
                />
            </Grid>
            <Grid item xs={12}>
                <TextField
                    label="Item Description"
                    required
                    type="text"
                    variant="outlined"
                    onChange={handleDescr}
                    value={descr}
                    multiline
                    rows={4}
                />
            </Grid>
            <Grid item xs={12}>
                <TextField
                    label="Price"
                    required
                    type="number"
                    variant="outlined"
                    onChange={handlePrice}
                    value={price}
                />
            </Grid>
            <Grid>
            {/*    DATE*/}
            </Grid>
            <Grid item xs={6}>
                <Button
                    onClick={sendData}
                    variant="contained"
                    color="primary"
                    sx={{ width: '150px', height: '50px'}}
                >
                    Register
                </Button>
            </Grid>
            <Grid item xs={6}>
                <Button
                    onClick={handleLogClose}
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

export default NewListingModal