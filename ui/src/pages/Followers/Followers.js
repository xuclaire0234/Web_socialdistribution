/*
2023-03-22
pages/Followers/Followers.js
*/
import React, { useContext, useEffect, useState } from 'react';
import { Typography, IconButton } from '@mui/material';
import PersonRemoveIcon from '@mui/icons-material/PersonRemove';

import GridWrapper from '../../components/common/GridWrapper/GridWrapper';
import AuthContext from '../../context/AuthContext';
import Backend from '../../utils/Backend';
import PageHeader from '../../components/Page/PageHeader';
import AuthorCard from '../../components/Author/AuthorCard';
import SearchBar from '../../components/SearchBar/SearchBar';
import BasicCard from '../../components/common/BasicCard/BasicCard';
import { isValidHttpUrl, getInboxUrl } from '../../utils/Utils'

const Followers = () => {
    //  variable declarations -------------------------------------
    const [ followers, setFollowers ] = useState([]);
    const { user, authTokens, logoutUser } = useContext(AuthContext);
    const [ input, setInput ] = useState('');

    const handleChange = (event) => {
        setInput(event.target.value);
    }

    //  event listeners --------------------------------------------
    useEffect(() => {
        const getFollowers = async () => {
            const [response, data] = await Backend.get(`/api/authors/${user.user_id}/followers/`, authTokens.access);
            if (response.status && response.status === 200) {
                console.log('Got followers');
                console.log(data);
                setFollowers(data.items);
            } else if (response.statusText === 'Unauthorized'){
                logoutUser();
            } else {
                console.log('Failed to get followers');
            }
        };
        getFollowers();
    }, [ user, authTokens, logoutUser ]);

    const deleteFollower = async (follower, idx) => {
        const response = await Backend.delete(`/api/authors/${user.user_id}/followers/${follower.id}`, authTokens.access);
        if (response.status && response.status === 204) {
            console.log("Deleted Follower");
            followers.splice(idx,1);
            setFollowers([...followers]);
        } else if (response.statusText === 'Unauthorized'){
            logoutUser();
        } else {
            console.log('Failed to delete follower');
        }
    }
    
    // This is where we POST to the "object's" inbox
    const sendFollowRequest = async () => {
        console.log(input);
        if (!isValidHttpUrl(input)){
            return
        }
        let profile;
        const [response, data] = await Backend.get(`/api/authors/${user.user_id}/`, authTokens.access);
        if (response.status && response.status === 200) {
            console.log("Got profile ...");
            console.debug(data);
            profile = data;
        } else if (response.statusText === 'Unauthorized'){
            logoutUser();
        } else {
            console.log('Failed to get profile');
        }
        console.log(input);
        let inboxData = {
            summary: 'I want to follow you',
            type: 'Follow',
            object: {
                url: input
            },
            inbox_urls : [getInboxUrl(input)],
            actor : profile 
        }
        const [ frResponse, frData ] = await Backend.post(`/api/node/object/`, authTokens.access, JSON.stringify(inboxData));
        if (frResponse.status && frResponse.status === 201) {
            console.log("Sent follow request");
        } else if (frResponse.statusText === 'Unauthorized'){
            logoutUser();
        } else {
            console.log('Failed to send request');
            console.debug(frResponse);
        }
    }


    // render functions ------------------------------------------
    const renderSearchBar = () => {
        return (
            <>
            <BasicCard 
                content = {<SearchBar 
                    placeholder='Enter Author ID'
                    onChange={(event) => handleChange(event)}
                    onSearch={() => sendFollowRequest()}
                />}
            />
            </>
        )
    }
    const renderFollowers = (followers) => {
        if (!followers || followers.length <= 0) return (<Typography paragraph >No Followers</Typography>);
        let itemsRender = [];
        followers.forEach((follower, idx) => {
            itemsRender.push(
                <AuthorCard author = {follower} size = "medium"> 
                    <div>
                        <IconButton 
                            aria-label="delete-follower"
                            onClick={()=> deleteFollower(follower, idx)}>
                        <PersonRemoveIcon/>
                        </IconButton>
                    </div>
                </AuthorCard>
            );
            itemsRender.push(<br key={idx + followers.length}></br>);
        });
        return (<>{itemsRender}</>);
    }
    // RENDER APP =================================================
    return (
    <>
        <PageHeader followers={followers} title='Followers'></PageHeader>
        <GridWrapper>
            {renderSearchBar()}
            {renderFollowers(followers)}
        </GridWrapper>
    </>
  )
}

export default Followers
