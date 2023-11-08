import React from 'react'
import Navbar from '../components/Navbar'
import StaticListing from "../components/winnings/StaticListing";

const Winnings = () => {

    const tempPropsList = [
        {
            image: "favicon.ico",
            title: "Child Slave",
            description: "straight from Mongolia",
            price: 1000,
            end: 202311012359, // YYYYMMDD, time (military)
            bidder: "none",
        },
        {
            image: "favicon.ico",
            title: "Adult Slave",
            description: "straight from Czech Republic",
            price: 3000,
            end: 202311012359, // YYYYMMDD, time (military)
            bidder: "none",
        },
    ];

    return (
        <>
            <Navbar></Navbar>
            <div style={{ display: 'flex', gap: '20px', marginTop: '20px' }}>
                {tempPropsList.map((tempProp, index) => (
                    <StaticListing key={index} {...tempProp} />
                ))}
            </div>
        </>
    )
}

export default Winnings