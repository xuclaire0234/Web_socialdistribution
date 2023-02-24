/*
2023-02-19
pages/Stream.js

This code is modified from a tutorial video about Authentication & Refreshing Tokens from Dennis Ivy on 2022-06-02, retrieved on 2023-02-19, to youtube.com
tutorial video here:
https://www.youtube.com/watch?v=2k8NleFjG7I
*/

import React, { useContext, useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';

import PostSummary from '../components/PostSummary';
import AuthContext from '../context/AuthContext';

const Stream = () => {
    //  variable declarations -------------------------------------
    const [ posts, setPosts ] = useState([]);
    const navigate = useNavigate();
    const { user, authTokens } = useContext(AuthContext);
    
    //  event listners --------------------------------------------
    useEffect(
        () => {
            getPosts();
        }, []);

    //  async functions -------------------------------------------
    const getPosts = async () => {
        const getPostsUrl = 'http://localhost:8000/api/authors/' + user.user_id + '/posts/';
        const response = await fetch(getPostsUrl, {
            headers: {
                'Authorization': 'Bearer ' + String(authTokens.access)
            }
        });
        const data = await response.json()
        if (response.status && response.status === 200) {
            setPosts(data);
        } else {
            console.log('Failed to get posts');
        }
    };

    const renderPosts = (posts) => {
        if (!posts || posts.length <= 0) {
            return(
                <div>No posts</div>
            );
        } else {
            console.log('XXX got posts', posts)
            return(
                <div>
                    {posts.map(post =>(
                        <div key={post.id}>
                            <PostSummary authorobject={post.author_id} description={post.description} postid={post.id}></PostSummary>
                            <br></br>
                        </div> 
                    ))}
                </div>
            );
        }
    };
    // RENDER APP =================================================
    return (
        <>
            <button onClick={() => {
                navigate('/createpost');
            }}>
                Make a post
            </button>

            <br/>
            <button onClick={() => {
                navigate('/post')
            }}> 
                View a post
            </button>
            {renderPosts(posts)}
        </>
    );
}

export default Stream;
