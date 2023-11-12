import { TextField, Button, Container, Grid } from '@mui/material';
import React, { useState } from 'react';

const NewListingModal = () =>{
    const [name, setName] = setState("")
    const [descr, setDescr] = setState("")
    const [price, setPrice] = setPrice("")
    const [yearEnd, setYearEnd] = setState(0)
    const [monthEnd, setMonthEnd] = setState(0)
    const [dayEnd, setDayEnd] = setState(0)

    const handleName = (e) => {
        setName(e.target.value);
    };

    const handleDescr = (e) =>{
        setDescr(e.target.value);
    };

    const handlePrice = (e) =>{
        setPrice(e.target.value)
    }

    const handleYear = (e) =>{
        setYearEnd(e.target.value)
    }

    const handleMonth = (e) =>{
        setMonthEnd(e.target.value)
    }

    const setDay = (e) =>{
        setDayEnd(e.target.value)
    }

    return (<></>);
};

export default NewListingModal