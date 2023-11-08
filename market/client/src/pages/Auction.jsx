import React from 'react';
import Listing from '../components/auction/Listing';

const Auction = () => {

    console.log("Auction page reached");

    const tempProp = {
        image: "favicon.ico",
        title: "Child Slave",
        description: "straight from Mongolia",
        price: 1000,
        end: 202311302359, // YYYYMMDD, time (military)
        bidder: "none",
    }

    return (
        <Listing {...tempProp} />
    );
}

export default Auction;