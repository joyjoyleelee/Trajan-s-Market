import React from 'react'
import {Badge, Card, CardActionArea, CardContent, CardMedia,
    Modal, Typography, Box, Button, TextField,} from "@mui/material";

const Listing = (props) => {
    const [bidPrice, setBid] = React.useState(0);
    const [open, setOpen] = React.useState(false);

    const handleModalOpen = () => {
        setOpen(true);
    };
    const handleModalClose = () => {
        setOpen(false);
    };

    const newBid = (e) => {
        setBid(e.target.value);
    };

    const handleNewBid = () => {
        // TODO: Add code to update price and current bidder
        handleModalClose();
    };

    return (
        <>
            <Badge badgeContent={"$" + props.price} color="success">
                <Card sx={{ width: 200, height: 275 }}>
                    <CardActionArea onClick={handleModalOpen}>
                        <CardMedia
                            component="img"
                            height="140"
                            image={props.image}
                            alt="Unable to load image"
                        />
                            <CardContent>
                                <Typography gutterBottom variant="h5" component="div">
                                    {props.title.substring(0, 20)}
                                </Typography>
                                <Typography variant="body2" color="text.secondary">
                                    {props.description.substring(0, 50) + "..."}
                                </Typography>
                            </CardContent>
                    </CardActionArea>
                </Card>
            </Badge>
            <Modal
                open = {open}
                onClose = {handleModalClose}
                aria-labelledby="modal-modal-title"
                aria-describedby="modal-modal-description"
            >
                <Box
                    sx={{
                        position: "absolute",
                        top: "50%",
                        left: "50%",
                        transform: "translate(-50%, -50%)",
                        width: 400,
                        bgcolor: "background.paper",
                        border: "1px solid #000",
                        boxShadow: 24,
                        p: 4,
                    }}
                >
                    <Button
                        sx={{
                            position: 'absolute',
                            top: 0,
                            right: 0,
                        }}
                        onClick={handleModalClose}
                    >
                        x
                    </Button>
                    <img
                        src={props.image}
                        alt="Unable to load image"
                        width="140"
                        height="140"
                    />
                    <Typography id="modal-item-title" variant="h6" component="h2">
                        {props.title}
                    </Typography>
                    <Typography id="modal-item-description" sx={{ mt: 2 }}>
                        <i>{props.description}</i>
                    </Typography>
                    <Typography id="modal-item-price" sx={{ mt: 2 }}>
                        <>{"$" + props.price}</>
                    </Typography>
                    <Typography id="modal-item-end" sx={{ mt: 2 }}>
                        <>{props.end}</>
                    </Typography>
                    <Typography id="modal-modal-bidder" sx={{ mt: 2 }}>
                        <>Current Bidder: {props.bidder}</>
                    </Typography>
                    <TextField
                        label="New Bid"
                        required
                        type="text"
                        variant="outlined"
                        onChange={newBid}
                        value={bidPrice}
                    />
                    <Button
                        sx={{
                            position: 'absolute',
                            bottom: 5,
                            right: 5,
                        }}
                        onClick={handleNewBid}
                    >
                        Place Bid
                    </Button>
                </Box>
            </Modal>
        </>
    )
}

export default Listing