/* eslint-disable import/prefer-default-export */
import axios from "axios";

// Object to store OAuth token information
const token = {
    access_token: "",
    expires_in: -1,
    token_type: "",
    updated_date: new Date(),
};

// Function to generate a new OAuth token
const generateToken = async () => {
    // Sending a POST request to Twitch's OAuth token endpoint to obtain a new token
    const auth = await axios({
        method: "POST",
        url: `https://id.twitch.tv/oauth2/token?client_id=${process.env.TWITCH_CLIENT_ID}&client_secret=${process.env.TWITCH_CLIENT_SECRET}4&grant_type=client_credentials`,
    });

    // Updating the token object with the obtained token information
    token.access_token = auth.data.access_token;
    token.expires_in = auth.data.expires_in;
    token.token_type = auth.data.token_type;
    token.check_date = new Date();
};

// Function to validate the existing token
const validateToken = async () => {
    try {
        // Sending a GET request to Twitch's token validation endpoint
        const valid = await axios({
            method: "GET",
            url: "https://id.twitch.tv/oauth2/validate",
            headers: {
                Authorization: `Bearer ${token.access_token}`,
            },
        });


        // Updating the token expiration time and check date
        token.expires_in = valid.data.expires_in;
        token.check_date = new Date();
    } catch (err) {
        // generate a new token if validation fails
        generateToken();
    }
};

// Middleware function for token authentication and validation
export const authenticate = () => {
    // If access token is empty, generate a new token
    if (token.access_token === "") {
        generateToken();
    }


    // If the token has not been updated in 15 days, validate it
    if ((new Date() - token.updated_date) / 86400000 >= 15) {
        validateToken();
    }

    return token;
};

// Function to add a webhook subscription for Twitch user stream events
export const addHook = async (username) => {
    // Authenticate to obtain a valid token
    const authToken = authenticate();

    try {
        // Fetching user information from Twitch API
        const user = await axios({
            method: "GET",
            url: `https://api.twitch.tv/helix/users?login=${username}`,
            headers: {
                Authorization: `Bearer ${authToken.access_token}`,
                "Client-ID": process.env.TWITCH_CLIENT_ID,
            },
        });

        const userid = user.data.data[0].id;

        // Constructing the webhook subscription request body
        const body = {
            version: "1",
            type: "stream.online",
            condition: {
                broadcaster_user_id: userid,
            },
            transport: {
                method: "webhook",
                callback: "https://ggst-discord.herokuapp.com",
                secret: process.env.SECRET,
            },
        };

        // Sending a POST request to add the webhook subscription
        await axios({
            method: "POST",
            url: process.env.TWITCH_SUB,
            headers: {
                Authorization: `Bearer ${authToken.access_token}`,
                "Client-ID": process.env.TWITCH_CLIENT_ID,
            },
            data: body,
        });

        return "success";
    } catch (err) {
        if (err.response.data.message === "subscription already exists") { return "exists"; }
        return err.response.data;
    }
};