import React from 'react';
import Listing from '../components/auction/Listing';
import Navbar from '../components/Navbar'

const Auction = () => {

    console.log("Auction page reached");

    const tempPropsList = [
        {
            image: "favicon.ico",
            title: "Child Slave",
            description: "straight from Mongolia",
            price: 1000,
            end: 202311302359, // YYYYMMDD, time (military)
            bidder: "none",
        },
        {
            image: "favicon.ico",
            title: "Adult Slave",
            description: "straight from Czech Republic",
            price: 3000,
            end: 202311302359, // YYYYMMDD, time (military)
            bidder: "none",
        },
    ];

    return (
        <>
            <Navbar></Navbar>
            <div style={{ display: 'flex', gap: '20px', marginTop: '20px' }}>
                {tempPropsList.map((tempProp, index) => (
                    <Listing key={index} {...tempProp} />
                ))}
            </div>
        </>
    );
}

export default Auction;