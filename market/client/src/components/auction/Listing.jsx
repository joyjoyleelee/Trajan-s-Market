import React from 'react'
import {
  Badge,
  Card,
  CardActionArea,
  CardContent,
  CardMedia,
  Modal,
  Typography,
  Box,
  Button,
} from "@mui/material";

const Listing = (props) => {
    const [price, setPrice] = ""
    const [bidder, setBidder] = ""
    const [open, setOpen] = React.useState(false);

    const handleModalOpen = () => {
        setOpen(true);
    };
    const handleModalClose = () => {
        setOpen(false);
    };

    return (
        <Badge badgeContent={"$" + props.price} color="success">
            <Card sx={{ maxWidth: 345 }}>
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

    )
}

export default Listing